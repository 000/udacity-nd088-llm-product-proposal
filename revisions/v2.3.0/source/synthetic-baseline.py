#!/usr/bin/env python3
"""Reproduce the user-supplied SYNTHETIC baseline, not customer telemetry.

The final attachment generator is retained without RNG/parameter changes.
Its unused SciPy import is omitted. NumPy and pandas are required.
All rate inputs and taxonomy are assumptions, not verified BLS benchmarks.
"""
import hashlib
import numpy as np
import pandas as pd

rng = np.random.default_rng(20261116)
N_POP = 1500  # Synthetic assumption: 150 * 10; no observation occurred.

domains = [
    ("D1_Install_Calib",   300, 0.44, 0.54, 13.0, 21.0),
    ("D2_Kinematics_Prog", 300, 0.33, 0.60, 17.0, 27.0),
    ("D3_Elec_PLC_IO",     275, 0.30, 0.63, 18.5, 29.0),
    ("D4_Parts_Catalog",   325, 0.34, 0.52, 19.5, 20.0),
    ("D5_Fault_Safety",    300, 0.25, 0.72, 22.0, 34.0),
]
families = {
    300: [("F1_Light6Axis", 125, 0.95), ("F2_HeavyArtic", 100, 1.08), ("F3_SCARA_Delta", 75, 0.98)],
    275: [("F1_Light6Axis", 100, 0.95), ("F2_HeavyArtic", 100, 1.08), ("F3_SCARA_Delta", 75, 0.98)],
    325: [("F1_Light6Axis", 125, 0.95), ("F2_HeavyArtic", 125, 1.08), ("F3_SCARA_Delta", 75, 0.98)],
}

rows = []
for d_name, N_dom, p_res, p_esc_u, med_s, med_sup in domains:
    for f_name, Nh, f_mult in families[N_dom]:
        sid, nh = f"{d_name[:2]}_{f_name[:2]}", (Nh * 4) // 25
        non_eng = rng.binomial(1, 0.40, size=Nh)
        eff_p_res = np.clip(p_res * np.where(non_eng == 1, 0.76, 1.14) / f_mult, 0.05, 0.95)
        res = rng.binomial(1, eff_p_res)
        esc = np.where(res == 1, 0, rng.binomial(1, p_esc_u, size=Nh))
        abn = 1 - res - esc
        s_min = rng.lognormal(np.log(med_s * f_mult), 0.56, size=Nh) * np.where(non_eng == 1, 1.16, 0.91)
        ack_min = np.where(esc == 1, rng.lognormal(np.log(39.0), 0.50, size=Nh), 0.0)
        sup_min = np.where(esc == 1, rng.lognormal(np.log(med_sup * f_mult), 0.48, size=Nh), 0.0)
        sampled = np.isin(np.arange(Nh), rng.choice(Nh, size=nh, replace=False)).astype(int)
        for i in range(Nh):
            rows.append((sid, d_name, f_name, Nh, nh, int(non_eng[i]), int(sampled[i]),
                         int(res[i]), int(esc[i]), int(abn[i]),
                         float(s_min[i]), float(ack_min[i]), float(sup_min[i])))

df = pd.DataFrame(rows, columns=["sid","domain","family","Nh","nh","non_eng","sampled","res","esc","abn","s_min","ack_min","sup_min"])

