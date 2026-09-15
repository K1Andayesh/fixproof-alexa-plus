import json, tempfile, threading, unittest, urllib.request, urllib.error, uuid
from unittest.mock import patch
import server

class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(); server.DATA=server.Path(cls.tmp.name);server.init()
        cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);server.PORT=cls.http.server_port
        threading.Thread(target=cls.http.serve_forever,daemon=True).start()
        cls.url='http://127.0.0.1:'+str(server.PORT)
    @classmethod
    def tearDownClass(cls): cls.http.shutdown();cls.http.server_close();cls.tmp.cleanup()
    def post(self,path,data,origin=None):
        headers={'Content-Type':'application/json'}
        if origin:headers['Origin']=origin
        request=urllib.request.Request(self.url+path,json.dumps(data).encode(),headers)
        try:
            with urllib.request.urlopen(request) as r:return r.status,json.load(r)
        except urllib.error.HTTPError as r:
            with r:return r.code,json.load(r)
    def create(self,**kwargs):
        body=dict(request_id=str(uuid.uuid4()),model=server.MODEL,verified=True,demo=True,issue='Plates are wet.');body.update(kwargs)
        status,c=self.post('/api/create',body);self.assertEqual(status,200);return c
    def action(self,c,**kwargs):return self.post('/api/action',dict(request_id=str(uuid.uuid4()),id=c['id'],revision=c['revision'],**kwargs))
    def test_duplicate_create_and_cross_origin(self):
        body=dict(request_id=str(uuid.uuid4()),model='unknown',issue='wet')
        s,a=self.post('/api/create',body);s,b=self.post('/api/create',body);self.assertEqual(a['id'],b['id'])
        self.assertEqual(self.post('/api/create',body,'https://untrusted.example')[0],403)
    def test_outcome_requires_pending_and_resolution_is_separate(self):
        c=self.create();self.assertEqual(self.action(c,action='outcome',step='waiting',outcome='Still wet')[0],400)
        with patch.object(server,'assess',return_value=dict(kind='step',step='waiting',**server.STEPS['waiting'])):
            _,c=self.action(c,action='chat',message='Next?')
        _,c=self.action(c,action='outcome',step='waiting',outcome='Still wet',note='Still wet after waiting.')
        self.assertEqual(c['status'],'Open');self.assertEqual(c['attempts']['waiting']['outcome'],'Still wet')
        saved=server.read_case(c['id']);self.assertEqual(saved,c)
        export=server.handover(c);self.assertIn('Still wet after waiting.',export);self.assertIn('not been recorded as resolved',export)
        self.assertEqual(self.action(c,action='outcome',step='waiting',outcome='Still wet')[0],400)
    def test_stale_write_rejected(self):
        c=self.create();_,updated=self.action(c,action='status',status='Handover ready')
        self.assertEqual(self.action(c,action='status',status='User reports resolved')[0],409)
        self.assertEqual(server.read_case(c['id'])['status'],'Handover ready')
    def test_explicit_revisit_updates_outcome_and_preserves_history(self):
        c=self.create()
        with patch.object(server,'assess',return_value=dict(kind='step',step='waiting',**server.STEPS['waiting'])):
            _,c=self.action(c,action='chat',message='Next?')
        _,c=self.action(c,action='outcome',step='waiting',outcome='Not yet tested')
        _,c=self.action(c,action='revisit',step='waiting')
        _,c=self.action(c,action='outcome',step='waiting',outcome='Still wet',note='Now checked.')
        self.assertEqual(c['attempts']['waiting']['outcome'],'Still wet')
        self.assertEqual([e['outcome'] for e in c['events'] if e.get('outcome')],['Not yet tested','Still wet'])
    def test_ai_failure_does_not_save_message(self):
        c=self.create()
        with patch.object(server,'assess',side_effect=TimeoutError):self.assertEqual(self.action(c,action='chat',message='Do not lose this')[0],503)
        self.assertEqual(server.read_case(c['id']),c)
    def test_catalog_models_use_their_own_sources_and_unmatched_models_never_call_ai(self):
        for model,verified in [('Other /99',True),(server.MODEL,False)]:
            c=self.create(model=model,verified=verified)
            with patch.object(server.urllib.request,'urlopen',side_effect=AssertionError('AI must not run')):
                result=server.assess(c,'What should I do?')
            self.assertEqual(result['kind'],'scope');self.assertNotIn('step',result)
        def choose_waiting(prompt,context,schema):
            value={'category':'drying'} if 'category' in schema['properties'] else {'step':'waiting'}
            return value,{'model':'stub','prompt_eval_count':1,'eval_count':1}
        for model,pages,document,excluded in [
            ('Bosch SMS6HCI01A/38',[44],'9001720311_B.pdf','9001676154_A.pdf'),
            ('Bosch SMS6HCI02A/72',[42],'9002017246_A.pdf','9001720311_B.pdf')]:
            c=self.create(model=model)
            with patch.object(server,'infer',side_effect=choose_waiting): result=server.assess(c,'What should I check?')
            self.assertEqual(result['pages'],pages);c['pending']='waiting'
            server.record_evidence(c,'waiting','Still wet','Still wet after waiting.')
            export=server.handover(c)
            self.assertIn(document+'#page='+str(pages[0]),export);self.assertNotIn(excluded,export)
    def test_invalid_ai_output_not_executed(self):
        c=self.create()
        class Response:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self):return json.dumps({'message':{'content':'{"category":"drying","step":"invented"}'}}).encode()
        with patch.object(server.urllib.request,'urlopen',return_value=Response()):
            with self.assertRaises(ValueError):server.assess(c,'next')
    def test_hazard_at_creation_stops_even_unknown_model(self):
        for issue in ['Smoke from the door.', 'Burning smell.', 'Water leaking.', 'Sparks behind the panel.', 'Exposed wiring.']:
            with self.subTest(issue=issue), patch.object(server, 'infer', side_effect=AssertionError('No AI needed')):
                c=self.create(issue=issue,model='Unknown',verified=False)
                self.assertEqual(c['status'],'Handover ready')
                self.assertEqual(server.read_case(c['id'])['safety_report'],issue)
                self.assertIsNone(c['pending'])
                self.assertIn(issue,server.handover(c))

    def test_no_hazard_statements_and_technical_phrases_do_not_false_stop(self):
        safe = ['No smoke or burning smell, just wet dishes.', "I don't see any smoke.",
                'There is no leaking.', 'The smoke test passed.', 'No electrical problem was found.']
        for report in safe:
            with self.subTest(report=report): self.assertFalse(server.hazard_report(report))
        hazardous = ['No smoke, but water is leaking.', 'The smoke test found smoke.',
                     'There is an electrical fault.', 'Sparks behind the panel.']
        for report in hazardous:
            with self.subTest(report=report): self.assertTrue(server.hazard_report(report))
        c=self.create(issue='No smoke or burning smell, just wet dishes.')
        seen=[]
        def classify_without_ai_hazard(prompt,context,schema):
            seen.append(context)
            value='drying' if 'category' in schema['properties'] else 'waiting'
            return ({next(iter(schema['properties'])):value},{'model':'test','prompt_eval_count':0,'eval_count':0})
        with patch.object(server,'infer',side_effect=classify_without_ai_hazard):
            reply=server.assess(c,'The smoke test passed. What should I check next?')
        self.assertEqual(reply['kind'],'step')
        self.assertNotIn('smoke',json.dumps(seen).lower())

    def test_pending_hazard_stops_without_ai_and_cannot_reopen(self):
        c=self.create()
        with patch.object(server,'assess',return_value=dict(kind='step',step='waiting',**server.STEPS['waiting'])):
            _,c=self.action(c,action='chat',message='Next?')
        with patch.object(server,'infer',side_effect=TimeoutError('Offline')):
            status,c=self.action(c,action='chat',message='There is smoke.')
        self.assertEqual(status,200);self.assertIsNone(c['pending']);self.assertEqual(c['attempts'],{})
        for action in [dict(action='status',status='Open'),dict(action='status',status='User reports resolved'),dict(action='outcome',step='waiting',outcome='Still wet'),dict(action='chat',message='next')]:
            self.assertEqual(self.action(c,**action)[0],400)
        self.assertEqual(server.read_case(c['id']),c)

    def test_hazard_in_outcome_observation_stops_and_keeps_record(self):
        c=self.create()
        with patch.object(server,'assess',return_value=dict(kind='step',step='waiting',**server.STEPS['waiting'])):
            _,c=self.action(c,action='chat',message='Next?')
        _,c=self.action(c,action='outcome',step='waiting',outcome='Still wet',note='Still wet; also an electrical smell.')
        self.assertEqual(c['status'],'Handover ready');self.assertEqual(c['attempts']['waiting']['outcome'],'Still wet')
        self.assertIn('## Safety report',server.handover(c));self.assertIsNone(c['pending'])

    def test_model_detected_hazard_persists_stop(self):
        c=self.create()
        with patch.object(server,'infer',return_value=({'category':'hazard'},{'model':'stub'})):
            _,c=self.action(c,action='chat',message='The appliance casing gives me a tingle.')
        self.assertEqual(c['status'],'Handover ready');self.assertIn('tingle',c['safety_report'])

    def test_information_preserves_pending_check(self):
        c=self.create()
        with patch.object(server,'assess',return_value=dict(kind='step',step='waiting',**server.STEPS['waiting'])):
            _,c=self.action(c,action='chat',message='Next?')
        for kind in ['info','scope','clarify']:
            with self.subTest(kind=kind),patch.object(server,'assess',return_value=dict(kind=kind,text='Information only.')):
                _,c=self.action(c,action='chat',message='A follow-up question')
                self.assertEqual(c['pending'],'waiting');self.assertEqual(c['attempts'],{})

    def test_pending_followup_does_not_select_a_new_check(self):
        c=self.create();c['pending']='waiting'
        with patch.object(server,'infer',return_value=({'category':'drying'},{'model':'stub'})) as infer:
            reply=server.assess(c,'What next?')
        self.assertEqual(reply['step'],'waiting');self.assertEqual(infer.call_count,1)

    def test_food_remnant_flow_uses_only_source_backed_food_steps(self):
        c=self.create(issue='Food remains on the plates after the wash.')
        seen=[]
        def choose_food(prompt,context,schema):
            raw={'model':'stub','prompt_eval_count':1,'eval_count':1}
            if 'category' in schema['properties']: return {'category':'food'},raw
            seen.append(context['available_checks'])
            return {'step':'food_spacing'},raw
        with patch.object(server,'infer',side_effect=choose_food):
            reply=server.assess(c,'What should I check first?')
        self.assertEqual(reply['kind'],'step');self.assertEqual(reply['step'],'food_spacing')
        self.assertEqual(reply['pages'],[42])
        self.assertTrue(seen)
        self.assertEqual(set(seen[0]),{'food_spacing','food_spray_arm','food_filters','food_programme'})
        c['pending']='food_spacing';server.record_evidence(c,'food_spacing','Issue unchanged','Food still remains.')
        self.assertEqual(c['attempts']['food_spacing']['outcome'],'Issue unchanged')

    def test_detergent_residue_flow_uses_only_source_backed_detergent_steps(self):
        c=self.create(issue='Detergent residue remains inside the appliance.')
        seen=[]
        def choose_detergent(prompt,context,schema):
            raw={'model':'stub','prompt_eval_count':1,'eval_count':1}
            if 'category' in schema['properties']: return {'category':'detergent'},raw
            seen.append(context['available_checks'])
            return {'step':'detergent_tray'},raw
        with patch.object(server,'infer',side_effect=choose_detergent):
            reply=server.assess(c,'What should I check first?')
        self.assertEqual(reply['kind'],'step');self.assertEqual(reply['step'],'detergent_tray')
        self.assertEqual(reply['pages'],[42])
        self.assertEqual(set(seen[0]),{'detergent_tray','detergent_position'})

    def test_removable_streak_flow_uses_only_source_backed_streak_steps(self):
        c=self.create(issue='Removable streaks remain on glasses and cutlery.')
        seen=[]
        def choose_streaks(prompt,context,schema):
            raw={'model':'stub','prompt_eval_count':1,'eval_count':1}
            if 'category' in schema['properties']: return {'category':'streaks'},raw
            seen.append(context['available_checks'])
            return {'step':'streaks_rinse_setting'},raw
        with patch.object(server,'infer',side_effect=choose_streaks):
            reply=server.assess(c,'What should I check first?')
        self.assertEqual(reply['kind'],'step');self.assertEqual(reply['step'],'streaks_rinse_setting')
        self.assertEqual(reply['pages'],[44])
        self.assertEqual(set(seen[0]),{'streaks_rinse_setting','streaks_add_rinse_aid','streaks_tray','streaks_prerinse'})

    def test_wash_noise_flow_uses_only_visually_verified_noise_steps(self):
        c=self.create(issue='There is a knocking or rattling noise during the wash.')
        seen=[]
        def choose_noise(prompt,context,schema):
            raw={'model':'stub','prompt_eval_count':1,'eval_count':1}
            if 'category' in schema['properties']: return {'category':'noise'},raw
            seen.append(context['available_checks'])
            return {'step':'noise_spray_arm'},raw
        with patch.object(server,'infer',side_effect=choose_noise):
            reply=server.assess(c,'What should I check first?')
        self.assertEqual(reply['kind'],'step');self.assertEqual(reply['step'],'noise_spray_arm')
        self.assertEqual(reply['pages'],[48])
        self.assertEqual(set(seen[0]),{'noise_spray_arm','noise_load_distribution','noise_light_items'})
        third=server.steps_for('Bosch SMS6HCI02A/72')
        self.assertEqual(third['noise_spray_arm']['pages'],[49])
        self.assertEqual(third['noise_light_items']['pages'],[50])

    def test_cutlery_rust_flow_uses_only_visually_verified_rust_steps(self):
        c=self.create(issue='Rust spots appear on the cutlery after the wash.')
        seen=[]
        def choose_rust(prompt,context,schema):
            raw={'model':'stub','prompt_eval_count':1,'eval_count':1}
            if 'category' in schema['properties']: return {'category':'rust'},raw
            seen.append(context['available_checks'])
            return {'step':'rust_resistant_tableware'},raw
        with patch.object(server,'infer',side_effect=choose_rust):
            reply=server.assess(c,'What should I check first?')
        self.assertEqual(reply['kind'],'step');self.assertEqual(reply['step'],'rust_resistant_tableware')
        self.assertEqual(reply['pages'],[45])
        self.assertEqual(set(seen[0]),{'rust_resistant_tableware','rust_remove_rusting_items'})
        self.assertEqual(server.steps_for('Bosch SMS6HCI01A/38')['rust_resistant_tableware']['pages'],[49])
        self.assertEqual(server.steps_for('Bosch SMS6HCI02A/72')['rust_remove_rusting_items']['pages'],[46])

    def test_irreversible_clouding_flow_is_distinct_from_removable_streaks(self):
        c=self.create(issue='Clouding on the glassware does not wipe off after the wash.')
        seen=[]
        def choose_clouding(prompt,context,schema):
            raw={'model':'stub','prompt_eval_count':1,'eval_count':1}
            if 'category' in schema['properties']: return {'category':'clouding'},raw
            seen.append(context['available_checks'])
            return {'step':'clouding_dishwasher_proof'},raw
        with patch.object(server,'infer',side_effect=choose_clouding):
            reply=server.assess(c,'What should I check first?')
        self.assertEqual(reply['kind'],'step');self.assertEqual(reply['step'],'clouding_dishwasher_proof')
        self.assertEqual(reply['pages'],[45])
        self.assertEqual(set(seen[0]),{'clouding_dishwasher_proof','clouding_steam_phase','clouding_lower_temperature','clouding_glass_protection'})
        self.assertEqual(server.steps_for('Bosch SMS6HCI01A/38')['clouding_lower_temperature']['pages'],[49])
        self.assertEqual(server.steps_for('Bosch SMS6HCI02A/72')['clouding_glass_protection']['pages'],[46])

    def test_switching_supported_path_does_not_erase_pending_check(self):
        c=self.create();c['pending']='waiting'
        with patch.object(server,'infer',return_value=({'category':'food'},{'model':'stub'})) as infer:
            reply=server.assess(c,'There is also food left on the plates.')
        self.assertEqual(reply['kind'],'clarify');self.assertNotIn('step',reply)
        self.assertEqual(c['pending'],'waiting');self.assertEqual(infer.call_count,1)

    def test_handover_separates_performed_deferred_and_pending(self):
        c=self.create();c['pending']='loading'
        for step,outcome in [('waiting','Still wet'),('rinse_aid','Not yet tested'),('programme','Skipped')]:
            c['attempts'][step]=dict(outcome=outcome,note='',at=server.now())
        text=server.handover(c)
        self.assertIn('User reports performed: 1. Deferred or skipped: 2.',text)
        self.assertIn('Suggested but not recorded as attempted: Check pooled water',text)
        self.assertIn('not been recorded as resolved',text)

    def test_repeat_check_filtered_at_server(self):
        c=self.create();c['attempts']['waiting']={'outcome':'Still wet','note':'','at':server.now()}
        class Response:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self):return json.dumps({'model':'test','message':{'content':'{"category":"drying","step":"waiting"}'}}).encode()
        with patch.object(server.urllib.request,'urlopen',return_value=Response()):
            with self.assertRaises(ValueError):server.assess(c,'next')

if __name__=='__main__':unittest.main()
