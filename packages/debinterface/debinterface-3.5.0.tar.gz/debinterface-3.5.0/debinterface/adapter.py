# -*- coding: utf-8 -*-
"""The NetworkAdapter class represents an interface and its configuration
from the /etc/network/interfaces.
It tries to validate data before writting, but it is by no means fool proof.
It has setter for many common options, but it is impossible to have setter for
every options on earth !
"""
from __future__ import print_function, with_statement, absolute_import

import copy
import socket
import warnings

from .adapterValidation import NetworkAdapterValidation, VALID_OPTS
try:
    import typing as tp
except ImportError:
    pass


class NetworkAdapter(object):
    """ A representation a network adapter. """
    _ifAttributes = None  # type: tp.Dict[str, tp.Any]

    @property
    def attributes(self):
        # type: ()->tp.Dict[str, tp.Any]
        return self._ifAttributes

    def get_attr(self, attr):
        # type: (str)->tp.Any
        return self._ifAttributes[attr]

    def validateAll(self):
        # type: ()->None
        """ Not thorough validations... and quick coded.

            Raises:
                ValueError: if there is a validation error
        """
        self._validator.validate_all(self._ifAttributes)

    def validateOne(self, opt, validations, val):
        # type: (str, tp.Dict[str, tp.Any], tp.Any)->None
        """ Not thorough validations... and quick coded.

            Args:
                opt (str): key name of the option
                validations (dict): contains the validations to checks
                val (any): the option value

            Raises:
                ValueError: if there is a validation error
        """
        self._validator.validate_one(opt, validations, val)

    @staticmethod
    def validateIP(ip):
        # type: (str)->None
        """Validate an IP Address. Works for subnet masks too.
        Tries ipv4 then ipv6

            Args:
                ip (str): the IP as a string

            Raises:
                socket.error on invalid IP
        """
        try:
            socket.inet_aton(ip)
        except socket.error:
            socket.inet_pton(socket.AF_INET6, ip)

    def setName(self, name):
        # type: (str)->None
        """Set the name option of an interface.

            Args:
                name (str): the name of the interface

            Raises:
                ValueError: if there is a validation error
        """
        self._validator.validate_one('name', VALID_OPTS['name'], name)
        self._ifAttributes['name'] = str(name)

    def setAddrFam(self, address_family):
        # type: (str)->None
        """ Set the address family option of an interface.

            Args:
                address_family (str): one of 'inet', 'inet6', 'ipx'

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'addrFam', VALID_OPTS['addrFam'], address_family)
        self._ifAttributes['addrFam'] = address_family

    def setAddressSource(self, address_source):
        # type: (str)->None
        """ Set the address source for an interface.

        Valid values are : dhcp, static, loopback, manual,
        bootp, ppp, wvdial, dynamic, ipv4ll, v4tunnel

            Args:
                address_source (string): address source for an interface

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'source', VALID_OPTS['source'], address_source)
        self._ifAttributes['source'] = address_source

    def setAddress(self, ip_address):
        # type: (str)->None
        """ Set the ipaddress of an interface.

            Args:
                ip_address (str): the IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'address', VALID_OPTS['address'], ip_address)
        self._ifAttributes['address'] = ip_address

    def setNetmask(self, netmask):
        # type: (str)->None
        """ Set the netmask of an interface.

            Args:
                netmask (str): the netmask IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'netmask', VALID_OPTS['netmask'], netmask)
        self._ifAttributes['netmask'] = netmask

    def setGateway(self, gateway):
        # type: (str)->None
        """ Set the default gateway of an interface.

            Args:
                gateway (str): the gateway IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'gateway', VALID_OPTS['gateway'], gateway)
        self._ifAttributes['gateway'] = gateway

    def setBroadcast(self, broadcast):
        # type: (str)->None
        """ Set the broadcast address of an interface.

            Args:
                broadcast (str): the broadcast IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'broadcast', VALID_OPTS['broadcast'], broadcast)
        self._ifAttributes['broadcast'] = broadcast

    def setNetwork(self, network):
        # type: (str)->None
        """ Set the network identifier of an interface.

            Args:
                network (str): the IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'network', VALID_OPTS['network'], network)
        self._ifAttributes['network'] = network

    def setAuto(self, auto):
        # type: (bool)->None
        """ Set the option to autostart the interface.

            Args:
                auto (bool): interface will be set as auto if True

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'auto', VALID_OPTS['auto'], auto)
        self._ifAttributes['auto'] = auto

    def setHotplug(self, hotplug):
        # type: (bool)->None
        """ Set the option to allow hotplug on the interface.
        Beware, option is really called allow-hotplug, that's a
        small historic cruft...

            Args:
                hotplug (bool): interface hotplug will be set if True

            Raises:
                ValueError: if there is a validation error
        """

        msg = "hotplug key will be renamed into allow-hotplug in 4.0"
        warnings.warn(msg, DeprecationWarning)

        self._validator.validate_one(
            'hotplug', VALID_OPTS['hotplug'], hotplug)
        self._ifAttributes['hotplug'] = hotplug

    def setHostapd(self, hostapd):
        # type: (tp.Any)->None
        """ Set the wifi conf file on the interface.

            Raises:
                ValueError: if there is a validation error
        """

        self._validator.validate_one(
            'hostapd', VALID_OPTS['hostapd'], hostapd)
        self._ifAttributes['hostapd'] = hostapd

    def setNameservers(self, nameserver):
        # type: (tp.Any)->None
        """ Set the ipaddress of an interface.

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('nameservers', self._valid['nameservers'], nameserver)
        self._ifAttributes['nameservers'] = nameserver

    def setDnsNameservers(self, nameservers):
        # type: (tp.Union[str, tp.List[str]])->None
        """ Set the dns nameservers on the interface.

            Args:
                nameservers (str, list): the IP as a string

            Raises:
                ValueError: if there is a validation error
        """
        if isinstance(nameservers, str):
            nameservers = nameservers.split()
        self._validator.validate_one(
            'dns-nameservers', VALID_OPTS['dns-nameservers'], nameservers)
        self._ifAttributes['dns-nameservers'] = nameservers

    def setDnsSearch(self, searchUri):
        # type: (tp.Union[str, tp.List[str]])->None
        """ Set the dns default search URI.

            Args:
                searchURI (str, list): The default search domain

            Raises:
                ValueError: if there is a validation error
        """
        if isinstance(searchUri, str):
            searchUri = searchUri.split()
        self._validator.validate_one(
            'dns-search', VALID_OPTS['dns-search'], searchUri)
        self._ifAttributes['dns-search'] = searchUri

    def setBropts(self, opts):
        # type: (tp.Dict[str, tp.Any])->None
        """Set the bridge options of an interface.

            Args:
                opts (dict): a dictionary mapping option names and values.
                    In the interfaces file, options will have a bridge prefix.

            Raises:
                ValueError: if there is a validation error

        """

        self._validator.validate_one(
            'bridge-opts', VALID_OPTS['bridge-opts'], opts)
        self._ifAttributes['bridge-opts'] = opts

    def setWpaConf(self, conf_path):
        # type: (str)->None
        '''Set the wpa supplicant configuration path for supplicant
        config for wireless interfaces.

        Args:
            conf_path (str): Path at which the supplicant config is located.
        '''
        self._ifAttributes['wpa-conf'] = conf_path

    def replaceBropt(self, key, value):
        # type: (str, tp.Any)->None
        """Set a discrete bridge option key with value

            Args:
                key (str): the option key in the bridge option
                value (any): the value
        """

        self._ifAttributes['bridge-opts'][key] = value

    def appendBropts(self, key, value):
        # type: (str, tp.Any)->None
        """Set a discrete bridge option key with value

            Args:
                key (str): the option key in the bridge option
                value (any): the value
        """
        new_value = value
        if key in self._ifAttributes['bridge-opts']:
            new_value = self._ifAttributes['bridge-opts'][key] + value
        self.replaceBropt(key, new_value)

    def setUp(self, up):
        # type: (tp.Union[str, tp.List[str]])->None
        """Set and add to the up commands for an interface.

            Args:
                up (list): list of shell commands
        """
        if isinstance(up, list):
            self._ifAttributes['up'] = up
        elif isinstance(up, str):
            self._ifAttributes['up'] = [up]
        else:
            raise ValueError("Invalid value type {0}, expected str or List[str]".format(type(up)))

    def appendUp(self, cmd):
        # type: (tp.Union[str, tp.List[str]])->None
        """Append a shell command to run when the interface is up.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "up", cmd)

    def setDown(self, down):
        # type: (tp.Union[str, tp.List[str]])->None
        """Set and add to the down commands for an interface.

            Args:
                down (list): list of shell commands
        """
        if isinstance(down, list):
            self._ifAttributes['down'] = down
        elif isinstance(down, str):
            self._ifAttributes['down'] = [down]
        else:
            raise ValueError("Invalid value type {0}, expected str or List[str]".format(type(down)))

    def appendDown(self, cmd):
        # type: (tp.Union[str, tp.List[str]])->None
        """Append a shell command to run when the interface is down.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "down", cmd)

    def setPreUp(self, pre):
        # type: (tp.Union[str, tp.List[str]])->None
        """Set and add to the pre-up commands for an interface.

            Args:
                pre (list): list of shell commands
        """
        if isinstance(pre, list):
            self._ifAttributes['pre-up'] = pre
        elif isinstance(pre, str):
            self._ifAttributes['pre-up'] = [pre]
        else:
            raise ValueError("Invalid value type {0}, expected str or List[str]".format(type(pre)))

    def appendPreUp(self, cmd):
        # type: (tp.Union[str, tp.List[str]])->None
        """Append a shell command to run when the interface is pre-up.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "pre-up", cmd)

    def setPreDown(self, pre):
        # type: (tp.Union[str, tp.List[str]])->None
        """Set and add to the pre-down commands for an interface.

            Args:
                pre (list): list of shell commands
        """
        if isinstance(pre, list):
            self._ifAttributes['pre-down'] = pre
        elif isinstance(pre, str):
            self._ifAttributes['pre-down'] = [pre]
        else:
            raise ValueError("Invalid value type {0}, expected str or List[str]".format(type(pre)))

    def appendPreDown(self, cmd):
        # type: (tp.Union[str, tp.List[str]])->None
        """Append a shell command to run when the interface is pre-down.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "pre-down", cmd)

    def setPostUp(self, post):
        # type: (tp.Union[str, tp.List[str]])->None
        """Set and add to the post-up commands for an interface.

            Args:
                post (list): list of shell commands
        """
        if isinstance(post, list):
            self._ifAttributes['post-up'] = post
        elif isinstance(post, str):
            self._ifAttributes['post-up'] = [post]
        else:
            raise ValueError("Invalid value type {0}, expected str or List[str]".format(type(post)))

    def appendPostUp(self, cmd):
        # type: (tp.Union[str, tp.List[str]])->None
        """Append a shell command to run when the interface is post-up.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "post-up", cmd)

    def setPostDown(self, post):
        # type: (tp.Union[str, tp.List[str]])->None
        """Set and add to the post-down commands for an interface.

            Args:
                post (list): list of shell commands
        """
        if isinstance(post, list):
            self._ifAttributes['post-down'] = post
        elif isinstance(post, str):
            self._ifAttributes['post-down'] = [post]
        else:
            raise ValueError("Invalid value type {0}, expected str or List[str]".format(type(post)))

    def appendPostDown(self, cmd):
        # type: (tp.Union[str, tp.List[str]])->None
        """Append a shell command to run when the interface is post-down.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "post-down", cmd)

    def setUnknown(self, key, val):
        # type: (str, tp.Any)->None
        """Stores uncommon options as there are with no special handling
        It's impossible to know about all available options
        WARNING: duplicated directives are overwriten. TODO better

            Args:
                key (str): the option name
                val (any): the option value
        """
        if 'unknown' not in self._ifAttributes:
            self._ifAttributes['unknown'] = {}
        self._ifAttributes['unknown'][key] = val

    def export(self, options_list=None):
        # type: (tp.Optional[tp.List[str]])->tp.Dict[str, tp.Any]
        """ Return a copy of the ifAttributes data structure as dict.
        You may optionally pass a list of options to return

            Args:
                options_list (list, optional): a list of options you want

            Returns:
                dict: the ifAttributes data structure, optionally filtered
        """

        attrs = self._ifAttributes
        if options_list:
            attrs = {}
            for k in options_list:
                try:
                    attrs[k] = self._ifAttributes[k]
                except KeyError:
                    attrs[k] = None
        return copy.deepcopy(attrs)

    def display(self):
        # type: ()->None
        """Display a (kind of) human readable representation of the adapter."""
        print('============')
        for key, value in self._ifAttributes.items():
            if isinstance(value, list):
                print(key + ': ')
                for item in value:
                    print('\t' + item)
            elif isinstance(value, dict):
                print(key + ': ')
                for item in value.keys():
                    print('\t' + item + ': ' + value[item])
            else:
                print(key + ': ' + str(value))
        print('============')

    def __init__(self, options, interfaces_path=None):
        # type: (tp.Union[str, tp.Dict[str, tp.Any]], tp.Optional[str])->None
        # Initialize attribute storage structure.
        self._validator = NetworkAdapterValidation()
        self._valid = VALID_OPTS  # For backward compatibility

        # the file from where the adapter belongs.
        self.interfaces_path = interfaces_path or "/etc/network/interfaces"
        self.reset()
        self.set_options(options)

    def reset(self):
        # type: ()->None
        """ Initialize attribute storage structure. """
        self._ifAttributes = {}
        self._ifAttributes['bridge-opts'] = {}
        self._ifAttributes['up'] = []
        self._ifAttributes['down'] = []
        self._ifAttributes['pre-up'] = []
        self._ifAttributes['pre-down'] = []
        self._ifAttributes['post-up'] = []
        self._ifAttributes['post-down'] = []

    def set_options(self, options):
        # type: (tp.Union[str, tp.Dict[str, tp.Any]])->None
        """Set options, either only the name if options is a str,
        or all given options if options is a dict

            Args:
                options (str/dict): historical code... only set
                    the name if options is a str, or all given
                    options if options is a dict

            Raises:
                ValueError: if validation error
                socket.error: if validation error of an IP
                Exception: if anything weird happens
        """

        # Set the name of the interface.
        if isinstance(options, str):
            self.setName(options)

        # If a dictionary of options is provided, populate the adapter options.
        elif isinstance(options, dict):
            try:
                roseta = {
                    'name': self.setName,
                    'addrFam': self.setAddrFam,
                    'source': self.setAddressSource,
                    'address': self.setAddress,
                    'netmask': self.setNetmask,
                    'gateway': self.setGateway,
                    'broadcast': self.setBroadcast,
                    'network': self.setNetwork,
                    'auto': self.setAuto,
                    'allow-hotplug': self.setHotplug,
                    'hotplug': self.setHotplug,
                    'bridgeOpts': self.setBropts,
                    'bridge-opts': self.setBropts,
                    'up': self.setUp,
                    'down': self.setDown,
                    'pre-up': self.setPreUp,
                    'pre-down': self.setPreDown,
                    'post-up': self.setPostUp,
                    'post-down': self.setPostDown,
                    'hostapd': self.setHostapd,
                    'dns-nameservers': self.setDnsNameservers,
                    'dns-search': self.setDnsSearch,
                    'nameservers': self.setNameservers,
                    'wpa-conf': self.setWpaConf,
                }  # type: tp.Dict[str, tp.Callable[[tp.Any], None]]
                for key, value in options.items():
                    if key in roseta:
                        # keep KeyError for validation errors
                        roseta[key](value)
                    else:
                        # Store as if
                        self.setUnknown(key, value)
            except Exception:
                self.reset()
                raise
        else:
            msg = "No arguments given. Provide a name or options dict."
            raise ValueError(msg)

    @staticmethod
    def _ensure_list(dic, key, value):
        # type: (tp.Any, str, tp.Any)->None
        """Ensure the data for the given key will be in a list.
        If value is a list, it will be flattened

            Args:
                dic (dict): source dict
                key (string): key to use in dic
                value (any): the data. Will be appended into a
                    list if it's not one
        """
        if key not in dic:
            dic[key] = []
        if not isinstance(dic[key], list):
            tmp = dic[key]
            dic[key] = [tmp]
        if isinstance(value, list):
            dic[key] += value
        else:
            dic[key].append(value)