from pathlib import Path
from statistics import NormalDist
import json, math, platform

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "simulation"
OUT.mkdir(parents=True, exist_ok=True)
CLAIMED_HASH = "cef03be7adb723bab005ea3d5ab679c3f418910d5f2612f5f7eccd74c9013de2"
ATTACHMENT_SHA256 = "e32d34fdbf943a8a4a56d1322fa183b13e2e8fb54c534419c3563a17fb34f0e7"
FINAL_BLOCK_SHA256 = "992d4a6530c9f3e76e0dbf04dbf558fc4e1672d609917987ce17683b0ce02108"
raw_csv = df.round(6).to_csv(index=False).encode("utf-8")
raw_hash = hashlib.sha256(raw_csv).hexdigest()
(OUT / "synthetic-baseline-canonical.csv").write_bytes(raw_csv)
normalized = df.round(6).copy()
normalized.insert(0, "synthetic_query_id", [f"SYN-Q-{i:04d}" for i in range(1, len(df)+1)])
normalized.insert(0, "data_status", "SYNTHETIC_SIMULATION")
normalized_csv = normalized.to_csv(index=False).encode("utf-8")
(OUT / "synthetic-baseline-normalized.csv").write_bytes(normalized_csv)
samp = df[df["sampled"] == 1]
escalated = df[df["esc"] == 1]
st = samp.groupby("sid").agg(Nh=("Nh","first"), nh=("nh","first"), mean=("s_min","mean"), variance=("s_min",lambda x: np.var(x,ddof=1)))
weights = st["Nh"] / N_POP
variance_no_fpc = float(np.sum(weights**2 * st["variance"] / st["nh"]))
variance_fpc = float(np.sum(weights**2 * (1-st["nh"]/st["Nh"]) * st["variance"] / st["nh"]))
se = math.sqrt(variance_fpc)
# Numerical Student-t quantile: composite Simpson CDF and bisection.
# This is a conditional illustrative sampling calculation, not field evidence.
def t_quantile_975(dof, panels=1024):
    constant = math.exp(math.lgamma((dof+1)/2)-math.lgamma(dof/2))/math.sqrt(dof*math.pi)
    def cdf(value):
        grid = np.linspace(0, value, panels+1)
        density = constant * (1+grid*grid/dof)**(-(dof+1)/2)
        area = value/panels/3*(density[0]+density[-1]+4*density[1:-1:2].sum()+2*density[2:-1:2].sum())
        return 0.5+float(area)
    lo, hi = 0.0, 16.0
    for _ in range(60):
        mid=(lo+hi)/2
        if cdf(mid)<0.975: lo=mid
        else: hi=mid
    return (lo+hi)/2
critical = t_quantile_975(len(samp)-len(st))
critical_coarse = t_quantile_975(len(samp)-len(st),512)
assert abs(critical-critical_coarse)<1e-7
mean_search = float(samp["s_min"].mean())
mean_support = float(escalated["sup_min"].mean())
assert math.isclose(mean_search,float(np.sum(weights*st["mean"])),abs_tol=1e-12)
ci = [mean_search-critical*se,mean_search+critical*se]
def wilson(k,n):
    z=NormalDist().inv_cdf(0.975);p=k/n;den=1+z*z/n
    center=(p+z*z/(2*n))/den;half=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/den
    return [center-half,center+half]
counts={key:int(df[key].sum()) for key in ["res","esc","abn"]}
assert sum(counts.values())==N_POP and len(st)==15 and int(df["sampled"].sum())==240
assert all(st["nh"]>=12) and np.allclose(st["nh"]/st["Nh"],0.16)
assert math.isclose(variance_fpc/variance_no_fpc,0.84,abs_tol=1e-12)
tech_hours=N_POP*mean_search/60
support_hours=counts["esc"]*mean_support/60
rates={"assumed_us_reference":{"technician_per_hour":52.0,"support_per_hour":68.0},"assumed_lower_rate_case":{"technician_per_hour":32.0,"support_per_hour":54.0}}
costs={}
for label,rate in rates.items():
    tech=tech_hours*rate["technician_per_hour"];support=support_hours*rate["support_per_hour"]
    costs[label]={"technician_search_labor":tech,"support_active_labor":support,"combined_distinct_owners":tech+support,"assumed_22_day_multiplier":2.2,"assumed_22_day_total":(tech+support)*2.2,"assumed_30_day_multiplier":3.0,"assumed_30_day_total":(tech+support)*3.0}
