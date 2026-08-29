"""Isolated HTTP boundary tests; no optimizer or credentials required."""
import http.client
import json
from pathlib import Path
import threading
import unittest

from serve import App, Handler, ThreadingHTTPServer
from runtime_worker import portable, validate_pipeline, ORDER


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = App(Path('/tmp'), 'python3')
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.server.app = cls.app
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.app.pool.shutdown()
        cls.thread.join()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        connection.request(method, path, body, headers or {})
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return response.status, data

    def test_state_and_static(self):
        self.assertEqual(self.request('GET', '/local/state')[0], 200)
        self.assertEqual(self.request('GET', '/workbench/')[0], 200)
        self.assertEqual(self.request('GET', '/resources/')[0], 200)

    def test_private_paths(self):
        for path in ['/workbench/serve.py', '/.git/config', '/docs/V0.2_SERVICE_SCOPE.md', '/extensions/../DESIGN.md', '/extensions/%2e%2e/DESIGN.md']:
            self.assertEqual(self.request('GET', path)[0], 404)
        self.assertEqual(self.request('HEAD', '/workbench/serve.py')[0], 405)

    def test_origin_host_csrf(self):
        self.assertEqual(self.request('GET', '/local/state', headers={'Origin':'https://external.invalid'})[0], 403)
        self.assertEqual(self.request('GET', '/local/state', headers={'Host':'external.invalid'})[0], 403)
        self.assertEqual(self.request('POST', '/local/run', '{}', {'Content-Type':'application/json'})[0], 403)

    def test_validation(self):
        headers={'Content-Type':'application/json','X-Workbench-Token':self.app.token}
        self.assertEqual(self.request('POST','/local/run','{',headers)[0],400)
        self.assertEqual(self.request('POST','/local/run',json.dumps({'dataset':'unknown'}),headers)[0],400)
        self.assertEqual(self.request('POST','/local/run',json.dumps({'dataset':'production_planning','pipeline':['shell']}),headers)[0],400)
        self.assertEqual(self.request('POST','/local/run','[]',headers)[0],400)

    def test_pipeline(self):
        self.assertEqual(validate_pipeline(ORDER),ORDER)
        for value in [[], ORDER[::-1], ORDER+ORDER[:1], ['exec'], [3]]:
            with self.assertRaises(ValueError):validate_pipeline(value)

    def test_portable(self):
        self.assertEqual(portable({'source':'/tmp/app/DataSets/data.db','_recipe_path':'x'},Path('/tmp/app')),{'source':'DataSets/data.db'})


if __name__ == '__main__':
    unittest.main()
