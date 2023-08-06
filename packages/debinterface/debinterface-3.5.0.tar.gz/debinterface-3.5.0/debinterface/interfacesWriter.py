# -*- coding: utf-8 -*-
# Write interface
from __future__ import print_function, with_statement, absolute_import
import shutil
from collections import defaultdict
import os
from string import Template

from . import toolutils
from .adapter import NetworkAdapter

try:
    import typing as tp
except ImportError:
    pass


class InterfacesWriter(object):
    """ Short lived class to write interfaces file """

    # Define templetes for blocks used in /etc/network/interfaces.
    _auto = Template('auto $name\n')
    _hotplug = Template('allow-hotplug $name\n')
    _iface = Template('iface $name $addrFam $source\n')
    _cmd = Template('\t$varient $value\n')
    _comment = Template('# $line\n')

    _addressFields = [
        'address', 'network', 'netmask', 'broadcast',
        'gateway', 'dns-nameservers', 'dns-search'
    ]
    _prepFields = ['pre-up', 'pre-down', 'up', 'down', 'post-up', 'post-down']
    _bridgeFields = ['ports', 'fd', 'hello', 'maxage', 'stp', 'maxwait']
    _plugins = ['hostapd', 'wpa-conf']

    def __init__(self, adapters, interfaces_path, backup_path=None,
                 header_comment=None):
        # type: (tp.List[NetworkAdapter], str, tp.Optional[str], tp.Optional[str])->None
        """ if backup_path is None => no backup """
        self._adapters = adapters
        self._interfaces_path = interfaces_path
        self._backup_path = backup_path
        try:
            is_str = isinstance(header_comment, basestring)
        except NameError:
            is_str = isinstance(header_comment, str)

        if is_str:
            self._header_comment = header_comment
        else:
            self._header_comment = None

    @property
    def adapters(self):
        # type: ()->tp.List[NetworkAdapter]
        return self._adapters

    @adapters.setter
    def adapters(self, value):
        # type: (tp.List[NetworkAdapter])->None
        self._adapters = value

    def write_interfaces(self):
        # type: ()->None
        adapters_by_path = defaultdict(list)
        for adapter in self._adapters:
            # retrocompat check
            path = adapter.interfaces_path or self._interfaces_path
            adapters_by_path[adapter.interfaces_path].append(adapter)

        self._backup_interfaces(adapters_by_path.keys())

        try:

            for path, adapters in adapters_by_path.items():
                with toolutils.atomic_write(path) as interfaces:
                    # Write any header comments for main file.

                    if path == self._interfaces_path:
                        self._write_header_comment(interfaces)

                    # Loop through the provided networkAdapters and
                    # write the new file.
                    for adapter in adapters:
                        # Get dict of details about the adapter.
                        self._write_adapter(interfaces, adapter)
            self._check_interfaces(self._interfaces_path)
        except Exception:
            # Any error, let's roll back
            self._restore_interfaces(adapters_by_path.keys())
            raise

    def _check_interfaces(self, interfaces_path):
        # type: (str)->None
        """Uses ifup to check interfaces file. If it is not in the
            default place, each interface must be checked one by one.

            Args:
                interfaces_path (string) : the path to interfaces file

            Raises:
                ValueError : if invalid network interfaces
        """
        ret = False
        output = ""
        if not self._adapters:
            return

        if interfaces_path == "/etc/network/interfaces":
            # Do not use long form to increase portability with Busybox
            # -n : print out what would happen, but don't do it
            # -i : interfaces file
            ret, output = toolutils.safe_subprocess([
                "/sbin/ifup", "-a", "-n"
            ])
        else:
            for adapter in self._adapters:
                # Do not use long form to increase portability with Busybox
                # -n : print out what would happen, but don't do it
                # -i : interfaces file
                ret, output = toolutils.safe_subprocess([
                    "/sbin/ifup", "-n",
                    "-i{0}".format(interfaces_path),
                    adapter.attributes["name"]
                ])
                if not ret:
                    break
        if not ret:
            raise ValueError("Invalid network interfaces file "
                             "written to disk, restoring to previous "
                             "one : {0}".format(output))

    def _write_header_comment(self, interfaces):
        # type: (tp.IO[str])->None
        if self._header_comment:
            for line in self._header_comment.split('\n'):
                # Check the beginning of the line for a comment field
                # if it does not exist, add it.
                if line[:2] != "# ":
                    line = self._comment.substitute(line=line)
                else:
                    # split strips the newline, add it back
                    line = line + '\n'
                interfaces.write(line)

            # Create a blank line between comment and start of interfaces
            interfaces.write('\n')

    def _write_adapter(self, interfaces, adapter):
        # type: (tp.IO[str], NetworkAdapter)->None
        try:
            adapter.validateAll()
        except ValueError as e:
            print(repr(e))
            raise

        ifAttributes = adapter.export()

        self._write_auto(interfaces, adapter, ifAttributes)
        self._write_hotplug(interfaces, adapter, ifAttributes)
        self._write_addrFam(interfaces, adapter, ifAttributes)
        self._write_addressing(interfaces, adapter, ifAttributes)
        self._write_bridge(interfaces, adapter, ifAttributes)
        self._write_plugins(interfaces, adapter, ifAttributes)
        self._write_callbacks(interfaces, adapter, ifAttributes)
        self._write_unknown(interfaces, adapter, ifAttributes)
        interfaces.write("\n")

    def _write_auto(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        """ Write if applicable """
        try:
            if adapter.attributes['auto'] is True:
                d = dict(name=ifAttributes['name'])
                interfaces.write(self._auto.substitute(d))
        except KeyError:
            pass

    def _write_hotplug(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        """ Write if applicable """
        try:
            if ifAttributes['hotplug'] is True:
                d = dict(name=ifAttributes['name'])
                interfaces.write(self._hotplug.substitute(d))
        except KeyError:
            pass

    def _write_addrFam(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        """ Construct and write the iface declaration.
            The addrFam clause needs a little more processing.
        """
        # Write the source clause.
        # Will not error if omitted. Maybe not the best plan.
        try:
            if (not ifAttributes["name"]
                    or not ifAttributes["addrFam"]
                    or not ifAttributes["source"]):
                raise ValueError("Invalid field content")
            d = dict(name=ifAttributes['name'],
                     addrFam=ifAttributes['addrFam'],
                     source=ifAttributes['source'])
            interfaces.write(self._iface.substitute(d))
        except KeyError:
            pass

    def _write_addressing(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        for field in self._addressFields:
            try:
                value = ifAttributes[field]
                if value and value != 'None':
                    if isinstance(value, list):
                        d = dict(varient=field,
                                 value=" ".join(ifAttributes[field]))
                    else:
                        d = dict(varient=field, value=ifAttributes[field])
                    interfaces.write(self._cmd.substitute(d))
            # Keep going if a field isn't provided.
            except KeyError:
                pass

    def _write_bridge(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        """ Write the bridge information. """
        for field in self._bridgeFields:
            try:
                value = ifAttributes['bridge-opts'][field]
                if value and value != 'None':
                    d = dict(varient="bridge_" + field, value=value)
                    interfaces.write(self._cmd.substitute(d))
            # Keep going if a field isn't provided.
            except KeyError:
                pass

    def _write_callbacks(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        """ Write the up, down, pre-up, pre-down, post-up, and post-down
            clauses.
        """
        for field in self._prepFields:
            try:
                for item in ifAttributes[field]:
                    if item and item != 'None':
                        d = dict(varient=field, value=item)
                        interfaces.write(self._cmd.substitute(d))
            except KeyError:
                # Keep going if a field isn't provided.
                pass

    def _write_plugins(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        """ Write plugins options, currently hostapd. """
        for field in self._plugins:
            try:
                if field in ifAttributes and ifAttributes[field] != 'None':
                    d = dict(varient=field, value=ifAttributes[field])
                    interfaces.write(self._cmd.substitute(d))
            # Keep going if a field isn't provided.
            except KeyError:
                pass

    def _write_unknown(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        """ Write unknowns options """
        try:
            for k, v in ifAttributes['unknown'].items():
                if v:
                    d = dict(varient=k, value=str(v))
                    interfaces.write(self._cmd.substitute(d))
        except (KeyError, ValueError):
            pass

    def _write_sourced_paths(self, interfaces, adapter, ifAttributes):
        # type: (tp.IO[str], NetworkAdapter, tp.Dict[str, tp.Any])->None
        """ Write sourced paths """

        for path in ifAttributes.get('sourced_paths', []):
            d = dict(varient="source", value=str(path))
            interfaces.write(self._cmd.substitute(d))

    def _backup_interfaces(self, adapters_paths):
        # type: (tp.List[str])->None
        """Backup interfaces file is the file exists

            Returns:
                True/False, command output

            Raises:
                IOError : if the copy fails and the source file exists
        """

        if not self._backup_path:
            return

        backup_path = self._backup_path
        if os.path.isfile(backup_path):
            backup_path = os.path.dirname(backup_path)
        # For better backward compatibility
        if not os.path.isdir(backup_path):
            os.mkdir(backup_path)

        for adapter_path in adapters_paths:
            try:
                src_path = os.path.join(backup_path, os.path.basename(adapter_path) + ".bak")

                shutil.copy(adapter_path, src_path)
            except IOError as ex:
                # Only raise if source actually exists
                if os.path.exists(adapter_path):
                    raise ex

    def _restore_interfaces(self, adapters_paths):
        # type: (tp.List[str])->None
        """Restore interfaces file is the file exists

            Returns:
                True/False, command output

            Raises:
                IOError : if the copy fails and the source file exists
        """

        if not self._backup_path:
            return

        for adapter_path in adapters_paths:
            src_path = ''
            try:
                backup_path = self._backup_path
                if os.path.isfile(backup_path):
                    backup_path = os.path.dirname(backup_path)

                src_path = os.path.join(backup_path, os.path.basename(adapter_path) + ".bak")

                shutil.copy(src_path, adapter_path)
            except IOError as ex:
                # Only raise if source actually exists
                if os.path.exists(src_path):
                    raise ex
