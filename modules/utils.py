'''
Various commonly used functions
'''
__author__ = 'Dorik1972'

from gevent import spawn_later, getcurrent
from urllib3.packages.six.moves.urllib.parse import parse_qs

def schedule(first_run_delay, delay, func, *args, **kw_args):
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


def get_logo(AceConfig, logo_map, name):
    logo_url = logo_map.get(name)

    if logo_url is None:
        name = name.replace(" ", "_").lower()
        logo_url = u'http://{}:{}/logos/{}.png'.format(get_ip(AceConfig), get_port(AceConfig), name)
    return logo_url


def get_epg_url(AceConfig, config_epg, tvgurl):
    if config_epg.updateevery > 0:
        return 'http://{}:{}/epg'.format(get_ip(AceConfig), get_port(AceConfig))
    return tvgurl


def get_ip(AceConfig):
    return '192.168.1.29'#
    #return AceConfig.httphost


def get_port(AceConfig):
    return '8008'#if running from docker that needs to be of exported port your docker container
    #return AceConfig.httpport
