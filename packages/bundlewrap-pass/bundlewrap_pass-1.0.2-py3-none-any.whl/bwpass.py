from os import environ
from os.path import expanduser
from subprocess import check_output, CalledProcessError

from bundlewrap.exceptions import FaultUnavailable
from bundlewrap.utils import Fault
from bundlewrap.utils.dicts import merge_dict
from bundlewrap.utils.text import bold, yellow
from bundlewrap.utils.ui import io

ENVIRONMENT = merge_dict(environ, {
    'PASSWORD_STORE_DIR': expanduser(environ.get('BW_PASS_DIR', '~/.password-store')),
})

DUMMY_MODE = environ.get('BW_PASS_DUMMY_MODE', '0') == '1'

cache = {}


def _get_contents_from_pass(identifier: str):
    try:
        return cache[identifier]
    except KeyError:
        # Not yet fetched from pass
        pass

    with io.job('{p}  fetching {identifier}'.format(
        p=bold('pass'),
        identifier=identifier,
    )):
        try:
            pass_output = check_output(
                ['pass', 'show', identifier],
                env=ENVIRONMENT,
            ).decode('UTF-8').splitlines()
        except FileNotFoundError:
            raise FaultUnavailable('pass not found')
        except CalledProcessError as e:
            raise FaultUnavailable('pass exited {} when trying to get secret "{}"'.format(
                e.returncode,
                identifier,
            ))

        if not pass_output:
            raise ValueError('BUG: `pass show {}` did not return any output!'.format(
                identifier
            ))

        cache[identifier] = {
            'password': pass_output[0].strip(),
            'attrs': {},
        }

        if len(pass_output) > 1:
            for line in pass_output[1:]:
                if not ':' in line:
                    continue

                attr, value = line.split(':', 1)

                cache[identifier]['attrs'][attr] = value.strip()

        return cache[identifier]


def _password(identifier):
    if DUMMY_MODE:
        return 'PASS DUMMY PASSWORD'
    else:
        secret = _get_contents_from_pass(identifier)
        return secret['password']


def password(identifier):
    return Fault(
        'bwpass password',
        _password,
        identifier=identifier,
    )


def _attr(identifier, attr):
    if DUMMY_MODE:
        return 'PASS DUMMY {} ATTRIBUTE'.format(attr)
    else:
        secret = _get_contents_from_pass(identifier)
        try:
            return secret['attrs'][attr]
        except KeyError:
            raise FaultUnavailable('attribute {} not found for identifier {}'.format(
                attr,
                identifier,
            ))


def attr(identifier, attr):
    return Fault(
        'bwpass attribute {}'.format(attr),
        _attr,
        identifier=identifier,
        attr=attr,
    )
