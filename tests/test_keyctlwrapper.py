
# -*- coding: utf-8 -*-

import pytest

from keyctl import KeyctlWrapper, KeyNotExistError, KeyAlreadyExistError


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


class TestKeyctlWrapper(object):
    def test_get_all_key_ids(self, empty_keyring):
        keyctl = empty_keyring

        # empty list
        keys = keyctl.get_all_key_ids()
        assert len(keys) == 0

        # 1 key
        keyids = [keyctl.add_key('test1', 'abc')]

        keys = keyctl.get_all_key_ids()
        assert len(keys) == 1
        assert keys[0] == keyids[0]

        # 2 keys
        keyids.append(keyctl.add_key('test2', 'abc'))

        keys = keyctl.get_all_key_ids()
        assert len(keys) == 2
        assert keys[0] in keyids
        assert keys[1] in keyids

    # ---------------------------------------------------------------

    def test_get_id_from_name(self, empty_keyring):
        keyctl = empty_keyring

        # non existing keyname
        with pytest.raises(KeyNotExistError):
            keyctl.get_id_from_name('this key should not exist')

        # simple name finding
        keyid1 = keyctl.add_key('test key', 'content')

        keyid = keyctl.get_id_from_name('test key')
        assert keyid == keyid1

        # deleted key
        keyctl.remove_key(keyid1)

        with pytest.raises(KeyNotExistError):
            keyctl.get_id_from_name('test key')

    # ---------------------------------------------------------------

    def test_get_name_from_id(self, empty_keyring):
        keyctl = empty_keyring

        # not found
        with pytest.raises(KeyNotExistError):
            keyctl.get_name_from_id(999)

        # simple name
        name1 = 'test key'
        keyid1 = keyctl.add_key(name1, 'content')

        name = keyctl.get_name_from_id(keyid1)
        assert name == name1

    # ---------------------------------------------------------------

    def test_get_data_from_id(self, empty_keyring):
        keyctl = empty_keyring

        # wrong mode
        with pytest.raises(AttributeError):
            keyctl.get_data_from_id(999, 'hexx')

        # not found
        with pytest.raises(KeyNotExistError):
            keyctl.get_data_from_id(999)

        # raw mode
        content = 'content xyz'
        keyid = keyctl.add_key('test key', content)

        data = keyctl.get_data_from_id(keyid)
        assert data == content

        # hex mode
        data = keyctl.get_data_from_id(keyid, 'hEx')
        assert data == content.encode("utf8").hex()

    # ---------------------------------------------------------------

    def test_add_key(self, empty_keyring):
        keyctl = empty_keyring

        # simple add
        content = 'abc def ghi'
        keyid = keyctl.add_key('test key', content)

        data = keyctl.get_data_from_id(keyid)
        assert data == content

        # existing key
        with pytest.raises(KeyAlreadyExistError):
            keyctl.add_key('test key', 'x')

    # ---------------------------------------------------------------

    def test_update_key(self, empty_keyring):
        keyctl = empty_keyring

        # simple update
        new_content = 'abc def ghi'
        keyid = keyctl.add_key('test key', 'xxx')
        data = keyctl.get_data_from_id(keyid)
        assert data == 'xxx'

        keyctl.update_key(keyid, new_content)
        data = keyctl.get_data_from_id(keyid)
        assert data == new_content

        # non existing
        with pytest.raises(KeyNotExistError):
            keyctl.update_key(999, 'abc')

    # ---------------------------------------------------------------

    def test_remove_key(self, empty_keyring):
        keyctl = empty_keyring

        # simple remove
        keyid = keyctl.add_key('test key', 'xxx')
        data = keyctl.get_data_from_id(keyid)
        assert data == 'xxx'

        keyctl.remove_key(keyid)
        with pytest.raises(KeyNotExistError):
            keyctl.get_data_from_id(keyid)

        # non existing
        with pytest.raises(KeyNotExistError):
            keyctl.remove_key(999)

    # ---------------------------------------------------------------

    def test_clear_keyring(self, empty_keyring):
        keyctl = empty_keyring

        keyctl.add_key('key1', 'abc')
        keyctl.add_key('key2', 'abc')
        keyctl.add_key('key3', 'abc')
        keys = keyctl.get_all_key_ids()
        assert len(keys) == 3

        keyctl.clear_keyring()
        keys = keyctl.get_all_key_ids()
        assert len(keys) == 0


# -------------------------------------------------------------------
