# -*- coding: utf-8 -*-
'''
This is the example of plugin.
Rename this file to epg_plugin.py to enable it.

To use it, go to http://127.0.0.1:8000/epg
'''
import os
import io
import sys
import zlib
import json
import gevent
import logging
import requests
import traceback

import config.epg_filter as config
from plugins.epg_filter import EpgFilter
from utils import schedule, query_get


class Epg(object):
    handlers = ('epg', )

    def __init__(self, AceConfig, AceProxy):
        self.AceConfig = AceConfig
        self.AceProxy = AceProxy
        self.logger = logging.getLogger('epg_plugin')
        self.epg_all_file_name = None
        self.etag = None
        self.headers = {'User-Agent': 'Magic Browser'}
        if config.updateevery:
            schedule(60, config.updateevery * 60, self.download_and_filter)
        pass

    def download_and_filter(self):
        try:
            epg_filter = EpgFilter(self.AceConfig, self.AceProxy)
            self.epg_all_file_name = epg_filter.download()
            self.last_time = gevent.time.time()
        except requests.exceptions.RequestException as e:
            logging.error("ERROR in download_and_filter %s" % (repr(e)))
            return False
        except: logging.error(traceback.format_exc()); return False

        return True

    def handle(self, connection):
        self.logger.info("handle(), headers: %s" % connection.headers)

        # config.updateevery * 60 minutes cache
        if not self.epg_all_file_name or not os.path.exists(self.epg_all_file_name) or (gevent.time.time() - self.last_time > config.updateevery * 60):
            if not self.download_and_filter(): connection.send_error()

        with io.open(self.epg_all_file_name, encoding='utf-8') as content_file:
            exported = content_file.read().encode('utf-8')

        response_headers = { 'Content-Type': 'text/html',
                             'Connection': 'close',
                             'Content-Length': len(exported),
                             'Content-Disposition': 'inline; filename="epg-all.xml"'}
        try:
            h = connection.headers.get('Accept-Encoding').split(',')[0]
            self.logger.info("handle(), header: %s" % h)
            compress_method = { 'zlib': zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS),
                                'deflate': zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS),
                                'gzip': zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16) }
            exported = compress_method[h].compress(exported) + compress_method[h].flush()
            response_headers['Content-Length'] = len(exported)
            response_headers['Content-Encoding'] = h
        except: pass

        connection.send_response(200)
        gevent.joinall([gevent.spawn(connection.send_header, k, v) for (k,v) in response_headers.items()])
        connection.end_headers()

        connection.wfile.write(exported)



