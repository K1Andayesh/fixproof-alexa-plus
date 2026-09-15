// Application-logic regression tests. This DOM double is not browser or usability QA.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const {webcrypto}=require('node:crypto');
const source=fs.readFileSync(require('node:path').join(__dirname,'../dist/app.js'),'utf8');
const page=fs.readFileSync(require('node:path').join(__dirname,'../dist/index.html'),'utf8');
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
test('explicit no-hazard statements and technical phrases do not false stop',()=>{
 for(const report of ['No smoke or burning smell, just wet dishes.',"I don't see any smoke.",'The smoke test passed.']){
  const a=app();a.run(`start(${JSON.stringify(report)})`);assert.equal(a.run('state.status'),'Open');
 }
 for(const report of ['No smoke, but water is leaking.','The smoke test found smoke.']){
  const a=app();a.run(`start(${JSON.stringify(report)})`);assert.equal(a.run('state.status'),'Handover ready');
 }
});
test('information and clarification preserve a pending suggestion',()=>{
 const a=app();a.start();a.ask('first check');
 for(const q of ['Help me.','Only plastic stays wet.','E24 error']){a.ask(q);assert.equal(a.run('state.pending'),'waiting');}
 const b=app();b.run("start('Plates are wet.','drying','Bosch SMS6HCI02A/72')");b.ask('Only plastic stays wet.');
 assert.match(b.run('latest'),/page 42/);
});
test('all deferred outcomes never become performed checks or a diagnosis',()=>{
 const a=app();a.start();
 for(let i=0;i<4;i++){a.ask('next');a.record(i%2?'Skipped':'Not yet tested');}
 a.ask('next');assert.equal(a.get('evidence-summary').textContent,'0 reported performed · 4 deferred or skipped');
 assert.match(a.handover(),/No cause or repair requirement has been diagnosed/);
});
test('food-remnant journey stays within its four cited checks',()=>{
 const a=app();a.run("start('Food remnants remain on plates after the wash.','food')");a.ask('What should I check first?');
 assert.equal(a.run('state.pending'),'food_spacing');assert.match(a.get('progress').textContent,/0 of 4 food-remnant checks/);
 a.record('Issue unchanged','Food still remains.');assert.match(a.get('evidence-summary').textContent,/1 reported performed/);
 assert.match(a.handover(),/Supported path: food remnants/);assert.match(a.handover(),/Issue unchanged/);
});
test('detergent-residue journey stays within its two cited checks',()=>{
 const a=app();a.run("start('Detergent residue remains inside the appliance.','detergent')");a.ask('What should I check first?');
 assert.equal(a.run('state.pending'),'detergent_tray');assert.match(a.get('progress').textContent,/0 of 2 detergent-residue checks/);
 a.record('Issue unchanged','Detergent residue remains.');
 assert.match(a.handover(),/Supported path: detergent residue/);assert.match(a.handover(),/Manual · p. 42|page=42/);
 const b=app();b.run("start('Detergent residue remains inside the appliance.','detergent','Bosch SMS6HCI01A/38')");b.ask('What should I check first?');b.record('Issue unchanged','Residue remains.');
 assert.match(b.handover(),/9001720311_B\.pdf#page=46/);assert.doesNotMatch(b.handover(),/9001676154_A\.pdf/);
 const c=app();c.run("start('Detergent residue remains inside the appliance.','detergent','Bosch SMS6HCI02A/72')");c.ask('What should I check first?');c.record('Issue unchanged','Residue remains.');
 assert.match(c.handover(),/9002017246_A\.pdf#page=43/);assert.doesNotMatch(c.handover(),/9001720311_B\.pdf/);
});
test('removable-streak journey stays within its four cited checks',()=>{
 const a=app();a.run("start('Removable streaks remain on glasses and cutlery.','streaks')");a.ask('What should I check first?');
 assert.equal(a.run('state.pending'),'streaks_rinse_setting');assert.match(a.get('progress').textContent,/0 of 4 removable-streak checks/);
 a.record('Issue unchanged','Streaks remain on the glasses.');
 assert.match(a.handover(),/Supported path: removable streaks/);assert.match(a.handover(),/Manual · p. 44|page=44/);
});
test('wash-noise journey stays within its three cited checks',()=>{
 const a=app();a.run("start('There is a knocking or rattling noise during the wash.','noise','Bosch SMS6HCI02A/72')");a.ask('What should I check first?');
 assert.equal(a.run('state.pending'),'noise_spray_arm');assert.match(a.get('progress').textContent,/0 of 3 wash-noise checks/);
 a.record('Issue unchanged','The knocking remains.');
 assert.match(a.handover(),/Supported path: knocking or rattling during the wash/);assert.match(a.handover(),/9002017246_A\.pdf#page=49/);
});
test('cutlery-rust journey stays within its two cited checks',()=>{
 const a=app();a.run("start('Rust spots appear on the cutlery after the wash.','rust','Bosch SMS6HCI02A/72')");a.ask('What should I check first?');
 assert.equal(a.run('state.pending'),'rust_resistant_tableware');assert.match(a.get('progress').textContent,/0 of 2 cutlery-rust checks/);
 a.record('Issue unchanged','Rust spots remain.');
 assert.match(a.handover(),/Supported path: rust spots on cutlery/);assert.match(a.handover(),/9002017246_A\.pdf#page=46/);
});
test('irreversible-glass-clouding journey stays distinct from removable streaks',()=>{
 const a=app();a.run("start('Clouding on glassware does not wipe off.','clouding','Bosch SMS6HCI02A/72')");a.ask('What should I check first?');
 assert.equal(a.run('state.pending'),'clouding_dishwasher_proof');assert.match(a.get('progress').textContent,/0 of 4 irreversible-glass-clouding checks/);
 a.record('Issue unchanged','The clouding does not wipe off.');
 assert.match(a.handover(),/Supported path: irreversible clouding of glassware/);assert.match(a.handover(),/9002017246_A\.pdf#page=46/);
});

test('a cross-path request does not replace a pending check',()=>{
 const a=app();a.start();a.ask('first check');a.ask('There is also food left on the plates.');
 assert.equal(a.run('state.pending'),'waiting');assert.match(a.run('latest'),/Start a new fictional case/);
 const b=app();b.run("start('Food remnants remain on plates after the wash.','food')");b.ask('first check');b.ask('The dishes are also wet.');
 assert.equal(b.run('state.pending'),'food_spacing');assert.match(b.run('latest'),/Start a new fictional case/);
});
test('the public evaluation page links to the callable MCP deployment',()=>{
 assert.match(page,/https:\/\/fixproof-mcp\.keyvan-andayesh\.chatgpt\.site\//);
 assert.match(page,/fictional-only input/);
 assert.match(page,/official TypeScript SDK 2\.0\.0 plus D1 continuity/);
});
