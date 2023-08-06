# -*- coding: utf-8 -*-
# A class representing the contents of /etc/network/interfaces
from __future__ import print_function, with_statement, absolute_import
from .interfacesWriter import InterfacesWriter
from .interfacesReader import InterfacesReader
from .adapter import NetworkAdapter
from . import toolutils
try:
    import typing as tp
except ImportError:
    pass


class Interfaces(object):
    _interfaces_path = '/etc/network/interfaces'
    _adapters = None  # type: tp.List[NetworkAdapter]
    _removed_adapters = None  # type: tp.Set[NetworkAdapter]

    def __init__(self, update_adapters=True,
                 interfaces_path='/etc/network/interfaces',
                 backup_path=None,
                 header_comment=None):
        # type: (bool, str, tp.Optional[str], tp.Optional[str])->None
        """ By default read interface file on init

            Args:
                update_adapters (bool, optional): load adapters from interface
                    file. Default True
                interfaces_path (str, optional): default to
                    /etc/network/interfaces
                backup_path (str, optional): default to
                    /etc/network/interfaces.bak
                header_comment(str, optional): default to
                    none, otherwise sets comments at the
                    top of the interfaces file.
        """

        self._set_paths(interfaces_path, backup_path)

        if update_adapters is True:
            self.updateAdapters()
        else:
            self._adapters = []
        self._header_comment = header_comment
        self._removed_adapters = set()

    @property
    def adapters(self):
        # type: ()->tp.List[NetworkAdapter]
        return self._adapters

    @property
    def interfaces_path(self):
        # type: ()->str
        """Returns the path of the main interface file
        Others may come from the source directive. Adapters register the path
        """
        return self._interfaces_path

    @property
    def backup_path(self):
        # type: ()->tp.Optional[str]
        return self._backup_path or self._interfaces_path + ".bak"

    @property
    def header_comment(self):
        # type: ()->tp.Optional[str]
        return self._header_comment

    def updateAdapters(self):
        # type: ()->None
        """ (re)read interfaces file and save adapters """
        reader = InterfacesReader(self._interfaces_path)
        self._adapters = reader.parse_interfaces()
        self._header_comment = reader.header_comments
        self._removed_adapters = set()

    def writeInterfaces(self):
        # type: ()->None
        """ write adapters to interfaces file """
        return InterfacesWriter(
            self._adapters,
            self._interfaces_path,
            self._backup_path,
            self._header_comment
        ).write_interfaces()

    def getAdapter(self, name):
        # type: (str)->tp.Optional[NetworkAdapter]
        """ Find adapter by interface name

            Args:
                name (str): the name of the interface

            Returns:
                NetworkAdapter: the new adapter or None if not found
        """
        return next(
            (
                x for x in self._adapters
                if x.attributes['name'] == name
            ),
            None)

    def addAdapter(self, options, index=None, interfaces_path=None):
        # type: (tp.Union[str, tp.Dict[str, tp.Any]], tp.Optional[int], tp.Optional[str])->NetworkAdapter
        """Insert a NetworkAdapter before the given index
            or at the end of the list.
            Options should be a string (name) or a dict

            Args:
                options (string or dict): options to build a network adaptator
                index (integer, optional): index to insert the NetworkAdapter
                interfaces_path (str, optional): path to the source file of the adadpter.

            Returns:
                NetworkAdapter: the new adapter
        """
        adapter = NetworkAdapter(options, interfaces_path=interfaces_path)
        adapter.validateAll()

        if index is None:
            self._adapters.append(adapter)
        else:
            self._adapters.insert(index, adapter)
        return adapter

    def removeAdapter(self, index):
        # type: (int)->None
        """ Remove the adapter at the given index.
        TODO: handle file deletion of sourced paths

            Args:
                index (int): the position of the adapter
        """

        self._removed_adapters.add(self._adapters.pop(index))

    def removeAdapterByName(self, name):
        # type: (str)->None
        """ Remove the adapter with the given name.

            Args:
                name (str): the name of the interface
        """

        cleaned_list = []
        for adapter in self._adapters:
            if adapter.attributes["name"] != name:
                cleaned_list.append(adapter)
            else:
                self._removed_adapters.add(adapter)

        self._adapters = cleaned_list

    @staticmethod
    def upAdapter(if_name):
        # type: (str)->tp.Tuple[bool, str]
        """Uses ifup

            Args:
                if_name (str): the name of the interface

            Returns:
                bool, str: True/False, command output.
        """

        return toolutils.safe_subprocess(["/sbin/ifup", if_name])

    @staticmethod
    def downAdapter(if_name):
        # type: (str)->tp.Tuple[bool, str]
        """Uses ifdown

            Args:
                if_name (str): the name of the interface

            Returns:
                bool, str: True/False, command output.
        """

        return toolutils.safe_subprocess(["/sbin/ifdown", if_name])

    def _set_paths(self, interfaces_path, backup_path):
        # type: (str, tp.Optional[str])->None
        """Either use user input or defaults

            Args:
                interfaces_path (str): path to interfaces file
                backup_path (str): default to interfaces_path + .bak
        """

        if interfaces_path:
            self._interfaces_path = interfaces_path

        if backup_path:
            self._backup_path = backup_path
        else:
            # self._interfaces_path is never None
            self._backup_path = self._interfaces_path + ".bak"
