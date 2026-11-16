#!/usr/bin/env python3
"""Verify the published revision with Python3's standard library only."""
from pathlib import Path
import argparse, hashlib, json, math, re, zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def verify(manifest=True):
 d=json.loads((ROOT/'source/deck-content.json').read_text()); checks=[]
 assert d['version']=='2.2.0' and len(d['slides'])==24
 sources=json.loads((ROOT/'docs/sources.json').read_text())['sources']; ids={r['id'] for r in sources}
 assert ids=={'R'+str(i).zfill(2) for i in range(1,13)}
 assert {r['id']:r['url'] for r in sources}=={r['id']:r['url'] for r in d['sources']}
 for slide in d['slides']:
  assert set(slide.get('sources',[]))<=ids
  assert slide.get('notes','').strip()
 components=json.loads((ROOT/'docs/components.json').read_text())['components']
 diagrams=[s for s in d['slides'] if s['type']=='diagram']
 assert len(diagrams)==2
 actual={n['id']:n['label'] for s in diagrams for n in s['nodes']}
 assert actual=={c['id']:c['name'] for c in components}
 for s in diagrams:
  node_ids={n['id'] for n in s['nodes']}
  assert all(e['from'] in node_ids and e['to'] in node_ids for e in s['edges'])
  assert all(n['label'] in s['notes'] for n in s['nodes'])
 edges={(e['from'],e['to']) for e in diagrams[0]['edges']}
 assert {('validator','api'),('api','client'),('policy','support'),('parts','validator')}<=edges
 checks+=['24 source slides with notes; 12 synchronized references','13 canonical component names match both native diagram sources; return and fallback edges present']
 metrics=json.loads((ROOT/'docs/metrics.json').read_text())
 assert len(metrics['metrics'])==5 and all(m['measured_value'] is None for m in metrics['metrics'])
 e=metrics['economics'];q=e['scenario_given_queries_per_day']*e['assumed_service_days_per_month'];cost=e['assumed_cloud_allowance_per_month']+e['assumed_review_hours_per_month']*e['assumed_review_hourly_cost']
 for c in e['cases']:
  count=q*c['eligible_share']*c['adoption_share']*c['verified_resolution_share']; value=count*c['minutes_saved']/60*e['assumed_hourly_capacity_value']
  assert math.isclose(count,c['successful_sessions'],abs_tol=1e-7)
  assert math.isclose(value,c['capacity_value'],abs_tol=1e-7)
  assert math.isclose(value-cost,c['net_before_implementation'],abs_tol=1e-7)
 checks+=['Five proposed KPIs remain unmeasured; all three capacity-value cases independently recomputed']
 pptx=ROOT/'artifact/LineGuide_Proposal_v2.2.0.pptx';pdf=ROOT/'artifact/LineGuide_Proposal_v2.2.0.pdf'
 assert pptx.read_bytes().startswith(b'PK') and pdf.read_bytes().startswith(b'%PDF-')
 with zipfile.ZipFile(pptx) as z:
  assert z.testzip() is None
  slides=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)],key=lambda n:int(re.search(r'(\d+)\.xml',n).group(1)))
  notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
  assert len(slides)==len(notes)==24
  roots=[ET.fromstring(z.read(n)) for n in slides]
  combined='\n'.join(t.text or '' for r in roots for t in r.findall('.//a:t',NS))
  for c in components: assert c['name'] in combined,c['name']
  for term in ['gpt-6-astra','2026-09-03','store=false','0.1','7,500','45,000','Cantonese','Urdu','85%','35%']:
   assert term in combined,term
  assert all(''.join(ET.fromstring(z.read(n)).itertext()).strip() for n in notes)
  tables=sum(len(r.findall('.//a:tbl',NS)) for r in roots)
  assert tables==8,tables
  assert all(not p.read_bytes().startswith(b'version https://git-lfs.github.com/spec/v1') for p in [pptx,pdf])
 checks+=['Actual PDF/PPTX headers and PPTX ZIP CRC; 24 slides and 24 notes; eight native tables','Canonical components, scenario ledger and concrete configuration are present in exported slide text; no LFS pointers']
 for p in ROOT.rglob('*'):
  if p.is_file() and p.suffix in {'.md','.json','.mjs','.py','.txt'} and p!=Path(__file__).resolve():
   text=p.read_text()
   assert '/Users/' not in text, str(p)
   assert '-----BEGIN '+'PRIVATE KEY-----' not in text
 count=None
 if manifest:
  entries=[]
  for line in (ROOT/'SHA256SUMS').read_text().splitlines():
   digest,rel=line.split('  ',1);p=ROOT/rel
   assert p.resolve().is_relative_to(ROOT)
   assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,rel
   entries.append(rel)
  files={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts}
  assert set(entries)==files and len(entries)==len(files)
  count=len(entries);checks+=['Complete package manifest coverage and every SHA-256 verified']
 return dict(status='passed',scope='Artifact integrity and design-source consistency only; no operational or academic certification',checks=checks,slides=24,notes=24,native_tables=tables,canonical_components=len(components),references=12,manifest_files_checked=count)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--without-manifest',action='store_true');args=p.parse_args()
 try: print(json.dumps(verify(not args.without_manifest),indent=2))
 except (AssertionError,OSError,ValueError,KeyError,zipfile.BadZipFile,ET.ParseError) as exc:
  print(json.dumps({'status':'failed','error':str(exc)}));raise SystemExit(1)
