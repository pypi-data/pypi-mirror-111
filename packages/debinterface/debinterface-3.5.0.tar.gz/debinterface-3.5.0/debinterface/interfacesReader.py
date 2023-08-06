# -*- coding: utf-8 -*-
# A class representing the contents of /etc/network/interfaces
from __future__ import print_function, with_statement, absolute_import
import glob
import os
from .adapter import NetworkAdapter
try:
    import typing as tp
except ImportError:
    pass


class InterfacesReader(object):
    """ Short lived class to read interfaces file """
    _root_interfaces_path = None  # type: str
    _parsed_files = None  # type: tp.Set[str]
    _adapters = None  # type: tp.List[NetworkAdapter]
    _header_comments = None  # type: str
    _auto_list = None  # type: tp.List[str]
    _hotplug_list = None  # type: tp.List[str]

    def __init__(self, interfaces_path):
        # type: (str)->None
        self._root_interfaces_path = interfaces_path
        self._parsed_files = set()
        self._reset()

    @property
    def adapters(self):
        # type: ()->tp.List[NetworkAdapter]
        return self._adapters

    @property
    def header_comments(self):
        # type: ()->str
        return self._header_comments

    def parse_interfaces(self, read_comments=False):
        # type: (bool)->tp.List[NetworkAdapter]
        """ Read /etc/network/interfaces (or specified file).
            Save adapters
            Return an array of networkAdapter instances.
        """
        self._reset()
        self._read_file(self._root_interfaces_path)

        for entry in self._auto_list:
            for adapter in self._adapters:
                if adapter.attributes['name'] == entry:
                    adapter.setAuto(True)

        for entry in self._hotplug_list:
            for adapter in self._adapters:
                if adapter.attributes['name'] == entry:
                    adapter.setHotplug(True)

        return self._adapters

    def _read_files(self, wildcard_path):
        all_files = glob.glob(wildcard_path)
        for file_path in all_files:
            # Skip all files that was parsed
            if file_path not in self._parsed_files:
                self._read_file(file_path)

    def _read_file(self, current_path):
        # type: (str)->None
        """Open up the given interfaces file. Read only.
        If a source directive is found, it will call itself recursively
        """

        if current_path in self._parsed_files:
            return
        self._parsed_files.add(current_path)

        with open(current_path, "r") as interfaces:
            # When the first non-comment line is parsed, header
            # comments have been read in.
            header_parsed = False
            # Loop through the interfaces file.
            for line in interfaces:
                # 1. Identify the clauses by analyzing the first
                # word of each line.
                # 2. Go to the next line if the current line is a comment.
                # line = line.strip().replace("\n", "")
                if not line:
                    pass
                elif line.strip().startswith("#") is True:
                    if not header_parsed:
                        self._header_comments += line
                else:
                    # Header comments can no longer
                    # be parsed in when the first interfaces
                    # line is parsed in.
                    header_parsed = True
                    self._parse_iface(line, current_path)
                    # Ignore blank lines.
                    if not line.isspace():
                        self._parse_details(line)
                    self._read_auto(line)
                    self._read_hotplug(line)

                    # Is there some file to source ?
                    source_path = self._read_sourced_path(line)
                    if source_path:
                        self._read_files(source_path)

                    # TODO: lots of directives are completly ignored
                    # and would be deleted

    def _parse_iface(self, line, current_path):
        # type: (str, str)->None
        if line.startswith('iface '):
            sline = line.split()
            # Update the self._context when an iface clause is encountered.
            self._context += 1
            # sline[1] being a string, it will be used as the adapter name
            self._adapters.append(
                NetworkAdapter(sline[1].strip(), interfaces_path=current_path)
            )
            self._adapters[self._context].setAddressSource(sline[-1].strip())
            self._adapters[self._context].setAddrFam(sline[2].strip())

    def _parse_details(self, line):
        # type: (str)->None
        if line[0].isspace() is True:
            keyword, value = line.strip().split(None, 1)

            if keyword == 'address':
                self._adapters[self._context].setAddress(value)
            elif keyword == 'netmask':
                self._adapters[self._context].setNetmask(value)
            elif keyword == 'gateway':
                self._adapters[self._context].setGateway(value)
            elif keyword == 'broadcast':
                self._adapters[self._context].setBroadcast(value)
            elif keyword == 'network':
                self._adapters[self._context].setNetwork(value)
            elif keyword == 'hostapd':
                self._adapters[self._context].setHostapd(value)
            elif keyword == 'wpa-conf':
                self._adapters[self._context].setWpaConf(value)
            elif keyword == 'dns-nameservers':
                self._adapters[self._context].setDnsNameservers(value)
            elif keyword == 'dns-search':
                self._adapters[self._context].setDnsSearch(value)
            elif keyword.startswith('bridge'):
                _, option = keyword.replace('-', '_').split('_', 1)
                self._adapters[self._context].replaceBropt(option, value)
            elif keyword == 'up':
                self._adapters[self._context].appendUp(value)
            elif keyword == 'down':
                self._adapters[self._context].appendDown(value)
            elif keyword == 'pre-up':
                self._adapters[self._context].appendPreUp(value)
            elif keyword == 'pre-down':
                self._adapters[self._context].appendPreDown(value)
            elif keyword == 'post-up':
                self._adapters[self._context].appendPostUp(value)
            elif keyword == 'post-down':
                self._adapters[self._context].appendPostDown(value)
            else:
                # store as if so as not to loose it
                self._adapters[self._context].setUnknown(keyword, value)

    def _read_auto(self, line):
        # type: (str)->None
        """ Identify which adapters are flagged auto. """
        if line.startswith('auto '):
            sline = [x.strip() for x in line.split()]
            for word in sline:
                if word == 'auto':
                    pass
                else:
                    self._auto_list.append(word)

    def _read_hotplug(self, line):
        # type: (str)->None
        """ Identify which adapters are flagged allow-hotplug. """
        if line.startswith('allow-hotplug '):
            sline = [x.strip() for x in line.split()]
            for word in sline:
                if word == 'allow-hotplug':
                    pass
                else:
                    self._hotplug_list.append(word)

    def _read_sourced_path(self, line):
        # type: (str)->tp.Optional[str]
        """Identify source path/to/file. If so will return the path to open it.
        Relative paths will be expanded from root path

            Returns:
              str: absolute path to the sourced file
        """
        if line.startswith('source '):
            sline = [x.strip() for x in line.split()]
            sline.pop(0)
            path = ' '.join(sline)
            if not os.path.isabs(path):
                current_root = self._root_interfaces_path
                if os.path.isfile(current_root):
                    current_root = os.path.dirname(current_root)
                path = os.path.join(current_root, path)
            return path
        return None

    def _reset(self):
        # type: ()->None
        # Initialize a place to store created networkAdapter objects.
        self._adapters = []

        # Keep a list of adapters that have the auto or
        # allow-hotplug flags set.
        self._auto_list = []
        self._hotplug_list = []

        # Store the interface context.
        # This is the index of the adapters collection.
        self._context = -1
        self._header_comments = ''
