import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const packageRoot = path.basename(here) === 'source' ? path.dirname(here) : path.join(here, 'package');
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
  text(s,d.footer||'Hypothetical product proposal • Proposed targets are unmeasured',64,677,1080,24,15,muted,false,'footer');
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
function architecture(s,d){
  text(s,'Device / public edge',64,148,320,38,23,muted,true);
  text(s,'Private application and data services',405,148,811,38,23,muted,true);
  const a=node(s,'Mobile web app\nTechnician + model ID',64,218,240,90);
  const b=node(s,'Entra ID + API\nAuthZ and risk policy',374,218,255,90);
  const c=node(s,'Hybrid retrieval\nTenant + model + revision',699,218,247,90);
  const e=node(s,'Azure OpenAI\nCited draft only',1016,218,200,90);
  arrow(s,a,b);arrow(s,b,c);arrow(s,c,e);
  const f=node(s,'Validation\nCitations + parts',1016,385,200,90);
  const g=node(s,'Approved manuals\nBlob + search index',699,385,247,90);
  const catalog=node(s,'Parts catalogue\nAPI-only SQL lookup',374,385,255,90);
  const h=node(s,'Human support\nEscalation via API',64,385,240,90);
  arrow(s,e,f,'bottom','top');arrow(s,g,c,'top','bottom');arrow(s,b,catalog,'bottom','top');
  arrow(s,b,h,'bottom','top');
  s.shapes.add({geometry:'connector',kind:'straight',position:{left:501,top:475,width:0,height:35},line:{fill:teal,width:2}});
  s.shapes.add({geometry:'connector',kind:'straight',position:{left:501,top:510,width:615,height:0},line:{fill:teal,width:2}});
  s.shapes.add({geometry:'connector',kind:'straight',position:{left:1116,top:475,width:0,height:35},line:{fill:teal,width:2},head:{type:'triangle',width:'sm',length:'sm'}});
  text(s,'Exact catalog records',700,481,310,28,23,muted);
  s.shapes.add({geometry:'line',position:{left:340,top:193,width:0,height:300},fill:'none',line:{fill:rule,width:1,style:'dashed'}});
  text(s,'TLS',312,242,55,30,18,muted);
  text(s,'Back-end links use private endpoints and managed identities. The API returns validated answers to the app; robot controllers remain disconnected.',64,552,1152,85,24,ink,true);
}
for(const [i,d]of content.slides.entries()){
 const s=base(d,i);
 if(d.type==='cover'){
   text(s,'LineGuide',64,120,1152,110,80,ink,true,'cover-title');
   text(s,'AI-powered industrial robot\nexpert advisor',64,260,1100,160,48,teal,false,'cover-subtitle');
   text(s,'Scenario C • Udacity ND088\nStakeholder proposal • 16 November 2026',64,494,1000,105,27,muted,false,'cover-meta');
 }else if(d.type==='table')table(s,d);
 else if(d.type==='rows')rows(s,d);
 else if(d.type==='two')two(s,d);
 else if(d.type==='architecture')architecture(s,d);
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
const finalPptx=path.join(outputDir,'LineGuide_Proposal.pptx');
if(process.env.PRESENTATIONS_SKILL_DIR){
 const sk=process.env.PRESENTATIONS_SKILL_DIR;
 const {finalizePresentation}=await import(pathToFileURL(path.join(sk,'container_tools/artifact_tool_utils.mjs')).href);
 await fs.mkdir(path.join(buildDir,'validated-output'),{recursive:true});
 const validated=path.join(buildDir,'validated-output',`validated-${Date.now()}.pptx`);
 const receipt=path.join(buildDir,`validation-${Date.now()}.json`);
 await finalizePresentation({workspaceDir:here,candidatePath:candidate,finalPath:validated,pythonExecutable:process.env.RUNTIME_PYTHON||'python3',integrityValidatorPath:path.join(sk,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(sk,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...content.slides.flatMap((x,i)=>x.type==='table'?['--require-native-table-slide',String(i+1)]:[])],requiredNativeTableOwnerSlides:content.slides.flatMap((x,i)=>x.type==='table'?[i+1]:[]),requiredNativeChartOwnerSlides:[],explicitTotalSlideCount:content.slides.length,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:receipt});
 await fs.copyFile(validated,finalPptx);
 await fs.copyFile(receipt,path.join(buildDir,'validation-current.json'));
}else await fs.copyFile(candidate,finalPptx);
// LibreOffice renders the exact delivered PPTX. Artifact Tool's bundled PDF
// exporter currently has an unresolved standard-font alias in this runtime.
execFileSync(process.env.SOFFICE_BINARY||'soffice',['--headless','--convert-to','pdf','--outdir',outputDir,finalPptx],{stdio:'inherit'});
execFileSync(process.env.PDFTOPPM_BINARY||'pdftoppm',['-png','-scale-to','1280',path.join(outputDir,'LineGuide_Proposal.pdf'),path.join(previews,'slide')],{stdio:'inherit'});
for(const [i,s]of p.slides.items.entries()){
 const stem=`slide-${String(i+1).padStart(2,'0')}`;
 await fs.writeFile(path.join(buildDir,stem+'.layout.json'),await(await s.export({format:'layout'})).text());
}
console.log(JSON.stringify({slides:content.slides.length,pptx:finalPptx,pdf:path.join(outputDir,'LineGuide_Proposal.pdf'),previews}));
