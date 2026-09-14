'use strict';
const $=id=>document.getElementById(id);const KEY='fixproof-public-case-v1';
const SOURCE='https://media3.bsh-group.com/Documents/9001676154_A.pdf';
const STEPS=[
 {id:'waiting',title:'Allow drying to finish',text:'Let the programme finish, then wait 30 minutes before removing the tableware.',pages:[41]},
 {id:'rinse',title:'Check rinse aid',text:'Check the rinse aid indicator and dosage. Follow page 23 for filling or adjusting it; use only domestic dishwasher rinse aid.',pages:[40,23]},
 {id:'loading',title:'Check pooled water',text:'Where possible, angle items so water can drain from their recesses.',pages:[41]},
 {id:'programme',title:'Check the programme',text:'Check whether the programme includes drying. Shortening options can reduce drying performance.',pages:[40]}
];
let state=null,currentStep=null,recognition=null,listening=false,latest='';
const PERFORMED=['Still wet','Improved, not resolved'];
const esc=s=>String(s||'');
function save(){localStorage.setItem(KEY,JSON.stringify(state));}
function event(role,text){state.events.push({role,text,at:new Date().toISOString()});save();}
function addEvent(item){const row=document.createElement('div');row.className='event '+item.role;const label=document.createElement('strong');label.textContent=item.role==='user'?'YOU':item.role==='record'?'SAVED OUTCOME':'FIXPROOF';const p=document.createElement('p');p.textContent=item.text;row.append(label,p);$('events').append(row);}
function render(){if(!state)return;$('intro').hidden=true;$('workspace').hidden=false;$('case-title').textContent=state.issue;$('events').replaceChildren();state.events.forEach(addEvent);$('events').scrollTop=$('events').scrollHeight;const completed=Object.keys(state.outcomes).length;$('progress').textContent=completed+' of '+STEPS.length+' checks recorded';currentStep=state.pending?STEPS.find(s=>s.id===state.pending):null;$('step').hidden=!currentStep;if(currentStep){$('step-title').textContent=currentStep.title;$('step-text').textContent=currentStep.text;$('citations').replaceChildren(...currentStep.pages.map(p=>{const a=document.createElement('a');a.href=SOURCE+'#page='+p;a.target='_blank';a.rel='noopener';a.textContent='Manual · p. '+p;return a;}));}$('ask').hidden=state.status!=='Open';document.querySelectorAll('[data-prompt]').forEach(button=>button.disabled=state.status!=='Open');$('listen').disabled=state.status!=='Open'||!recognition;$('safety-notice').hidden=!state.safetyReport;renderEvidence();latest=[...state.events].reverse().find(e=>e.role==='assistant')?.text||'';}
function start(issue){state={id:crypto.randomUUID(),created:new Date().toISOString(),issue:issue.trim()||'Plates and glasses are still wet after a wash.',events:[],outcomes:{},pending:null,status:'Open'};event('user',state.issue);if(classify(state.issue)==='hazard'){haltForSafety(state.issue);}else{event('assistant','Case saved. Ask for the first check when you are ready. Only an outcome you explicitly save counts as attempted.');}render();}
function haltForSafety(report){state.stoppedCheck=state.pending||state.stoppedCheck||null;state.pending=null;state.status='Handover ready';state.safetyReport=report;event('assistant','Stop using the appliance and stop troubleshooting. Contact a qualified service provider; use emergency services for immediate danger. No diagnosis has been made.');}
function hazardReport(message){let m=message.toLowerCase();m=m.replace(/\bsmoke\s+test(?:s|ing)?\b|\b(?:no|without)\s+(?:visible\s+)?(?:smoke|sparks?|sparking|leaks?|leaking|flood(?:ed|ing)?|burning(?:\s+(?:smell|odou?r))?|electrical\s+(?:issue|problem|fault|hazard|damage))(?:\s*(?:,|or|and)\s*(?:no\s+)?(?:visible\s+)?(?:smoke|sparks?|sparking|leaks?|leaking|flood(?:ed|ing)?|burning(?:\s+(?:smell|odou?r))?|electrical\s+(?:issue|problem|fault|hazard|damage)))*|\b(?:do\s+not|don['’]t|did\s+not|didn['’]t|cannot|can['’]t)\s+(?:see|smell|notice|observe|find|detect)\s+(?:any\s+)?(?:smoke|sparks?|sparking|leaks?|leaking|flood(?:ed|ing)?|burning(?:\s+(?:smell|odou?r))?)\b|\bthere\s+(?:is|are)\s+no\s+(?:smoke|sparks?|leaks?|leaking|flood(?:ed|ing)?|burning(?:\s+(?:smell|odou?r))?)\b|\bthere\s+(?:isn['’]t|aren['’]t)\s+any\s+(?:smoke|sparks?|leaks?|leaking|flood(?:ed|ing)?|burning(?:\s+(?:smell|odou?r))?)\b/g,' ');return /\b(?:smoke|smoking|burning|burnt|burned|electric shock|sparks?|sparking|arcing|flood(?:ed|ing)?|leaks?|leaking|exposed wir\w*)\b|\belectrical\s+(?:issue|problem|fault|hazard|damage|burn\w*|smell|shock|spark\w*)\b|\bopen\w*.*\b(?:panel|casing)\b|\bbypass\w*.*\b(?:lock|switch)\b/.test(m);}
function classify(message){const m=message.toLowerCase();if(hazardReport(m))return'hazard';if(/\be\d{2}\b|error|drain|pump|won.t start/.test(m))return'unsupported';if(/plastic/.test(m)&&/wet|dry/.test(m))return'plastic';if(/inside|inner wall|tub/.test(m)&&/wet|drop|moist|condens/.test(m))return'interior';if(!/wet|dry|next|check|dish|glass|plate|programme|program|rinse|water/.test(m))return'unclear';return'drying';}
$('start').onsubmit=e=>{e.preventDefault();start($('issue').value)};$('resume').onclick=()=>{state=JSON.parse(localStorage.getItem(KEY));render();};
if(localStorage.getItem(KEY))$('resume').hidden=false;
document.querySelectorAll('[data-prompt]').forEach(button=>button.onclick=()=>{$('question').value=button.dataset.prompt;$('question').focus();});
$('restart').onclick=()=>{localStorage.removeItem(KEY);state=null;location.reload();};
$('ask').onsubmit=e=>{e.preventDefault();const q=$('question').value.trim();if(!q||state.status!=='Open')return;event('user',q);const kind=classify(q);if(kind==='hazard'){haltForSafety(q);}else if(kind==='unsupported'){event('assistant','This verified reference set covers drying only. I cannot establish a supported check for this issue. Add your observations and prepare a handover.');}else if(kind==='plastic'){event('assistant','Plastic retains less heat and can remain wet. The manufacturer manual describes this as normal on page 41.');}else if(kind==='interior'){event('assistant','Moisture on the inner walls is part of condensation drying. The manufacturer manual says no action is required for this condition on page 41.');}else if(kind==='unclear'){event('assistant','Please describe the symptom first. For a drying problem, say what remains wet and whether the programme finished.');}else{const next=STEPS.find(s=>s.id===state.pending)||STEPS.find(s=>!state.outcomes[s.id]);if(next){state.pending=next.id;event('assistant',next.title+'. '+next.text+' Open the linked manual page, then record what happened.');}else{state.status='Handover ready';event('assistant','All four checks have a recorded outcome. Prepare the handover for a service conversation; no fault has been diagnosed.');}}$('question').value='';save();render();};
$('outcome').onsubmit=e=>{e.preventDefault();const result=$('result').value;if(!result||!currentStep||state.status!=='Open')return;const note=$('note').value.trim();state.outcomes[currentStep.id]={result,note,at:new Date().toISOString()};event('record',currentStep.title+' — '+result+(note?'\n'+note:''));state.pending=null;if(classify(note)==='hazard')haltForSafety(note);$('result').value='';$('note').value='';save();render();};
function renderEvidence(){
 const records=Object.values(state.outcomes);
 const performed=records.filter(o=>PERFORMED.includes(o.result)).length;
 $('evidence-summary').textContent=performed+' reported performed · '+(records.length-performed)+' deferred or skipped';
 $('evidence-list').replaceChildren();
 for(const step of STEPS){
  const outcome=state.outcomes[step.id];
  const row=document.createElement('li');
  const name=document.createElement('strong');name.textContent=step.title;
  const status=document.createElement('span');
  status.textContent=state.pending===step.id?'Awaiting your outcome':outcome?outcome.result:state.stoppedCheck===step.id?'Stopped before an outcome':'No outcome recorded';
  row.append(name,status);
  if(outcome){
   const note=document.createElement('p');note.textContent=outcome.note||'No additional observation.';row.append(note);
   if(state.status==='Open'&&!state.pending){
    const revisit=document.createElement('button');revisit.type='button';revisit.className='secondary';revisit.textContent='Update '+step.title.toLowerCase();
    revisit.onclick=()=>{state.pending=step.id;event('record','Reopened '+step.title+' to update the outcome. The earlier record remains in the history.');render();$('step').scrollIntoView({behavior:'smooth',block:'start'});};row.append(revisit);
   }
  }
  $('evidence-list').append(row);
 }
}
function handover(){
 const records=Object.values(state.outcomes),performed=records.filter(o=>PERFORMED.includes(o.result)).length;
 const lines=['# FixProof repair handover','','Hosted Alexa+ workflow simulation · fictional user-reported facts, not a diagnosis.','',`Case: ${state.id}`,`Created: ${state.created}`,`Status: ${state.status}`,'Model: Bosch SMS6HAI02A/01 (fictional evaluation identity)','','## Reported issue',state.issue,'','## Evidence summary',`User reports performed: ${performed}. Deferred or skipped: ${records.length-performed}.`,'Deferred and skipped records do not establish that a check was performed.'];
 for(const [heading,filter] of [['User reports performed',o=>PERFORMED.includes(o.result)],['Deferred or skipped',o=>!PERFORMED.includes(o.result)]]){
  lines.push('','## '+heading);let count=0;
  for(const step of STEPS){const o=state.outcomes[step.id];if(o&&filter(o)){count++;lines.push(`- ${step.title}: ${o.result} (${o.at})`,`  Observation: ${o.note||'No additional observation.'}`,...step.pages.map(p=>`  Source: ${SOURCE}#page=${p}`));}}
  if(!count)lines.push('None recorded.');
 }
 if(state.pending)lines.push('','## Suggested, awaiting outcome',STEPS.find(s=>s.id===state.pending).title,'No outcome has been recorded for this suggestion.');
 if(state.safetyReport)lines.push('','## Safety report',state.safetyReport,'Troubleshooting stopped. No pending check remains; seek qualified help.');
 lines.push('','## Record history',...state.events.filter(e=>e.role==='record').map(e=>`- ${e.at}: ${e.text}`));
 lines.push('','## Reference provenance','Bosch SMS6HAI02A · Australian English user manual','Document 9001676154 (010805) 650 V1 · reference verified 9 September 2026',SOURCE,'https://www.bosch-home.com.au/en/productservice/SMS6HAI02A-01');
 lines.push('','## Unresolved / unverified','No cause or repair requirement has been diagnosed. This hosted build uses a guided sequence; it does not run the local AI implementation.','The physical appliance and model identity were not inspected.');return lines.join('\n')+'\n';
}
$('handover').onclick=()=>{$('handover-text').textContent=handover();$('preview').showModal();};$('close').onclick=()=>$('preview').close();
function download(name,text){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type:'text/markdown'}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
$('download').onclick=()=>download('fixproof-handover.md',handover());
$('feedback').onclick=()=>{const value=$('value').value||'No rating selected';const missing=$('missing').value.trim()||'No written feedback.';download('fixproof-feedback.md',['# FixProof test feedback','',`Compared with manual + notes: ${value}`,'',`Missing or confusing: ${missing}`,'',`Case outcomes recorded: ${Object.keys(state?.outcomes||{}).length}`,'No personal identifier was requested.'].join('\n'));};
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(SR){recognition=new SR();recognition.lang='en-AU';recognition.interimResults=true;recognition.onstart=()=>{listening=true;$('listen').classList.add('listening');$('listen').setAttribute('aria-pressed','true');$('listen').textContent='Listening…';$('voice-status').textContent='Listening. Your words will appear below for review.'};recognition.onresult=e=>{let t='';for(let i=e.resultIndex;i<e.results.length;i++)t+=e.results[i][0].transcript;$('question').value=t.trim();$('voice-status').textContent=e.results[e.results.length-1].isFinal?'Transcript ready. Review it, then press Ask FixProof.':'Listening… '+t.trim();};recognition.onerror=e=>$('voice-status').textContent=e.error==='not-allowed'?'Microphone access was not granted. Type instead.':'Voice input stopped: '+e.error+'. Type instead.';recognition.onend=()=>{listening=false;$('listen').classList.remove('listening');$('listen').setAttribute('aria-pressed','false');$('listen').textContent='● Speak';};$('listen').onclick=()=>listening?recognition.stop():recognition.start();}else{$('listen').disabled=true;$('voice-status').textContent='Voice input is unavailable here. Type your question below.';}
if('speechSynthesis'in window&&'SpeechSynthesisUtterance'in window){$('hear').onclick=()=>{if(!latest)return;$('voice-status').textContent='Reading the latest response aloud.';speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(latest);u.lang='en-AU';u.onend=()=>$('voice-status').textContent='Ready for a typed or spoken question.';speechSynthesis.speak(u);};}else{$('hear').disabled=true;}
