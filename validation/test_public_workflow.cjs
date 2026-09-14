// Application-logic regression tests. This DOM double is not browser or usability QA.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const {webcrypto}=require('node:crypto');
const source=fs.readFileSync(require('node:path').join(__dirname,'../dist/app.js'),'utf8');
function app(saved=new Map()){
 const elements=new Map();
 const element=()=>({value:'',children:[],hidden:false,disabled:false,textContent:'',append(...items){this.children.push(...items)},replaceChildren(...items){this.children=items},focus(){},scrollIntoView(){},showModal(){},close(){},classList:{add(){},remove(){}},setAttribute(){}});
 const get=id=>{if(!elements.has(id))elements.set(id,element());return elements.get(id)};
 const sandbox={document:{getElementById:get,createElement:element,querySelectorAll:()=>[]},window:{},localStorage:{getItem:k=>saved.get(k)||null,setItem:(k,v)=>saved.set(k,v),removeItem:k=>saved.delete(k)},crypto:webcrypto,location:{reload(){}},setTimeout,URL,Blob};
 vm.createContext(sandbox);vm.runInContext(source,sandbox);
 return {get,saved,run:code=>vm.runInContext(code,sandbox),start:()=>sandbox.start('Plates are wet.'),ask:q=>{get('question').value=q;get('ask').onsubmit({preventDefault(){}})},record:(result,note='')=>{get('result').value=result;get('note').value=note;get('outcome').onsubmit({preventDefault(){}})},handover:()=>sandbox.handover()};
}
test('a suggestion is not a performed check; next preserves the pending check',()=>{
 const a=app();a.start();a.ask('first check');a.ask('next');
 assert.equal(a.run('state.pending'),'waiting');assert.match(a.get('evidence-summary').textContent,/0 reported performed/);
 assert.match(a.handover(),/Suggested, awaiting outcome/);
});
test('deferred records remain distinct and can be revisited with history',()=>{
 const a=app();a.start();a.ask('first check');a.record('Not yet tested','Will check later.');
 assert.equal(a.get('evidence-summary').textContent,'0 reported performed · 1 deferred or skipped');
 a.get('evidence-list').children[0].children.find(e=>e.textContent==='Update allow drying to finish').onclick();
 a.record('Still wet','Checked after 30 minutes.');
 assert.equal(a.get('evidence-summary').textContent,'1 reported performed · 0 deferred or skipped');
 assert.match(a.handover(),/Not yet tested/);assert.match(a.handover(),/Checked after 30 minutes/);
});
test('reload restores recorded evidence and excludes it from next suggestions',()=>{
 const a=app();a.start();a.ask('first check');a.record('Still wet','Fictional observation');
 const restored=app(a.saved);restored.get('resume').onclick();restored.ask('next');
 assert.equal(restored.run('state.pending'),'rinse');assert.match(restored.handover(),/Fictional observation/);
});
test('hazards in initial issues, questions and observations stop persisted state',()=>{
 for(const entry of ['initial','question','observation']){
  const a=app();
  if(entry==='initial')a.run("start('Sparks behind the panel.')");
  else{a.start();a.ask('first check');if(entry==='question')a.ask('There is smoke.');else a.record('Not yet tested','There is smoke.');}
  assert.equal(a.run('state.status'),'Handover ready');assert.equal(a.run('state.pending'),null);
  const restored=app(a.saved);restored.get('resume').onclick();
  assert.equal(restored.get('safety-notice').hidden,false);assert.match(restored.handover(),/## Safety report/);
  restored.ask('next');assert.equal(restored.run('state.pending'),null);
 }
});
test('information and clarification preserve a pending suggestion',()=>{
 const a=app();a.start();a.ask('first check');
 for(const q of ['Help me.','Only plastic stays wet.','E24 error']){a.ask(q);assert.equal(a.run('state.pending'),'waiting');}
});
test('all deferred outcomes never become performed checks or a diagnosis',()=>{
 const a=app();a.start();
 for(let i=0;i<4;i++){a.ask('next');a.record(i%2?'Skipped':'Not yet tested');}
 a.ask('next');assert.equal(a.get('evidence-summary').textContent,'0 reported performed · 4 deferred or skipped');
 assert.match(a.handover(),/No cause or repair requirement has been diagnosed/);
});
