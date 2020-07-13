'''
Various commonly used functions
'''
import hashlib

__author__ = 'Dorik1972'

from gevent import spawn_later, getcurrent
from urllib3.packages.six.moves.urllib.parse import parse_qs


def schedule(delay, func, *args, **kw_args):
    '''
    Run a function at repeated intervals
    '''
    spawn_later(0, func, *args, **kw_args)
    spawn_later(delay, schedule, delay, func, *args, **kw_args)


def schedule_with_first_run_delay(first_run_delay, delay, func, *args, **kw_args):
    '''
    Run a function at repeated intervals
    '''
    spawn_later(first_run_delay, func, *args, **kw_args)
    spawn_later(delay, schedule, delay, func, *args, **kw_args)


def query_get(query, key, default=''):
    '''
    Helper for getting values from a pre-parsed query string
    '''
    return parse_qs(query).get(key, [default])[0]


def get_logo(logo_map, name):
    logo_url = logo_map.get(name)

    if logo_url is None:
        name = name.replace(" ", "_").lower()
        logo_url = u'http://127.0.0.1/logos/{}.png'.format(name)
    return logo_url


def get_epg_url(host_port, config_epg, tvgurl):
    if config_epg.updateevery > 0:
        return 'http://{}/epg'.format(host_port)
    return tvgurl


def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

