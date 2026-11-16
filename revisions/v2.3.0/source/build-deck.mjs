#!/usr/bin/env node
/** Build the editable LineGuide deck from the adjacent versioned JSON source.
 * Requires @oai/artifact-tool 2.8.157. LINEGUIDE_MODULES may point at its
 * configured node_modules directory. PDF conversion follows PPTX validation.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(HERE);
const OUT = path.resolve(process.env.LINEGUIDE_OUT || path.join(ROOT, 'artifact'));
const requireFromRuntime = process.env.LINEGUIDE_MODULES
  ? createRequire(path.join(path.resolve(process.env.LINEGUIDE_MODULES), '__lineguide_runtime.cjs'))
  : createRequire(import.meta.url);
const { Presentation, PresentationFile } = await import(pathToFileURL(requireFromRuntime.resolve('@oai/artifact-tool')).href);
const sourceBytes = await fs.readFile(path.join(HERE, 'deck-content.json'));
const content = JSON.parse(sourceBytes.toString('utf8'));
const P = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const C = { ink: '#0B2133', muted: '#405B68', teal: '#006D77', rule: '#CAD5DB', paper: '#FAFCFC', white: '#FFFFFF' };
const FONT = 'Arial';
await fs.mkdir(OUT, { recursive: true });

function text(s, value, x, y, w, h, size=26, color=C.ink, bold=false, name='text', link=null, background='none') {
  const sh=s.shapes.add({geometry:'textbox', name, position:{left:x,top:y,width:w,height:h}, fill:background, line:{fill:'none',width:0}});
  sh.text=String(value ?? '');
  sh.text.style={typeface:FONT,fontSize:size,color,bold,wrap:'square',autoFit:'none',insets:0,verticalAlignment:'top'};
  if(link)sh.hyperlink={uri:link,isExternal:true};
  return sh;
}
function line(s,x1,y1,x2,y2,{color=C.rule,width=1,dashed=false,arrow=false,name='line'}={}) {
  if(x1===x2&&y1===y2)return null;
  return s.shapes.add({geometry:'connector',kind:'straight',name,position:{left:Math.min(x1,x2),top:Math.min(y1,y2),width:Math.abs(x2-x1),height:Math.abs(y2-y1),horizontalFlip:x2<x1,verticalFlip:y2<y1},line:{fill:color,width,style:dashed?'dashed':'solid'},tail:arrow?{type:'triangle',width:'sm',length:'sm'}:{type:'none'}});
}
function base(d,i){
  const s=P.slides.add();s.background.fill=C.paper;
  if(d.type!=='cover')text(s,d.title,64,38,1152,98,d.titleFontSize||44,C.ink,true,'slide-title');
  line(s,64,660,1216,660);
  text(s,d.footer||'Hypothetical proposal. Proposed targets remain unmeasured.',64,676,1080,24,15,C.muted,false,'footer');
  text(s,String(i+1).padStart(2,'0'),1176,674,40,28,18,C.muted,false,'slide-number');
  return s;
}
function table(s,d){
  const values=[d.headers,...d.rows], top=d.top??156,height=d.height??428,fs=d.fontSize??24;
  const t=s.tables.add({rows:values.length,columns:d.headers.length,left:64,top,width:1152,height,columnWidths:d.widths,values});
  t.borders.assign({fill:C.rule,width:0.75,style:'solid'});
  for(let r=0;r<values.length;r++){
    t.rows[r].height=height/values.length;
    for(let c=0;c<d.headers.length;c++){
      const cell=t.getCell(r,c);
      cell.fill=r===0?C.ink:(r%2?C.white:'#EFF4F5');
      cell.text.style={typeface:FONT,fontSize:fs,color:r===0?C.white:C.ink,bold:r===0,verticalAlignment:'middle',wrap:'square',autoFit:'none',insets:{left:12,right:12,top:7,bottom:7}};
    }
  }
  if(d.caption)text(s,d.caption,64,d.captionTop??610,1152,44,20,C.muted,false,'caption');
}
function rows(s,d){
  const top=d.top??156,gap=d.gap??108;
  for(let j=0;j<d.rows.length;j++){
    text(s,d.rows[j][0],64,top+j*gap,d.labelWidth??290,gap-16,d.labelFontSize??27,C.teal,true,'row-label');
    const dx=d.detailX??380;
    text(s,d.rows[j][1],dx,top+j*gap,1216-dx,gap-16,d.fontSize??26,C.ink,false,'row-detail');
    if(j<d.rows.length-1)line(s,64,top+j*gap+gap-15,1216,top+j*gap+gap-15);
  }
  if(d.caption)text(s,d.caption,64,d.captionTop??608,1152,44,20,C.muted,false,'caption');
}
function two(s,d){
  text(s,d.leftTitle,64,158,530,52,29,C.teal,true,'left-title');
  text(s,d.rightTitle,670,158,546,52,29,C.teal,true,'right-title');
  text(s,d.left,64,226,530,365,d.fontSize??27,C.ink,false,'left-body');
  text(s,d.right,670,226,546,365,d.fontSize??27,C.ink,false,'right-body');
  if(d.caption)text(s,d.caption,64,d.captionTop??611,1152,42,20,C.muted,false,'caption');
}
function diagram(s,d){
  for(const b of d.boundaries||[]){
    s.shapes.add({geometry:'rect',name:'boundary-'+b.label,position:{left:b.x,top:b.y,width:b.w,height:b.h},fill:'none',line:{fill:b.color||C.muted,width:1.25,style:'dashed'}});
    const wraps=b.w<300&&b.label.length>27;
    text(s,b.label,b.x+8,b.y-(wraps?45:27),b.w-16,wraps?42:26,b.fontSize||(b.w<300?16:18),C.muted,true,'boundary-label');
  }
  const nodes=new Map((d.nodes||[]).map(n=>[n.id,n]));
  const center=(n,side)=>({left:[n.x,n.y+n.h/2],right:[n.x+n.w,n.y+n.h/2],top:[n.x+n.w/2,n.y],bottom:[n.x+n.w/2,n.y+n.h]})[side];
  for(const e of d.edges||[]){
    const points=e.points||[center(nodes.get(e.from),e.fromSide||'right'),center(nodes.get(e.to),e.toSide||'left')];
    for(let j=1;j<points.length;j++)line(s,...points[j-1],...points[j],{color:e.color||C.teal,width:e.width||2,dashed:e.dashed,arrow:j===points.length-1,name:'flow-'+e.from+'-'+e.to+'-'+j});
  }
  for(const n of d.nodes||[]){
    const sh=s.shapes.add({geometry:'rect',name:'component-'+n.id,position:{left:n.x,top:n.y,width:n.w,height:n.h},fill:n.fill||C.white,line:{fill:n.color||C.teal,width:1.6}});
    sh.text=n.label;
    sh.text.style={typeface:FONT,fontSize:n.fontSize||23,color:C.ink,bold:n.bold||false,alignment:'center',verticalAlignment:'middle',wrap:'square',autoFit:'none',insets:8};
  }
  for(const e of d.edges||[]){
    if(e.label)text(s,e.label,e.labelX,e.labelY,e.labelW||170,e.labelH||20,e.fontSize||16,C.muted,false,'flow-label',null,C.paper);
  }
  for(const a of d.annotations||[])text(s,a.text,a.x,a.y,a.w,a.h||44,a.fontSize||19,a.color||C.muted,a.bold||false,'diagram-annotation');
  if(d.caption)text(s,d.caption,64,d.captionTop??607,1152,d.captionHeight??44,d.captionFontSize??19,C.ink,false,'diagram-caption');
}
function notes(s,d){
  const sourceIds=d.sources||[];
  const refs=sourceIds.map(id=>{
    const z=content.sources.find(x=>x.id===id);if(!z)throw new Error('Unknown source '+id);
    return `${id}: ${z.title}\n${z.url}\nSource limit: ${z.limit||z.limits?.join(' ')||'See the versioned source register.'}`;
  });
  s.speakerNotes.text=[d.notes||'',`Evidence status: ${d.status||'Design proposal. No operational model test, user study or deployment has been run.'}`,refs.length?'References:\n'+refs.join('\n\n'):''].filter(Boolean).join('\n\n');
}
for(const [i,d] of content.slides.entries()){
  const s=base(d,i);
  if(d.type==='cover'){
    text(s,'LineGuide',64,120,1152,110,80,C.ink,true,'cover-title');
    text(s,d.subtitle||'AI-powered industrial robot\nexpert advisor',64,260,1100,160,48,C.teal,false,'cover-subtitle');
    text(s,d.meta||'',64,494,1100,110,27,C.muted,false,'cover-meta');
  }else if(d.type==='table')table(s,d);
  else if(d.type==='rows')rows(s,d);
  else if(d.type==='two')two(s,d);
  else if(d.type==='diagram')diagram(s,d);
  else if(d.type==='statement'){
    if(d.definitionLabel)text(s,d.definitionLabel,64,148,1152,36,23,C.muted,true,'definition-label');
    text(s,d.statement,64,d.statementTop??174,1140,d.statementHeight??230,d.statementFontSize??42,C.teal,true,'main-statement');
    text(s,d.body,64,d.bodyTop??438,1140,d.bodyHeight??176,d.bodyFontSize??27,C.ink,false,'statement-body');
  }else if(d.type==='sources'){
    for(const [j,id] of d.ids.entries()){
      const z=content.sources.find(x=>x.id===id);if(!z)throw new Error('Unknown source '+id);
      const y=148+j*(d.sourceGap||(d.ids.length>6?70:d.ids.length>5?80:92));
      const titleSize=d.sourceFontSize||(d.ids.length>6?20:d.ids.length>5?22:25);
      text(s,`${id}  ${z.title}`,64,y,1152,36,z.title.length>85?Math.min(titleSize,20):titleSize,C.ink,true,'source-title');
      text(s,z.url,64,y+38,1152,45,z.url.length>150?14:z.url.length>95?16:19,C.teal,false,'source-url',z.url);
    }
  }else throw new Error('Unsupported layout '+d.type);
  notes(s,d);
}
const output=path.join(OUT,'LineGuide_Proposal_v2.3.0.pptx');
await(await PresentationFile.exportPptx(P)).save(output);
console.log(JSON.stringify({output,sourceSha256:createHash('sha256').update(sourceBytes).digest('hex'),pptxSha256:createHash('sha256').update(await fs.readFile(output)).digest('hex'),slides:P.slides.items.length,nativeTableSlides:content.slides.flatMap((s,i)=>s.type==='table'?[i+1]:[]),diagramSlides:content.slides.flatMap((s,i)=>s.type==='diagram'?[i+1]:[]),font:FONT},null,2));
