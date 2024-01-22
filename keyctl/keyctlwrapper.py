# -*- coding: utf-8 -*-

import subprocess
from typing import List


# -------------------------------------------------------------------


class KeyctlWrapperException(Exception):
    @staticmethod
    def _getkeydesc(keyid=None, keyname=None):
        if keyid is not None and keyname is not None:
            keydesc = "({} / '{}')".format(keyid, keyname)
        elif keyid is not None:
            keydesc = "({})".format(keyid)
        elif keyname is not None:
            keydesc = "('{}')".format(keyname)
        else:
            keydesc = '(undef)'

        return keydesc


class KeyNotExistError(KeyctlWrapperException):
    def __init__(self, message=None, keyid=None, keyname=None):
        if message is None:
            message = 'Key {} does not exit in kernel keyring.'.format(self._getkeydesc(keyid, keyname))
        super(KeyNotExistError, self).__init__(message)


class KeyAlreadyExistError(KeyctlWrapperException):
    def __init__(self, message=None, keyid=None, keyname=None):
        if message is None:
            message = 'Key {} already exists in kernel keyring.'.format(self._getkeydesc(keyid, keyname))
        super(KeyAlreadyExistError, self).__init__(message)


class KeyctlOperationError(KeyctlWrapperException):
    def __init__(self, message=None, keyid=None, keyname=None, errmsg=None):
        if message is None:
            message = 'Operation on key {} failed. ErrorMsg:{}'.format(self._getkeydesc(keyid, keyname), errmsg)
        super(KeyctlOperationError, self).__init__(message)


# -------------------------------------------------------------------


class KeyctlWrapper(object):
    default_keyring = '@u'
    default_keytype = 'user'

    def __init__(self, keyring: str = default_keyring, keytype: str = default_keytype):
        self.keyring = keyring
        self.keytype = keytype

    # ---------------------------------------------------------------

    @staticmethod
    def _system(args, data: str = None, check=True):

        try:
            p = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                bufsize=4096,
                text=True,
            )
        except OSError as e:
            raise OSError('Command \'{}\' execution failed. ErrMsg:{}'.format(' '.join(args), e))

        if data is None:
            (out, err) = p.communicate()
        else:
            (out, err) = p.communicate(input=data)

        ret = p.returncode

        if not check:
            return ret, out, err
        elif ret == 0:
            return out
        else:
            raise KeyctlOperationError(errmsg='({}){} {}'.format(ret, err, out))

    # ---------------------------------------------------------------

    def get_all_key_ids(self) -> List[int]:
        out = self._system(['keyctl', 'rlist', self.keyring])
        return [int(x) for x in out.split()]

    # ---------------------------------------------------------------

    def get_id_from_name(self, name: str) -> int:
        # ret, out, err = self._system(['keyctl', 'request', self.keytype, name], check=False)
        ret, out, err = self._system(['keyctl', 'search', self.keyring, self.keytype, name], check=False)

        if ret != 0:
            raise KeyNotExistError(keyname=name)

        keyid = int(out.strip())

        return keyid

    # ---------------------------------------------------------------

    def get_name_from_id(self, keyid: int) -> str:
        ret, out, err = self._system(['keyctl', 'rdescribe', str(keyid)], check=False)

        if ret != 0:
            raise KeyNotExistError(keyid=keyid)

        name = ';'.join(out.split(';')[4:])

        return name.rstrip('\n')

    # ---------------------------------------------------------------

    def get_data_from_id(self, keyid: int, mode='raw'):
        if mode.lower() == 'raw':
            kmode = 'pipe'
        elif mode.lower() == 'hex':
            kmode = 'read'
        else:
            raise AttributeError('mode must be one of [\'raw\', \'hex\'].')

        ret, out, err = self._system(['keyctl', kmode, str(keyid)], check=False)

        if ret == 1:
            raise KeyNotExistError(keyid=keyid)

        if mode == 'raw':
            return out
        else:
            # connecting lines to a single line and remove first line
            h = ''.join(out.splitlines()[1:])
            # remove spaces
            return h.replace(' ', '')

    # ---------------------------------------------------------------

    def add_key(self, name: str, data) -> int:
        try:
            keyid = self.get_id_from_name(name)
            raise KeyAlreadyExistError(keyid=keyid, keyname=name)
        except KeyNotExistError:
            pass

        out = self._system(['keyctl', 'padd', self.keytype, name, self.keyring], data)
        keyid = int(out)

        return keyid

    # ---------------------------------------------------------------

    def update_key(self, keyid: int, data):
        ret, out, err = self._system(['keyctl', 'pupdate', str(keyid)], data, check=False)

        if ret == 1:
            raise KeyNotExistError(keyid=keyid)
        elif ret != 0:
            raise KeyctlOperationError(keyid=keyid, errmsg='({}){}'.format(ret, err))

    # ---------------------------------------------------------------

    def remove_key(self, keyid: int):
        # revoke first, because unlinking is slow
        ret, out, err = self._system(['keyctl', 'revoke', str(keyid)], check=False)
        if ret == 1:
            raise KeyNotExistError(keyid=keyid)
        elif ret != 0:
            raise KeyctlOperationError(keyid=keyid, errmsg='({}){}'.format(ret, err))

        self._system(['keyctl', 'unlink', str(keyid), self.keyring])

    # ---------------------------------------------------------------

    def clear_keyring(self):
        self._system(['keyctl', 'clear', self.keyring])

# -------------------------------------------------------------------