assert math.isclose(support_hours,float(escalated["sup_min"].sum())/60,abs_tol=1e-10)
rounded_tech=N_POP*round(mean_search,2)/60*52
rounded_support=counts["esc"]*round(mean_support,2)/60*68
language={}
for flag,label in [(0,"synthetic_english_primary"),(1,"synthetic_non_english_primary")]:
    pop=df[df["non_eng"]==flag];sample=samp[samp["non_eng"]==flag]
    language[label]={"population_rows":len(pop),"resolved_rows":int(pop["res"].sum()),"sample_rows":len(sample),"sample_search_median_minutes":float(sample["s_min"].median())}
summary={
 "data_status":"SYNTHETIC_SIMULATION_ONLY",
 "observed_customer_rows":0,
 "population_rows":len(df),"timed_sample_rows":len(samp),"strata":len(st),"outcomes":counts,
 "search":{"sample_mean_minutes":mean_search,"sample_median_minutes":float(samp["s_min"].median()),"sample_sd_minutes":float(samp["s_min"].std(ddof=1)),"sample_quantiles_25_75_95":[float(x) for x in np.percentile(samp["s_min"],[25,75,95])],"sample_above_30_minutes":int((samp["s_min"]>30).sum()),"known_synthetic_population_mean_minutes":float(df["s_min"].mean())},
 "support":{"synthetic_escalation_rows":len(escalated),"active_mean_minutes":mean_support,"active_median_minutes":float(escalated["sup_min"].median()),"acknowledgement_mean_minutes":float(escalated["ack_min"].mean()),"acknowledgement_median_minutes":float(escalated["ack_min"].median())},
 "conditional_sampling_diagnostic":{"variance_fpc_factor":0.84,"se_fpc_factor":math.sqrt(0.84),"stratified_se_minutes":se,"t_degrees_freedom":len(samp)-len(st),"t_critical_975":critical,"critical_panel_convergence_difference":abs(critical-critical_coarse),"illustrative_95_interval_minutes":ci,"scope":"Approximate design-based interval for the mean of this fixed synthetic population under its specified within-stratum sampling scheme. It is not a customer-population or model-parameter interval."},
 "wilson_formula_diagnostic":{key:{"rate":value/N_POP,"interval":wilson(value,N_POP)} for key,value in counts.items()},
 "wilson_scope":"Numerical reconciliation only. Rates of the fully generated synthetic population are known exactly. These intervals are not field estimates; heterogeneous generated probabilities also differ from a common-probability iid Bernoulli assumption.",
 "language_slices":language,"rate_assumptions":rates,"labor_hours":{"estimated_technician_search":tech_hours,"generated_support_active":support_hours},"cost_cases":costs,
 "rounding_reconciliation":{"technician_from_two_decimal_mean":rounded_tech,"support_from_two_decimal_mean":rounded_support,"combined_delta_from_two_decimal_means":rounded_tech+rounded_support-costs["assumed_us_reference"]["combined_distinct_owners"]},
 "cost_interval_diagnostic":{"technician_only":[N_POP*x/60*52 for x in ci],"combined_with_fixed_generated_support":[N_POP*x/60*52+support_hours*68 for x in ci],"scope":"Only conditional technician-time sampling uncertainty; assumed rates and generated support hours held fixed. Not a forecast, financial statement or savings interval."},
 "provenance_limits":["All language probabilities, duration multipliers, domains and family assignments are coded assumptions; differences are not causal evidence.","The final generator has no technician, asset, site, date, PII or CRM identifiers. Added SYN-Q values are fabricated row labels, not pseudonymized identities.","The 15 grouped strata are a simulation taxonomy with no demonstrated mapping to actual 25 topics or 15 models.","The 375-cell empty-strata criticism assumes every topic/model combination is relevant and nonempty; the scenario alone does not establish that.","US/reference and lower-rate inputs are unverified assumptions, not verified BLS or regional-wage benchmarks.","Languages do not establish worker countries, regional wage weights or geography.","Generated support rows are not a CRM census. All counts and figures remain simulation results.","Four-decimal means are rounded displays; full-precision values drive arithmetic. No measured savings, margin, downtime, industrial safety or product benefit is established.","Distinct technician and support labor owners are reported separately; adding them does not make one company P&L cost."],
 "canonical_csv_sha256":raw_hash,"claimed_canonical_csv_sha256":CLAIMED_HASH,"claimed_hash_reproduced":raw_hash==CLAIMED_HASH,
 "normalized_csv_sha256":hashlib.sha256(normalized_csv).hexdigest(),
 "runtime":{"python":platform.python_version(),"numpy":np.__version__,"pandas":pd.__version__,"scipy":"not installed; unused final-generator import omitted","bit_generator":type(rng.bit_generator).__name__,"seed":20261116},
 "generator_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 "source_adaptation":"Final attachment generator only. Unused SciPy import omitted; one observation-wording comment corrected. RNG parameters, calls and draw order unchanged. No tuning."}
(OUT/"synthetic-baseline-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
meta={"status":"SYNTHETIC_SIMULATION_ONLY","customer_records":0,"canonical_csv":"synthetic-baseline-canonical.csv","normalized_csv":"synthetic-baseline-normalized.csv","summary":"synthetic-baseline-summary.json","canonical_columns":list(df.columns),"normalized_added_columns":{"data_status":"Constant SYNTHETIC_SIMULATION","synthetic_query_id":"Fabricated sequential row label; not a real or de-identified query ID"},"serialization":"pandas DataFrame.round(6).to_csv(index=False), UTF-8, LF; default float formatting","canonical_sha256":raw_hash,"normalized_sha256":hashlib.sha256(normalized_csv).hexdigest(),"runtime":summary["runtime"]}
(OUT/"dataset-metadata.json").write_text(json.dumps(meta,indent=2)+"\n")
check={"status":"reproduced_with_scope_limits" if raw_hash==CLAIMED_HASH else "hash_mismatch_do_not_relabel","input_classification":"User-supplied synthetic generator and analytical narrative, not measured baseline data","attachment_lines_reviewed":721,"source_attachment_sha256":ATTACHMENT_SHA256,"original_final_code_block_sha256":FINAL_BLOCK_SHA256,"final_block_hash_scope":"UTF-8 code-fence payload without trailing newline","python_blocks_inspected":5,"canonical_generator":"Final42-line Python block only","static_inspection":"Final block contains numerical/dataframe/hash operations only; no network, credentials, filesystem or process calls","untouched_execution":"Blocked by absent unused SciPy import; transparently omitted for reproduction","claimed_hash":CLAIMED_HASH,"actual_hash":raw_hash,"claimed_hash_matches":raw_hash==CLAIMED_HASH,"observed_customer_rows":0,"actual_counts":counts,"actual_search_sample_mean_minutes":mean_search,"actual_support_mean_minutes":mean_support,"finite_population_variance_factor":0.84,"finite_population_se_factor":math.sqrt(0.84),"mean_cost_arithmetic_checked":True,"runtime":summary["runtime"],"generator_sha256":summary["generator_sha256"],"summary_sha256":hashlib.sha256((OUT/"synthetic-baseline-summary.json").read_bytes()).hexdigest(),"limits":summary["provenance_limits"],"inference_or_customer_data_use":False}
(ROOT/"evidence/synthetic-baseline-check.json").write_text(json.dumps(check,indent=2)+"\n")
print(json.dumps({key:summary[key] for key in ["claimed_hash_reproduced","canonical_csv_sha256","outcomes","search","support","conditional_sampling_diagnostic","labor_hours","cost_cases","runtime"]},indent=2))
if raw_hash!=CLAIMED_HASH: raise SystemExit(1)
