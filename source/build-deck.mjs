import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const packageRoot = path.basename(here) === 'source' ? path.dirname(here) : path.join(here, 'package');
const workspaceDir = process.env.LINEGUIDE_WORKSPACE_DIR || packageRoot;
const outputDir = process.env.LINEGUIDE_OUTPUT_DIR || path.join(packageRoot, 'submission');
const buildDir = process.env.LINEGUIDE_BUILD_DIR || path.join(here, 'render-build');
const previews = process.env.LINEGUIDE_PREVIEW_DIR || path.join(here, 'previews');
const content = JSON.parse(await fs.readFile(path.join(here, 'deck-content.json'), 'utf8'));
await Promise.all([outputDir, buildDir, previews].map(p => fs.mkdir(p, { recursive: true })));
const W=1280, H=720;
const ink='#0B2133', muted='#405B68', teal='#006D77', accent='#B34E22', rule='#CAD5DB', paper='#FAFCFC';
const font='Arial';
const p = Presentation.create({slideSize:{width:W,height:H}});
const geometry=[];
function text(s,t,x,y,w,h,size=25,color=ink,bold=false,name='text') {
  const z=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  z.text=t;
  z.text.style={fontSize:size,typeface:font,color,bold,verticalAlignment:'top',alignment:'left',wrap:'square',autoFit:'none',insets:0};
  geometry.push({slide:p.slides.items.length,name,x,y,w,h,size,text:t});
  return z;
}
function line(s,x,y,w,color=rule){return s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},fill:'none',line:{fill:color,width:1}});}
function base(d,i) {
  const s=p.slides.add();s.background.fill=paper;
  if(d.type!=='cover')text(s,d.title,64,42,1152,96,44,ink,true,'slide-title');
  line(s,64,660,1152);
  text(s,d.footer||'Hypothetical product proposal. Proposed targets are unmeasured.',64,677,1080,24,15,muted,false,'footer');
  text(s,String(i+1).padStart(2,'0'),1174,675,42,26,17,muted,false,'slide-number');
  const citations=(d.sources||[]).map(id=>{const z=content.sources.find(x=>x.id===id);return z?`${id}: ${z.title}\n${z.url}\nLimit: ${z.limit||'Vendor documentation establishes features, not application performance.'}`:id;}).join('\n\n');
  s.speakerNotes.text=`${d.notes||''}\n\nEvidence status: ${d.status||'Design proposal; no production deployment or user study has been run.'}\n\nSources checked 16 November 2026:\n${citations}`;
  return s;
}
function table(s,d){
  const vals=[d.headers,...d.rows];
  const t=s.tables.add({rows:vals.length,columns:d.headers.length,left:64,top:d.top||156,width:1152,height:d.height||440,columnWidths:d.widths,values:vals});
  t.borders.assign({style:'solid',fill:rule,width:0.65});
  for(let r=0;r<vals.length;r++)for(let c=0;c<vals[r].length;c++){
    const cell=t.getCell(r,c);cell.fill=r===0?ink:(r%2?'#FFFFFF':'#EFF4F5');
    cell.text.style={typeface:font,fontSize:d.fontSize||23,bold:r===0,color:r===0?'#FFFFFF':ink,wrap:'square',autoFit:'none',insets:12,verticalAlignment:'middle'};
  }
  if(d.caption)text(s,d.caption,64,610,1152,42,20,muted,false,'table-caption');
}
function rows(s,d){
  const top=d.top||156, gap=d.gap||108;
  d.rows.forEach((r,j)=>{
    text(s,r[0],64,top+j*gap,290,gap-16,27,teal,true,'row-label');
    text(s,r[1],380,top+j*gap,836,gap-16,d.fontSize||26,ink,false,'row-detail');
    if(j<d.rows.length-1)line(s,64,top+j*gap+gap-15,1152);
  });
  if(d.caption)text(s,d.caption,64,608,1152,40,20,muted,false,'row-caption');
}
function two(s,d){
  text(s,d.leftTitle,64,158,530,52,29,teal,true,'left-title');
  text(s,d.rightTitle,670,158,546,52,29,teal,true,'right-title');
  text(s,d.left,64,226,530,365,d.fontSize||27,ink,false,'left-body');
  text(s,d.right,670,226,546,365,d.fontSize||27,ink,false,'right-body');
  if(d.caption)text(s,d.caption,64,611,1152,40,20,muted,false,'two-caption');
}
function node(s,t,x,y,w,h=82){
  const z=s.shapes.add({geometry:'rect',name:'architecture-node',position:{left:x,top:y,width:w,height:h},fill:'#FFFFFF',line:{fill:teal,width:1.5}});
  z.text=t;z.text.style={fontSize:23,typeface:font,color:ink,bold:false,insets:10,verticalAlignment:'middle',alignment:'center',autoFit:'none',wrap:'square'};
  return z;
}
function arrow(s,a,b,from='right',to='left'){s.shapes.connect(a,b,{kind:'straight',fromSide:from,toSide:to,line:{fill:teal,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});}
function route(s,points,color=teal,dashed=false){
  for(let i=1;i<points.length;i++){
    const [x1,y1]=points[i-1],[x2,y2]=points[i];
    const reverse=x2<x1||y2<y1;
    const end=i===points.length-1?{[reverse?'head':'tail']:{type:'triangle',width:'sm',length:'sm'}}:{};
    s.shapes.add({geometry:'connector',kind:'straight',position:{left:Math.min(x1,x2),top:Math.min(y1,y2),width:Math.abs(x2-x1),height:Math.abs(y2-y1)},line:{fill:color,width:2,...(dashed?{style:'dashed'}:{})},...end});
  }
}
function architecture(s,d){
  text(s,'Device and support edge',64,148,350,34,23,muted,true);
  text(s,'Authenticated backend services',544,148,672,34,23,muted,true);
  const a=node(s,'C1 Mobile\nweb client',64,250,190,90);
  const b=node(s,'C2 Identity and\npolicy API',304,250,190,90);
  const c=node(s,'C3 Hybrid\nretrieval',544,250,190,90);
  const g=node(s,'C4 Generation\nendpoint',784,250,190,90);
  const v=node(s,'C5 Response\nvalidator',1024,250,192,90);
  const h=node(s,'C8 Human\nsupport',64,480,190,90);
  const catalog=node(s,'C7 Parts catalogue',365,480,255,90);
  const audit=node(s,'C10 Audit events',745,480,240,90);
  arrow(s,a,b);arrow(s,b,c);arrow(s,c,g);arrow(s,g,v);
  route(s,[[1120,250],[1120,205],[399,205],[399,250]],accent,true);
  route(s,[[304,295],[280,295],[280,225],[159,225],[159,250]],accent,true);
  text(s,'Validated answer or abstention',596,176,420,28,20,accent);
  text(s,'TLS',261,273,42,28,17,muted);
  route(s,[[399,340],[399,410],[492,410],[492,480]]);
  text(s,'Read-only lookup',415,374,220,28,20,muted);
  route(s,[[620,525],[680,525],[680,400],[1160,400],[1160,340]]);
  text(s,'Exact compatible records',714,365,355,29,20,muted);
  route(s,[[304,315],[285,315],[285,455],[159,455],[159,480]]);
  text(s,'Reviewed escalation',66,417,245,28,20,muted);
  route(s,[[1216,295],[1240,295],[1240,610],[865,610],[865,570]],muted,true);
  text(s,'Minimal trace metadata',877,578,320,27,18,muted);
  s.shapes.add({geometry:'line',position:{left:275,top:237,width:0,height:335},line:{fill:rule,width:1,style:'dashed'}});
  text(s,'Private endpoints and managed identities protect backend links. Robot controllers remain disconnected.',64,622,1152,28,20,ink,true);
}
function ingestion(s,d){
  const source=node(s,'C6 Controlled manuals',64,220,300,90);
  const ingest=node(s,'C9 Ingestion job',490,220,300,90);
  const index=node(s,'C3 Hybrid retrieval',916,220,300,90);
  const audit=node(s,'C10 Audit events',490,430,300,90);
  node(s,'C7 Parts catalogue',916,430,300,90);
  arrow(s,source,ingest);arrow(s,ingest,index);arrow(s,ingest,audit,'bottom','top');
  text(s,'Approval + applicability',64,333,350,30,22,muted);
  text(s,'Versioned chunks + withdrawal',790,333,426,30,22,muted);
  text(s,'Managed identity\nIngestion/revocation records',310,367,300,66,22,muted);
  text(s,'Current catalog stays structured.\nRuntime path: C2 to C7 to C5.',916,541,300,65,21,muted);
  text(s,'Proposed pilot: up to 200 approved English articles, five topics and two models.',64,152,1152,40,27,teal,true);
  text(s,'Review revisions daily. Process withdrawals before serving affected content. Unknown approval, entitlement or freshness means abstention.',64,565,730,78,23,ink,true);
}
function componentRegister(s,d){
  const items=[
   ['C1 Mobile web client','Technician context, sources and support.'],
   ['C2 Identity and policy API','Entra identity, access and orchestration.'],
   ['C3 Hybrid retrieval','Approved text and vector search index.'],
   ['C4 Generation endpoint','Bounded, cited draft through Azure.'],
   ['C5 Response validator','Applicability, citations and exact parts.'],
   ['C6 Controlled manuals','Approved originals with revision metadata.'],
   ['C7 Parts catalogue','Authoritative compatible structured records.'],
   ['C8 Human support','Reviewed escalation through existing support.'],
   ['C9 Ingestion job','Approval checks, chunks and index updates.'],
   ['C10 Audit events','Minimized trace and revocation records.']
  ];
  items.forEach(([label,body],j)=>{
   const x=j<5?64:670,y=156+(j%5)*94;
   text(s,label,x,y,546,35,26,teal,true,'component-label');
   text(s,body,x,y+38,546,49,23,ink,false,'component-description');
  });
}
for(const [i,d]of content.slides.entries()){
 const s=base(d,i);
 if(d.type==='cover'){
   text(s,'LineGuide',64,120,1152,110,80,ink,true,'cover-title');
   text(s,'AI-powered industrial robot\nexpert advisor',64,260,1100,160,48,teal,false,'cover-subtitle');
   text(s,'Scenario C, Udacity ND088\nRevision v1.1.0, 16 November 2026',64,494,1000,105,27,muted,false,'cover-meta');
 }else if(d.type==='table')table(s,d);
 else if(d.type==='rows')rows(s,d);
 else if(d.type==='two')two(s,d);
 else if(d.type==='architecture')architecture(s,d);
 else if(d.type==='ingestion')ingestion(s,d);
 else if(d.type==='component_register')componentRegister(s,d);
 else if(d.type==='statement'){
   text(s,d.statement,64,174,1140,230,42,teal,true,'main-statement');
   text(s,d.body,64,438,1140,176,27,ink,false,'statement-body');
 }else if(d.type==='sources'){
   d.ids.forEach((id,j)=>{const z=content.sources.find(x=>x.id===id);const yy=148+j*92;text(s,`${id}  ${z.title}`,64,yy,1152,34,25,ink,true);const url=text(s,z.url,64,yy+38,1152,45,19,teal);url.text.get(z.url).link={uri:z.url,isExternal:true};});
 }
}
await fs.writeFile(path.join(buildDir,'geometry.json'),JSON.stringify(geometry,null,2));
await fs.writeFile(path.join(buildDir,'presentation.json'),JSON.stringify(p.toProto()));
const candidate=path.join(buildDir,'candidate.pptx');
await(await PresentationFile.exportPptx(p)).save(candidate);
const finalPptx=path.join(outputDir,'LineGuide_Proposal_v1.1.0.pptx');
if(process.env.PRESENTATIONS_SKILL_DIR){
 const sk=process.env.PRESENTATIONS_SKILL_DIR;
 const {finalizePresentation}=await import(pathToFileURL(path.join(sk,'container_tools/artifact_tool_utils.mjs')).href);
 await fs.mkdir(path.join(buildDir,'validated-output'),{recursive:true});
 const validated=path.join(buildDir,'validated-output',`validated-${Date.now()}.pptx`);
 const receipt=path.join(buildDir,`validation-${Date.now()}.json`);
 await finalizePresentation({workspaceDir,candidatePath:candidate,finalPath:validated,pythonExecutable:process.env.RUNTIME_PYTHON||'python3',integrityValidatorPath:path.join(sk,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(sk,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...content.slides.flatMap((x,i)=>x.type==='table'?['--require-native-table-slide',String(i+1)]:[])],requiredNativeTableOwnerSlides:content.slides.flatMap((x,i)=>x.type==='table'?[i+1]:[]),requiredNativeChartOwnerSlides:[],explicitTotalSlideCount:content.slides.length,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:receipt});
 await fs.copyFile(validated,finalPptx);
 await fs.copyFile(receipt,path.join(buildDir,'validation-current.json'));
}else await fs.copyFile(candidate,finalPptx);
// LibreOffice renders the exact delivered PPTX. Artifact Tool's bundled PDF
// exporter currently has an unresolved standard-font alias in this runtime.
execFileSync(process.env.SOFFICE_BINARY||'soffice',['--headless','--convert-to','pdf','--outdir',outputDir,finalPptx],{stdio:'inherit'});
execFileSync(process.env.PDFTOPPM_BINARY||'pdftoppm',['-png','-scale-to','1280',path.join(outputDir,'LineGuide_Proposal_v1.1.0.pdf'),path.join(previews,'slide')],{stdio:'inherit'});
for(const [i,s]of p.slides.items.entries()){
 const stem=`slide-${String(i+1).padStart(2,'0')}`;
 await fs.writeFile(path.join(buildDir,stem+'.layout.json'),await(await s.export({format:'layout'})).text());
}
console.log(JSON.stringify({slides:content.slides.length,pptx:finalPptx,pdf:path.join(outputDir,'LineGuide_Proposal_v1.1.0.pdf'),previews}));
