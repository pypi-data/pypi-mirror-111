# -*- coding: utf-8 -*-
import os
import unittest
from ..debinterface import InterfacesReader


INF_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces.txt")
INF2_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces2.txt")
INF3_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces3.txt")
INF4_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces4.txt")
INF5_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces5.txt")  # source interfaces2.txt


class TestInterfacesReader(unittest.TestCase):
    def test_parse_interfaces_count(self):
        # type: ()->None
        """Should have 9 adapters"""

        nb_adapters = 10
        reader = InterfacesReader(INF_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), nb_adapters)

    def test_parse_interfaces1(self):
        # type: ()->None
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF_PATH)
        for adapter in reader.parse_interfaces():
            adapter.validateAll()

    def test_parse_interfaces1_comments(self):
        # type: ()->None
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF_PATH)
        adapters = reader.parse_interfaces(read_comments=True)
        for adapter in adapters:
            adapter.validateAll()
        expected_comment = ('# Used by ifup(8) and ifdown(8). See the interfaces(5) manpage or\n'
                            '# /usr/share/doc/ifupdown/examples for more information.\n')
        self.assertEqual(expected_comment, reader.header_comments)

    def test_parse_interfaces2(self):
        # type: ()->None
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF2_PATH)
        for adapter in reader.parse_interfaces():
            adapter.validateAll()

    def test_parse_interfaces2_comments(self):
        # type: ()->None
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF2_PATH)
        adapters = reader.parse_interfaces(read_comments=True)
        for adapter in adapters:
            adapter.validateAll()
        self.assertEqual('# The primary network interface\n', reader.header_comments)

    def test_dnsnameservers_not_unknown(self):
        # type: ()->None
        """All adapters should validate"""
        reader = InterfacesReader(INF_PATH)
        eth1 = next(
            (x for x in reader.parse_interfaces() if x.attributes['name'] == "eth1"),
            None
        )
        self.assertNotEqual(eth1, None)
        self.assertEqual(eth1.attributes["dns-nameservers"], ["8.8.8.8"])  # type: ignore

    def test_dnssearch_not_unknown(self):
        # type: ()->None
        """dns-search should be found."""
        reader = InterfacesReader(INF_PATH)
        eth2 = next(
            (x for x in reader.parse_interfaces() if x.attributes['name'] == "eth2"),
            None
        )
        self.assertNotEqual(eth2, None)
        self.assertEqual(eth2.attributes['dns-search'], ['mydomain.com', 'myotherdomain.com'])  # type: ignore
        self.assertEqual(eth2.attributes['dns-nameservers'], ['172.16.1.1', '172.16.1.2'])  # type: ignore

    def test_interfaces2(self):
        # type: ()->None
        """All adapters should validate"""
        reader = InterfacesReader(INF2_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), 2)
        for adapter in adapters:
            adapter.validateAll()
        self.assertEqual(adapters[0].attributes, {
            'addrFam': 'inet',
            'broadcast': '192.168.0.255',
            'name': 'eth0',
            'auto': True,
            'bridge-opts': {},
            'up': ['ethtool -s eth0 wol g'],
            'gateway': '192.168.0.254',
            'down': [],
            'source': 'static',
            'netmask': '255.255.255.0',
            'address': '192.168.0.250',
            'pre-up': [],
            'post-down': [],
            'post-up': [],
            'pre-down': []
        })

    def test_multiDns_read(self):
        # type: ()->None
        """All adapters should validate"""
        reader = InterfacesReader(INF2_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), 2)
        for adapter in adapters:
            adapter.validateAll()
        self.assertEqual(adapters[1].attributes, {
            'addrFam': 'inet',
            'name': 'eth2',
            'source': 'static',
            'bridge-opts': {},
            'dns-nameservers': ['8.8.8.8', '8.8.4.4', '4.2.2.2'],
            'dns-search': ['mydomain.com', 'myotherdomain.com'],
            'netmask': '255.255.255.0',
            'address': '10.1.20.10',
            'up': [],
            'down': [],
            'pre-up': [],
            'pre-down': [],
            'post-up': [],
            'post-down': []
        })

    def test_read_comments_no_space(self):
        # type: ()->None
        """Comments at the top of file should all be returned."""
        reader = InterfacesReader(INF_PATH)
        reader.parse_interfaces(read_comments=True)
        expected = ('# Used by ifup(8) and ifdown(8). See the interfaces(5) manpage or\n'
                    '# /usr/share/doc/ifupdown/examples for more information.\n')
        self.assertEqual(expected, reader.header_comments)

    def test_read_comments_no_comments(self):
        # type: ()->None
        """Comments at the top of file should all be returned."""
        reader = InterfacesReader(INF4_PATH)
        adapters = reader.parse_interfaces(read_comments=True)
        self.assertEqual('', reader.header_comments)
        self.assertEqual(adapters[0].attributes, {'addrFam': 'inet',
                                                  'auto': True,
                                                  'bridge-opts': {},
                                                  'down': [],
                                                  'name': 'lo',
                                                  'post-down': [],
                                                  'post-up': [],
                                                  'pre-down': [],
                                                  'pre-up': [],
                                                  'source': 'loopback',
                                                  'up': []})

    def test_read_comments_space(self):
        # type: ()->None
        """Comments at the top of file should all be returned."""
        reader = InterfacesReader(INF3_PATH)
        adapters = reader.parse_interfaces(read_comments=True)
        expected = ('# This is a comment block\n'
                    '# That contains a space after it\n'
                    '# before starting parsing any interfaces information.\n')
        self.assertEqual(expected, reader.header_comments)
        self.assertEqual(adapters[0].attributes, {'addrFam': 'inet',
                                                  'auto': True,
                                                  'bridge-opts': {},
                                                  'down': [],
                                                  'name': 'lo',
                                                  'post-down': [],
                                                  'post-up': [],
                                                  'pre-down': [],
                                                  'pre-up': [],
                                                  'source': 'loopback',
                                                  'up': []})

    def test_read_wpa_conf(self):
        # type: ()->None
        reader = InterfacesReader(INF_PATH)
        wlan2 = next(
            (x for x in reader.parse_interfaces() if x.attributes['name'] == 'wlan2'),
            None
        )
        self.assertEqual(wlan2.attributes['wpa-conf'], '/etc/wpa_supplicant/wpa_supplicant.conf')  # type: ignore

    def test_source_other_file(self):
        # type: ()->None
        """Load two adapters in main file and 2 others in a sourced file"""

        reader = InterfacesReader(INF5_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), 4)
        for adapter in adapters:
            adapter.validateAll()
        self.assertEqual(adapters[0].attributes["name"], "eth_main_file_1")  # before the source
        self.assertEqual(adapters[1].attributes["name"], "eth0")  # in the sourced file
        self.assertEqual(adapters[2].attributes["name"], "eth2")  # in the sourced file
        self.assertEqual(adapters[3].attributes["name"], "eth_main_file_2")   # after the source

        #  Check paths
        self.assertEqual(adapters[0].interfaces_path, INF5_PATH)  # before the source
        self.assertEqual(adapters[1].interfaces_path, INF2_PATH)  # in the sourced file
        self.assertEqual(adapters[2].interfaces_path, INF2_PATH)  # in the sourced file
        self.assertEqual(adapters[3].interfaces_path, INF5_PATH)  # before the source

    def test_attrs_with_spaces(self):
        # type: ()->None
        reader = InterfacesReader(INF_PATH)
        eth1 = next(
            (x for x in reader.parse_interfaces() if x.attributes['name'] == 'eth1'),
            None
        )
        self.assertIsNotNone(eth1)
        self.assertEqual(eth1.attributes, {  # type: ignore
            'bridge-opts': {},
            'up': ['ls -la', 'another command on up', 'up up up up up up'],
            'down': ['I am root'],
            'pre-up': [],
            'pre-down': [],
            'post-up': [],
            'post-down': [],
            'name': 'eth1',
            'source': 'static',
            'addrFam': 'inet',
            'address': '10.1.20.1',
            'netmask': '255.255.255.0',
            'dns-nameservers': ['8.8.8.8'],
            'unknown': {'some-attr': 'value contains space\ttab_underscore-dash'}
        })
