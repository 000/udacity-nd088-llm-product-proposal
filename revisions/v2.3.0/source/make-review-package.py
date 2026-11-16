#!/usr/bin/env python3
"""Create a candidate-only transcript, diagram source and portable review archive."""
from pathlib import Path
import argparse, hashlib, json, posixpath, shutil, subprocess, zipfile
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
REPO=R.parents[1]
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','pr':'http://schemas.openxmlformats.org/package/2006/relationships'}
def sha(data):return hashlib.sha256(data).hexdigest()
def rels(z,part):
 path=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
 if path not in z.namelist():return {}
 return {x.get('Id'):x for x in ET.fromstring(z.read(path))}
def target(part,rel):
 assert rel.get('TargetMode','Internal')!='External'
 raw=rel.get('Target')
 p=posixpath.normpath(raw.lstrip('/') if raw.startswith('/') else posixpath.join(posixpath.dirname(part),raw))
 assert not p.startswith('../')
 return p

def lines(root,notes=False):
 skip=set()
 if notes:
  for shape in root.findall('.//p:sp',NS):
   ph=shape.find('p:nvSpPr/p:nvPr/p:ph',NS)
   if ph is not None and ph.get('type')=='sldNum':skip.update(shape.findall('.//a:p',NS))
 result=[]
 for p in root.findall('.//a:p',NS):
  if p in skip:continue
  text=''.join((x.text or '') if x.tag=='{'+NS['a']+'}t' else '\n' if x.tag=='{'+NS['a']+'}br' else '' for x in p.iter()).strip()
  if text:result.append(text)
 return result

def prepare():
 content=json.loads((R/'source/deck-content.json').read_text());pptx=R/'artifact/LineGuide_Proposal_v2.3.0.pptx'
 output=['# LineGuide2.3.0: exact slide text and speaker notes'.replace('LineGuide2','LineGuide 2'),'','Extracted from the actual PPTX. Text inside images is outside this extraction; the PDF and standalone diagrams support visual review.','',f'PPTX SHA-256: `{sha(pptx.read_bytes())}`.','']
 with zipfile.ZipFile(pptx) as z:
  presentation='ppt/presentation.xml';links=rels(z,presentation)
  ids=ET.fromstring(z.read(presentation)).findall('p:sldIdLst/p:sldId',NS)
  for n,item in enumerate(ids,1):
   part=target(presentation,links[item.get('{'+NS['r']+'}id')]);root=ET.fromstring(z.read(part))
   output += [f'## Slide{n}: {content["slides"][n-1]["title"]}'.replace('Slide'+str(n),'Slide '+str(n)),'','### Visible text','',*lines(root),'','### Speaker notes','']
   notes=[v for v in rels(z,part).values() if v.get('Type','').endswith('/notesSlide')]
   assert len(notes)==1
   output+=lines(ET.fromstring(z.read(target(part,notes[0]))),True)+['']
 (R/'slides-and-notes.md').write_text('\n'.join(output).rstrip()+'\n')
 dest=R/'diagrams';dest.mkdir(exist_ok=True)
 names=[('runtime',8),('ingestion',17)]
 for name,n in names:shutil.copyfile(R/f'previews/slide-{n:02}.png',dest/(name+'.png'))
 m=['%% Logical proposed flows. No deployed network or industrial-safety certification.','flowchart TB']
 for name,number in names:
  slide=content['slides'][number-1];prefix=name+'_';m+=['  subgraph '+name+'["'+slide['title']+'"]','    direction LR']
  nodes={n['id']:n for n in slide['nodes']}
  def emit(ids):
   for key in ids:m.append('    '+prefix+key+'['+json.dumps(nodes[key]['label'])+']')
  if name=='runtime':
   m+=['    subgraph runtime_internet["Authenticated internet boundary"]'];emit(['client','identity']);m+=['    end','    subgraph runtime_private["Private application and data services"]'];emit(['api','policy','index','validator','parts','support','audit']);m+=['    subgraph runtime_provider["Provider processing boundary"]'];emit(['model']);m+=['    end','    end']
  else:
   m+=['    subgraph ingestion_private["Private ingestion and data boundary"]'];emit(['sources','ingestion','index','parts','audit']);m+=['    subgraph ingestion_provider["Provider embedding boundary"]'];emit(['embedding']);m+=['    end','    end']
  for edge in slide['edges']:
   arrow='-.->' if edge.get('dashed') else '-->'
   label=(edge.get('label','')+' / TLS1.2+').strip(' /').replace('TLS1','TLS 1').replace('"',"'")
   m.append('    '+prefix+edge['from']+' '+arrow+(' |"'+label+'"|' if label else '')+' '+prefix+edge['to'])
  m+=['  end']
 m+=['%% All network links require TLS1.2+; managed identities/private endpoints where supported.'.replace('TLS1','TLS 1'),'%% Application/source/index/catalogue/audit stores require encryption and scoped RBAC.','%% Runtime internet boundary: Mobile client and Entra ID. Provider boundaries: Generation endpoint and Embedding endpoint.']
 # The native rendered diagrams preserve exact geometry; Mermaid preserves logical boundary membership.
 (dest/'architecture.mmd').write_text('\n'.join(m)+'\n')
 (dest/'README.md').write_text('# Standalone architecture\n\n`runtime.png` and `ingestion.png` are exact renders of final PDF pages8and17, respectively. They show the native diagrams, labels, trust/provider boundaries and connection controls. `architecture.mmd` is a logical flow specification using the same canonical component names and edges. Its subgraphs identify boundary membership; the PNGs preserve their precise nested visual placement. These are proposed designs, not a deployed or safety-certified system.\n'.replace('pages8and17','pages 8 and 17'))
 print(json.dumps({'slides':len(ids),'transcript':'slides-and-notes.md','diagrams':['diagrams/runtime.png','diagrams/ingestion.png','diagrams/architecture.mmd']}))

