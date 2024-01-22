# -*- coding: utf-8 -*-

import pytest

from keyctl import KeyctlWrapper, KeyNotExistError, KeyAlreadyExistError, KeyctlOperationError
from keyctl import Key


# -------------------------------------------------------------------


@pytest.fixture
def empty_keyring():
    keyctl = KeyctlWrapper()

    keyctl.clear_keyring()
    keys = keyctl.get_all_key_ids()
    assert len(keys) == 0

    yield keyctl

    # teardown
    keyctl.clear_keyring()


# -------------------------------------------------------------------


class TestKey(object):
    def test_init(self, empty_keyring):
        # empty
        k = Key()
        assert k.id is None
        assert k.name is None
        assert k.data is None

        # non existing key
        with pytest.raises(KeyNotExistError):
            Key(999)

        # exisitng key
        keyctl = empty_keyring
        keyid = keyctl.add_key('test key', 'content xyz')
        k = Key(keyid)
        assert k.name == 'test key'
        assert k.data == 'content xyz'

    # ---------------------------------------------------------------

    def test_list(self, empty_keyring):
        keyctl = empty_keyring

        # empty list
        keylist = Key.list()
        assert len(keylist) == 0

        # 3 keys
        keysrc = [
            {'name': 'test key 1', 'data': 'content 111'},
            {'name': 'test key 2', 'data': 'content 222'},
            {'name': 'test key 3', 'data': 'content 333'},
        ]
        for src in keysrc:
            src['id'] = keyctl.add_key(src['name'], src['data'])

        keylist = Key.list()
        assert len(keylist) == 3
        for key in keylist:
            src = next((x for x in keysrc if x['id'] == key.id), None)
            assert key.id == src['id']
            assert key.name == src['name']
            assert key.data == src['data']

    # ---------------------------------------------------------------

    def test_search(self, empty_keyring):
        # non existing key
        with pytest.raises(KeyNotExistError):
            Key.search('this key does not exist')

        # existing key
        keyctl = empty_keyring
        keyid = keyctl.add_key('test key', 'content xyz')
        k = Key.search('test key')
        assert k.id == keyid
        assert k.name == 'test key'
        assert k.data == 'content xyz'

    # ---------------------------------------------------------------

    def test_add(self, empty_keyring):
        keyctl = empty_keyring

        # not existing key
        with pytest.raises(KeyNotExistError):
            keyctl.get_id_from_name('test key 111')

        k = Key.add('test key 111', 'content 111')
        keyid = keyctl.get_id_from_name('test key 111')
        assert k.id == keyid

        # already existing key
        with pytest.raises(KeyAlreadyExistError):
            Key.add('test key 111', 'content xyz')

    # ---------------------------------------------------------------

    def test_delete(self, empty_keyring):
        keyctl = empty_keyring

        # existing key
        keyid = keyctl.add_key('test key', 'abc')
        k = Key(keyid)
        assert k.name == 'test key'
        k.delete()
        with pytest.raises(KeyNotExistError):
            keyctl.get_id_from_name('test key')

        # uninitialized key
        k = Key()
        with pytest.raises(KeyctlOperationError):
            k.delete()

        # not existing key (delete called twice)
        keyid = keyctl.add_key('test key', 'abc')
        k = Key(keyid)
        k.delete()
        with pytest.raises(KeyNotExistError):
            k.delete()

    # ---------------------------------------------------------------

    def test_update(self, empty_keyring):
        keyctl = empty_keyring

        # existing key
        keyid = keyctl.add_key('test key', 'abc')
        k1 = Key(keyid)
        assert k1.data == 'abc'

        k1.update('xyz')
        assert k1.data == 'xyz'
        k2 = Key(keyid)
        assert k1.id == k2.id
        assert k1.name == k2.name
        assert 'xyz' == k2.data

        # not existing key
        k1.delete()
        with pytest.raises(KeyNotExistError):
            k2.update('xxxx')

# -------------------------------------------------------------------
