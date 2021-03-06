#-*- coding: utf-8 -*-
'''
Torrenttelik playlist Downloader Plugin
http://ip:port/torrent-telik
'''
__author__ = 'AndreyPavlenko, Dorik1972'

import traceback
import time
import gevent, requests, os
import logging, zlib
from urllib3.packages.six.moves.urllib.parse import urlparse, quote, unquote
from urllib3.packages.six import ensure_str, ensure_text, ensure_binary
from PlaylistGenerator import PlaylistGenerator
from requests_file import FileAdapter
from utils import schedule, query_get, get_logo, get_epg_url
import config.epg_filter as config_epg
import config.torrenttelik as config
import config.picons.torrenttelik as picons

class Torrenttelik(object):

    handlers = ('ttv',)

    def __init__(self, AceConfig, AceProxy):
        self.AceConfig = AceConfig
        self.picons = self.channels = self.playlist = self.etag = self.last_modified = None
        self.playlisttime = gevent.time.time()
        self.headers = {'User-Agent': 'Magic Browser'}
        if config.updateevery: schedule(config.updateevery * 60, self.Playlistparser)

    def Playlistparser(self):
        try:
           s = requests.Session()
           s.mount('file://', FileAdapter())
           for index in range(3):
               try:
                   logging.info("[%s]: get: %s" % (self.__class__.__name__, config.url))
                   with s.get(config.url, headers=self.headers, proxies=config.proxies, stream=False, timeout=30) as playlist:
                      if playlist.status_code != 304:
                         if playlist.encoding is None: playlist.encoding = 'utf-8'
                         playlist = playlist.json()
                         self.headers['If-Modified-Since'] = gevent.time.strftime('%a, %d %b %Y %H:%M:%S %Z', gevent.time.gmtime(self.playlisttime))
                         self.playlist = PlaylistGenerator(m3uchanneltemplate=config.m3uchanneltemplate)
                         self.picons = picons.logomap
                         self.channels = {}
                         m = requests.auth.hashlib.md5()
                         logging.info('[%s]: playlist %s downloaded' % (self.__class__.__name__, config.url))
                         try:
                            urlpattern = requests.utils.re.compile(r'^(acestream|infohash)://[0-9a-f]{40}$|^(http|https)://.*.(acelive|acestream|acemedia|torrent)$')
                            for channel in playlist['channels']:
                               name = channel['name']
                               url = 'acestream://{url}'.format(**channel)
                               channel['group'] = channel.pop('cat')
                               channel['logo'] = self.picons[name] = channel.get('logo', get_logo(picons.logomap, name))

                               if requests.utils.re.search(urlpattern, url):
                                  self.channels[name] = url
                                  channel['url'] = quote(ensure_str(name),'')

                               self.playlist.addItem(channel)
                               m.update(ensure_binary(name))

                         except Exception as e:
                            logging.error("[%s]: can't parse JSON! %s" % (self.__class__.__name__, repr(e)))
                            return False

                         self.etag = '"' + m.hexdigest() + '"'
                         logging.debug('[%s]: plugin playlist generated' % self.__class__.__name__)

                      self.playlisttime = gevent.time.time()
                      logging.info("Return True")
                      return True
               except ValueError:
                   logging.error("[%s]: can't parse %s playlist, attempt: %d" % (self.__class__.__name__, config.url, index + 1))
                   if index + 1 < 3:
                       logging.error("Sleeping")
                       time.sleep((index + 1) * 2)
                       logging.error("Sleeping end")
                   else:
                       logging.error("Return False")
                       return False

        except requests.exceptions.RequestException:
           logging.error("[%s]: can't download %s playlist!" % (self.__class__.__name__, config.url))
           return False
        except:
            logging.error("[%s]: can't parse %s playlist!" % (self.__class__.__name__, config.url))
            logging.error(traceback.format_exc())
            return False

    def handle(self, connection):
        # 30 minutes cache
        if not self.playlist or (gevent.time.time() - self.playlisttime > 30 * 60):
           if not self.Playlistparser():
              logging.info('Parser failed to parse')
              connection.send_error()

        connection.ext = query_get(connection.query, 'ext', 'ts')
        if connection.path.startswith('/{reqtype}/channel/'.format(**connection.__dict__)):
           if not connection.path.endswith(connection.ext):
              logging.info('Invalid path')
              connection.send_error(404, 'Invalid path: {path}'.format(**connection.__dict__), logging.ERROR)
           name = ensure_text(unquote(os.path.splitext(os.path.basename(connection.path))[0]))
           url = self.channels.get(name)
           if url is None:
              logging.info('Unknown channel')
              connection.send_error(404, '[%s]: unknown channel: %s' % (self.__class__.__name__, name), logging.ERROR)
           connection.__dict__.update({'channelName': name,
                                       'channelIcon': self.picons.get(name),
                                       'path': {'acestream': '/content_id/%s/%s.%s' % (urlparse(url).netloc, name, connection.ext),
                                                'infohash' : '/infohash/%s/%s.%s' % (urlparse(url).netloc, name, connection.ext),
                                                'http'     : '/url/%s/%s.%s' % (quote(url,''), name, connection.ext),
                                                'https'    : '/url/%s/%s.%s' % (quote(url,''), name, connection.ext),
                                               }[urlparse(url).scheme]})
           connection.__dict__.update({'splittedpath': connection.path.split('/')})
           connection.__dict__.update({'reqtype': connection.splittedpath[1].lower()})
           return

        elif self.etag == connection.headers.get('If-None-Match'):
           logging.debug('[%s]: ETag matches. Return 304 to [%s]' % (self.__class__.__name__, connection.clientip))
           connection.send_response(304)
           connection.send_header('Connection', 'close')
           connection.end_headers()
           return

        else:
           host_port = connection.headers['Host']
           exported = self.playlist.exportm3u( hostport=host_port,
                                               path='' if not self.channels else '/{reqtype}/channel'.format(**connection.__dict__),
                                               header=config.m3uheadertemplate.format(get_epg_url(host_port, config, config.tvgurl), config.tvgshift),
                                               query=connection.query
                                              )
           response_headers = {'Content-Type': 'audio/mpegurl; charset=utf-8', 'Connection': 'close', 'Access-Control-Allow-Origin': '*'}
           try:
              h = connection.headers.get('Accept-Encoding').split(',')[0]
              compress_method = { 'zlib': zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS),
                                  'deflate': zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS),
                                  'gzip': zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16) }
              exported = compress_method[h].compress(exported) + compress_method[h].flush()
              response_headers['Content-Encoding'] = h
           except: pass
           response_headers['Content-Length'] = len(exported)
           if connection.request_version == 'HTTP/1.1':
              response_headers['ETag'] = self.etag
           connection.send_response(200)
           gevent.joinall([gevent.spawn(connection.send_header, k, v) for (k,v) in response_headers.items()])
           connection.end_headers()
           connection.wfile.write(exported)
           logging.debug('[%s]: plugin sent playlist to [%s]' % (self.__class__.__name__, connection.clientip))