def snapshot():
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
 proof={'source_artifact_commit':head,'repository_url':'https://github.com/000/udacity-nd088-llm-product-proposal','default_branch':'main','scope':'Git metadata captured after publishing the artifact content commit. Envelope documents/manifests and archive are added by a subsequent commit; this is not a self-referential final-HEAD claim.','git_status':subprocess.check_output(['git','status','--short','--branch'],cwd=REPO,text=True),'recent_commits':subprocess.check_output(['git','log','-n','3','--oneline'],cwd=REPO,text=True).splitlines(),'head_tree':subprocess.check_output(['git','ls-tree','-r','--long',head],cwd=REPO,text=True).splitlines()}
 (R/'evidence/repository-snapshot.json').write_text(json.dumps(proof,indent=2)+'\n')
 print(head)

def archive():
 output=REPO/'review/LineGuide_Review_v2.3.0.zip';output.parent.mkdir(exist_ok=True)
 files={str(p.relative_to(REPO)):p.read_bytes() for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 for rel in ['README.md','CURRENT.json','VERSION','verify.py','tools/extract-audit.sh','docs/academic-integrity.md']:
  files[rel]=(REPO/rel).read_bytes()
 files['START-HERE.md']=b'# LineGuide2.3.0 review bundle\n\nOpen revisions/v2.3.0/artifact/LineGuide_Proposal_v2.3.0.pdf or the editable PPTX beside it. Complete slide text/notes and standalone architecture PNGs/Mermaid are inside that same candidate directory. Its SHA256SUMS verifies every candidate file except itself. CURRENT.json identifies the sole current candidate. Earlier versions are omitted from this bundle.\n\nThis is a hypothetical course proposal with labelled scenario facts, assumptions and synthetic illustrations. Evaluation describes future implementation work. No classroom submission is claimed.\n'
 files['START-HERE.md']=files['START-HERE.md'].replace(b'LineGuide2',b'LineGuide 2')
 files['BUNDLE-SHA256SUMS']=''.join(sha(data)+'  '+name+'\n' for name,data in sorted(files.items())).encode()
 with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in sorted(files.items()):
   info=zipfile.ZipInfo(name,date_time=(2026,11,16,0,0,0));info.external_attr=0o644<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
 with zipfile.ZipFile(output) as z:
  assert z.testzip() is None
  assert all(z.read(name)==data for name,data in files.items())
 print(json.dumps({'archive':str(output.relative_to(REPO)),'members':len(files),'bytes':output.stat().st_size,'sha256':sha(output.read_bytes()),'exact_member_readback':True}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','snapshot','zip']);args=p.parse_args();{'prepare':prepare,'snapshot':snapshot,'zip':archive}[args.action]()
