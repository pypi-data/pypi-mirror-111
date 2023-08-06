import os
import sys
import unittest
from genie.conf.base.device import Device
from genie.conf.base.api import ExtendApis


class TestApi(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='iosxe',
                             custom={'abstraction': {'order':['os']}})

    def test_api_success(self):
        api = self.device.api.get_api('shut_interface', self.device)
        self.assertEqual(callable(api), True)
        self.assertEqual(api.__name__, 'shut_interface')

    def test_api_exception(self):
        with self.assertRaises(AttributeError):
            api = self.device.api.get_api('DontExists', self.device)

class TestExtendApi(unittest.TestCase):

    def setUp(self):
        sys.path.append(os.path.dirname(__file__))

    def test_extend_api(self):
        ext = ExtendApis('dummy_api')
        ext.extend()
        summary = ext.output['extend_info']

        self.assertEqual(len(summary), 2)
        self.assertIn("api name: 'dummy_iosxe', tokens ['iosxe'], "
                      "module name: utils",
                      summary)
        self.assertIn("api name: 'dummy_common', tokens ['com'], "
                      "module name: utils",
                      summary)


if __name__ == '__main__':
    unittest.main()
