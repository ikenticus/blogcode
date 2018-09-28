'''
    tester: contains all the unit tests
'''
import config
import json
import reader
import unittest

class TestRolodex(unittest.TestCase):

    def test_parser(self):
        for t in config.parse_tests:
            got = reader.parse(t['line'])
            self.assertEqual(got, t['want'])

    def test_reader(self):
        got = reader.read('data.in')
        self.assertIsNotNone(got)
        self.assertIsInstance(got['entries'], list)
        self.assertIsInstance(got['errors'], list)
        self.assertTrue(len(got['entries']) > 0)
        self.assertTrue(len(got['errors']) > 0)

    def test_writer(self):
        filename = 'test.json'
        reader.write(config.write_output, filename)
        data = json.loads(open(filename).read())
        for t in config.write_tests:
            got = data['entries'][0][t['key']]
            self.assertEqual(got, t['want'])

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRolodex)
    unittest.TextTestRunner(verbosity=2).run(suite)
