from os import environ
from os.path import expanduser

from bundlewrap.exceptions import FaultUnavailable
from bundlewrap.utils import Fault
from bundlewrap.utils.text import bold, yellow
from bundlewrap.utils.ui import io
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError

DUMMY_MODE = environ.get('BW_KEEPASS_DUMMY_MODE', '0') == '1'
KEEPASS_FILE = environ.get('BW_KEEPASS_FILE', None)
KEEPASS_PASS = environ.get('BW_KEEPASS_PASSWORD', None)

cache = {}


try:
    with open(expanduser('~/.bw_keepass.cfg'), 'r') as f:
        cfg = f.read().splitlines()

        if not KEEPASS_FILE:
            KEEPASS_FILE = cfg[0].strip()

            if not KEEPASS_PASS and len(cfg) > 1:
                KEEPASS_PASS = cfg[1]
except (FileNotFoundError, IndexError):
    pass


def _get_contents_from_keepass(path):
    if not KEEPASS_FILE or not KEEPASS_PASS:
        raise FaultUnavailable('BW_KEEPASS_FILE and/or BW_KEEPASS_PASSWORD missing')

    if isinstance(path, list):
        list_path = path
        string_path = '|'.join(path)
    else:
        list_path = path.split('|')
        string_path = path

    try:
        return cache[string_path]
    except KeyError:
        # Not yet fetched from keepass
        pass

    with io.job('{p}  looking up "{path}" in "{file}"'.format(
        p=bold('KeePass'),
        path=list_path,
        file=KEEPASS_FILE,
    )):
        try:
            keepass = PyKeePass(expanduser(KEEPASS_FILE), KEEPASS_PASS)

            result = keepass.find_entries_by_path(list_path, first=True)
        except CredentialsError:
            raise FaultUnavailable('Your specified BW_KEEPASS_PASSWORD is invalid for use with {}'.format(KEEPASS_FILE))
        except Exception as e:
            raise FaultUnavailable('Exception while trying to get path "{}" from file "{}": {}'.format(
                list_path,
                KEEPASS_FILE,
                repr(e)
            ))

        if not result:
            raise FaultUnavailable('Could not find any entries for path "{}" in file "{}"'.format(
                list_path,
                KEEPASS_FILE,
            ))

        cache[string_path] = result

        return cache[string_path]


def _password(path):
    if DUMMY_MODE:
        return 'KEEPASS DUMMY PASSWORD'
    else:
        secret = _get_contents_from_keepass(path)
        return secret.password


def password(path):
    return Fault(
        'bwkeepass password',
        _password,
        path=path,
    )


def _username(path):
    if DUMMY_MODE:
        return 'KEEPASS DUMMY USERNAME'
    else:
        secret = _get_contents_from_keepass(path)
        return secret.username


def username(path):
    return Fault(
        'bwkeepass username',
        _username,
        path=path,
    )


def _url(path):
    if DUMMY_MODE:
        return 'http://KEEPASS.DUMMY.URL'
    else:
        secret = _get_contents_from_keepass(path)
        return secret.url


def url(path):
    return Fault(
        'bwkeepass url',
        _url,
        path=path,
    )


def _notes(path):
    if DUMMY_MODE:
        return 'KEEPASS DUMMY NOTES'
    else:
        secret = _get_contents_from_keepass(path)
        return secret.notes


def notes(path):
    return Fault(
        'bwkeepass notes',
        _notes,
        path=path,
    )
