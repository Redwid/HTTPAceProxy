# -*- coding: utf-8 -*-
'''
This is the example of plugin.
Rename this file to epg_plugin.py to enable it.

To use it, go to http://127.0.0.1:8000/epg
'''
import os
import io
import sys
import time
import zlib
import json
import gevent
import logging
import requests
import traceback

import config.epg_filter as config
from modules.utils import md5
from plugins.epg_filter import EpgFilter
from utils import schedule, query_get
from datetime import datetime


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
            self.etag = md5(self.epg_all_file_name)
        except requests.exceptions.RequestException as e:
            logging.error("ERROR in download_and_filter %s" % (repr(e)))
            return False
        except: logging.error(traceback.format_exc()); return False

        return True

    def handle(self, connection):
        self.logger.info("handle(), headers: %s" % connection.headers)

        if connection.command == 'HEAD':
            self.send_epg_info(connection)
        else:
            self.send_epg(connection)

    def send_epg_info(self, connection):
        self.logger.info("send_epg_info()")

        if self.etag == connection.headers.get('If-None-Match'):
            self.logger.debug('[%s]: ETag matches. Return 304 to [%s]' % (self.__class__.__name__, connection.clientip))
            connection.send_response(304)
            connection.send_header('Connection', 'close')
            connection.end_headers()
            return

        if not os.path.exists(self.epg_all_file_name):
            self.logger.error("send_epg_info(%s) not found" % self.epg_all_file_name)
            connection.send_error(404, "Not Found %s" % self.epg_all_file_name)

        response_headers = { 'Content-Type': 'image/png',
                             'Accept-Ranges': 'bytes',
                             'Content-Length': os.path.getsize(self.epg_all_file_name),
                             'Last-Modified': time.ctime(os.path.getmtime(self.epg_all_file_name)),
                             'ETag': self.etag,
                             'Connection': 'Close'}

        connection.send_response(200)
        gevent.joinall([gevent.spawn(connection.send_header, k, v) for (k,v) in response_headers.items()])
        connection.end_headers()

    def send_epg(self, connection):
        self.logger.info("send_epg()")
        # config.updateevery * 60 minutes cache
        if not self.epg_all_file_name or not os.path.exists(self.epg_all_file_name) or (gevent.time.time() - self.last_time > config.updateevery * 60):
            if not self.download_and_filter(): connection.send_error()

        if self.etag == connection.headers.get('If-None-Match'):
            self.logger.info("send_epg(), ETag matches. Return 304 to [%s]" % connection.clientip)
            connection.send_response(304)
            connection.send_header('Connection', 'close')
            connection.end_headers()
            return

        if_modified_since = connection.headers.get('If-Modified-Since')
        epg_all_file_time = datetime.fromtimestamp(os.path.getmtime(self.epg_all_file_name))
        epg_all_file_time = epg_all_file_time.replace(microsecond=0)
        epg_all_file_last_modified = epg_all_file_time.strftime('%a, %d %b %Y %H:%M:%S %Z')
        if if_modified_since is not None:
            header_time = self.get_header_time(if_modified_since)
            self.logger.info("If-Modified-Since: [%s], time: [%s]" % (if_modified_since, header_time))
            self.logger.info("epg_all_file_time: [%s], time: [%s]" % (epg_all_file_last_modified, epg_all_file_time))
            if header_time >= epg_all_file_time:
                self.logger.info("send_epg(), If-Modified-Since matches. Return 304 to [%s]" % connection.clientip)
                connection.send_response(304)
                connection.send_header('Connection', 'close')
                connection.end_headers()
                return

        with io.open(self.epg_all_file_name, encoding='utf-8') as content_file:
            exported = content_file.read().encode('utf-8')

        response_headers = { 'Content-Type': 'text/html',
                             'Connection': 'close',
                             'Content-Length': len(exported),
                             'Last-Modified': epg_all_file_last_modified,
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
        self.logger.info("send_epg() done")

    def get_header_time(self, header_time):
        formats = ['%a, %d %b %Y %H:%M:%S %Z', '%a %d %b %Y %H:%M:%S']
        for item in formats:
            try:
                return datetime.strptime(header_time, item)
            except: pass
        return None


