
# -*- coding: utf-8 -*-

from typing import List
from .keyctlwrapper import KeyctlWrapper


# -------------------------------------------------------------------


class Key(object):
    def __init__(self, keyid=None, keyring=None, keytype=None):
        self.id = None
        self.name = None
        self.data = None
        self.data_hex = None

        self._keyctl = self._init_keyctl(keyring, keytype)

        if keyid is not None:
            self._load_key(keyid)

    # ---------------------------------------------------------------

    @staticmethod
    def _init_keyctl(keyring=None, keytype=None) -> KeyctlWrapper:
        if keyring is not None and keytype is not None:
            keyctl = KeyctlWrapper(keyring=keyring, keytype=keytype)
        elif keyring is not None:
            keyctl = KeyctlWrapper(keyring=keyring)
        elif keytype is not None:
            keyctl = KeyctlWrapper(keytype=keytype)
        else:
            keyctl = KeyctlWrapper()

        return keyctl

    # ---------------------------------------------------------------

    def _load_key(self, keyid):
        self.id = keyid
        self.name = self._keyctl.get_name_from_id(keyid)
        self.data = self._keyctl.get_data_from_id(keyid)
        self.data_hex = self._keyctl.get_data_from_id(keyid, 'hex')

    # ---------------------------------------------------------------

    @classmethod
    def list(cls, keyring=None, keytype=None) -> List["Key"]:
        keyctl = cls._init_keyctl(keyring, keytype)
        keyids = keyctl.get_all_key_ids()

        keylist = []
        for keyid in keyids:
            key = cls(keyid)
            keylist.append(key)

        return keylist

    # ---------------------------------------------------------------

    @classmethod
    def search(cls, name, keyring=None, keytype=None) -> "Key":
        key = cls(keyring, keytype)

        key.id = key._keyctl.get_id_from_name(name)
        key.name = name
        key.data = key._keyctl.get_data_from_id(key.id)
        key.data_hex = key._keyctl.get_data_from_id(key.id, 'hex')

        return key

    # ---------------------------------------------------------------

    @classmethod
    def add(cls, name, data, keyring=None, keytype=None) -> "Key":
        keyctl = cls._init_keyctl(keyring, keytype)

        keyid = keyctl.add_key(name, data)

        key = cls(keyid)

        return key

    # ---------------------------------------------------------------

    def update(self, data):
        self._keyctl.update_key(self.id, data)
        self._load_key(self.id)

    # ---------------------------------------------------------------

    def delete(self):
        self._keyctl.remove_key(self.id)

    # ---------------------------------------------------------------

    def __repr__(self):
        return '<{}({}, \'{}\', \'{}\')>'.format(self.__class__.__name__, self.id, self.name, self.data)


# -------------------------------------------------------------------
