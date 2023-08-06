# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement, absolute_import
import os
import unittest
import tempfile
from ..debinterface import InterfacesWriter, NetworkAdapter


INF_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces.txt")


class TestInterfacesWriter(unittest.TestCase):
    def compare_iterface_with_expected(self, content_text, expected, number_of_stict_lines=2):
        # type: (str, tp.List[str], int)->None

        content = list(map(lambda x: x.strip(), content_text.strip().split("\n")))

        self.assertEqual(len(content), len(expected), "\n".join(content))
        for i in range(number_of_stict_lines):
            self.assertEqual(content[i], expected[i])

        content = list(filter(lambda x: x, content))
        for line_written, line_expected in zip(sorted(content[number_of_stict_lines:]), sorted(expected[number_of_stict_lines:])):
            self.assertEqual(line_written, line_expected)

    def test_write_complete(self):
        # type: ()->None
        """Should work"""

        options = {
            'addrFam': 'inet',
            'broadcast': '192.168.1.255',
            'name': 'eth0.99',
            'auto': True,
            'bridge-opts': {'ports': 'eth0 ath0 ath1'},
            'up': [
                'ifconfig ath0 down ; ifconfig ath0 up # this is a workaround',
                'iwpriv ath1 wds 1',
                'iwpriv ath1 wds_add AA:BB:CC:DD:EE:FF',
                'ifconfig ath1 down ; ifconfig ath1 up # this is a workaround'],
            'gateway': '192.168.1.1',
            'down': ["cp /etc/badaboum /etc/bigbadaboum"],
            'source': 'static',
            'netmask': '255.255.255.0',
            'address': '192.168.1.2',
            'pre-up': [
                'wlanconfig ath0 create wlandev wifi0 wlanmode ap',
                'wlanconfig ath1 create wlandev wifi0 wlanmode wds',
                'iwpriv ath0 mode 11g',
                'iwpriv ath0 bintval 1000',
                'iwconfig ath0 essid "voyage-wds" channel 1'
            ],
            'pre-down': ['ls poufff'],
            'post-down': ['wlanconfig ath0 destroy', 'wlanconfig ath1 destroy'],
            'network': '192.168.1.0',
            'unknown': {
                'wireless-mode': 'Ad-hoc',
                'wireless-channel': '1',
                'madwifi-base': 'wifi0',
                'wireless-essid': 'voyage-adhoc'
            }
        }

        expected = [
            "auto eth0.99",
            "iface eth0.99 inet static",
            "address 192.168.1.2",
            "network 192.168.1.0",
            "netmask 255.255.255.0",
            "broadcast 192.168.1.255",
            "gateway 192.168.1.1",
            "bridge_ports eth0 ath0 ath1",
            "pre-up wlanconfig ath0 create wlandev wifi0 wlanmode ap",
            "pre-up wlanconfig ath1 create wlandev wifi0 wlanmode wds",
            "pre-up iwpriv ath0 mode 11g",
            "pre-up iwpriv ath0 bintval 1000",
            """pre-up iwconfig ath0 essid "voyage-wds" channel 1""",
            "up ifconfig ath0 down ; ifconfig ath0 up # this is a workaround",
            "up iwpriv ath1 wds 1",
            "up iwpriv ath1 wds_add AA:BB:CC:DD:EE:FF",
            "up ifconfig ath1 down ; ifconfig ath1 up # this is a workaround",
            "down cp /etc/badaboum /etc/bigbadaboum",
            "pre-down ls poufff",
            "post-down wlanconfig ath0 destroy",
            "post-down wlanconfig ath1 destroy",
            "wireless-essid voyage-adhoc",
            "wireless-channel 1",
            "wireless-mode Ad-hoc",
            "madwifi-base wifi0"
        ]

        with tempfile.NamedTemporaryFile() as tempf:
            adapter = NetworkAdapter(options={}, interfaces_path=tempf.name)
            adapter._ifAttributes = options

            writer = InterfacesWriter([adapter], interfaces_path=tempf.name, backup_path="/tmp")
            writer.write_interfaces()

            self.compare_iterface_with_expected(open(tempf.name).read(), expected)

    def test_write_complete2(self):
        # type: ()->None
        """Should work"""

        options = {
            'addrFam': 'inet',
            'broadcast': '192.168.0.255',
            'source': 'static',
            'name': 'eth0',
            'auto': True,
            'up': ['ethtool -s eth0 wol g'],
            'gateway': '192.168.0.254',
            'address': '192.168.0.250',
            'netmask': '255.255.255.0',
            'dns-nameservers': ['8.8.8.8'],
        }

        expected = [
            "auto eth0",
            "iface eth0 inet static",
            "address 192.168.0.250",
            "netmask 255.255.255.0",
            "broadcast 192.168.0.255",
            "gateway 192.168.0.254",
            "dns-nameservers 8.8.8.8",
            "up ethtool -s eth0 wol g",
        ]
        with tempfile.NamedTemporaryFile() as tempf:
            adapter = NetworkAdapter(options={}, interfaces_path=tempf.name)
            adapter._ifAttributes = options

            writer = InterfacesWriter([adapter], interfaces_path=tempf.name, backup_path="/tmp")
            writer.write_interfaces()

            self.compare_iterface_with_expected(open(tempf.name).read(), expected)

    def test_supplicant_conf_write(self):
        # type: ()->None
        '''Test what wpa-conf is written out.'''

        options = {
            'addrFam': 'inet',
            'source': 'dhcp',
            'name': 'wlan0',
            'auto': True,
            'wpa-conf': '/etc/wpa_supplicant/wpa_supplicant.conf'
        }

        expected = [
            "auto wlan0",
            "iface wlan0 inet dhcp",
            "wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf"
        ]
        with tempfile.NamedTemporaryFile() as tempf:
            adapter = NetworkAdapter(options, interfaces_path=tempf.name)
            writer = InterfacesWriter([adapter], interfaces_path=tempf.name, backup_path="/tmp")
            writer.write_interfaces()

            self.compare_iterface_with_expected(open(tempf.name).read(), expected)

    def test_multiDns_write(self):
        # type: ()->None
        """Should work"""

        options = {
            'addrFam': 'inet',
            'broadcast': '192.168.0.255',
            'source': 'static',
            'name': 'eth0',
            'auto': True,
            'gateway': '192.168.0.254',
            'address': '192.168.0.250',
            'netmask': '255.255.255.0',
            'dns-nameservers': ['8.8.8.8', '8.8.4.4', '4.2.2.2'],
            'dns-search': ['mydomain.com', 'myotherdomain.com']
        }

        expected = [
            "auto eth0",
            "iface eth0 inet static",
            "address 192.168.0.250",
            "netmask 255.255.255.0",
            "broadcast 192.168.0.255",
            "gateway 192.168.0.254",
            "dns-nameservers 8.8.8.8 8.8.4.4 4.2.2.2",
            "dns-search mydomain.com myotherdomain.com"
        ]
        with tempfile.NamedTemporaryFile() as tempf:
            adapter = NetworkAdapter(options, interfaces_path=tempf.name)
            writer = InterfacesWriter([adapter], interfaces_path=tempf.name, backup_path="/tmp")
            writer.write_interfaces()

            self.compare_iterface_with_expected(open(tempf.name).read(), expected)

    def test_header_comment_no_symbol_write(self):
        # type: ()->None
        """Write without symbol should work"""

        options = {
            'addrFam': 'inet',
            'source': 'dhcp',
            'name': 'eth0',
            'auto': True
        }
        header_comment = ('This is a multiple line header comment\n'
                          'without the preceding # header, it should be placed at the top\n'
                          'of the file with each line having a "# " in front.')

        expected = [
            '# This is a multiple line header comment',
            '# without the preceding # header, it should be placed at the top',
            '# of the file with each line having a "# " in front.',
            '',
            'auto eth0',
            'iface eth0 inet dhcp'
        ]

        with tempfile.NamedTemporaryFile() as tempf:
            adapter = NetworkAdapter(options=options, interfaces_path=tempf.name)
            writer = InterfacesWriter([adapter], interfaces_path=tempf.name,
                                      header_comment=header_comment, backup_path="/tmp")
            writer.write_interfaces()

            self.compare_iterface_with_expected(open(tempf.name).read(), expected, number_of_stict_lines=len(expected))

    def test_header_comment_symbol_write(self):
        # type: ()->None
        """Write with symbol should work"""

        options = {
            'addrFam': 'inet',
            'source': 'dhcp',
            'name': 'eth0',
            'auto': True
        }
        header_comment = ('# This is a multiple line header comment\n'
                          '# with the preceding # header, it should be placed at the top\n'
                          '# of the file with each line having a "# " in front.')

        expected = [
            '# This is a multiple line header comment',
            '# with the preceding # header, it should be placed at the top',
            '# of the file with each line having a "# " in front.',
            '',
            'auto eth0',
            'iface eth0 inet dhcp'
        ]

        with tempfile.NamedTemporaryFile() as tempf:
            adapter = NetworkAdapter(options=options, interfaces_path=tempf.name)
            writer = InterfacesWriter([adapter], interfaces_path=tempf.name,
                                      header_comment=header_comment, backup_path="/tmp")
            writer.write_interfaces()

            self.compare_iterface_with_expected(open(tempf.name).read(), expected, number_of_stict_lines=len(expected))
