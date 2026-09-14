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
    def test_wrong_or_unconfirmed_model_never_calls_ai(self):
        for model,verified in [('Other /99',True),(server.MODEL,False)]:
            c=self.create(model=model,verified=verified)
            with patch.object(server.urllib.request,'urlopen',side_effect=AssertionError('AI must not run')):
                result=server.assess(c,'What should I do?')
            self.assertEqual(result['kind'],'scope');self.assertNotIn('step',result)
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
