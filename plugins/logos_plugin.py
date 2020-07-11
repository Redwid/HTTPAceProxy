# -*- coding: utf-8 -*-
'''
Logo plugin

Logos sources:
https://github.com/Jasmeet181/mediaportal-ru-logos
https://github.com/zag2me/TheLogoDB/tree/master/Images
'''
import hashlib
import os
import urllib

import gevent
import io

from modules.utils import md5

__author__ = 'Redwid'

import time, zlib
import psutil, requests
import logging
from gevent.subprocess import Popen, PIPE
from getmac import get_mac_address
from urllib3.packages.six.moves import getcwdb, map
from urllib3.packages.six import ensure_binary
from requests.compat import json
from requests.utils import re
from utils import query_get

class Logos(object):
    handlers = ('logos',)
    logger = logging.getLogger('logos')

    def __init__(self, AceConfig, AceProxy):
        self.AceConfig = AceConfig
        self.AceProxy = AceProxy

    def handle(self, connection):
        self.logger.info("handle()")
        if connection.splittedpath[1] == 'logos' and connection.splittedpath.__len__() == 3:
            self.logger.info("handle(), path: %s" % connection.splittedpath[2])

            logo_file_name = urllib.unquote(connection.splittedpath[2])
            if connection.command == 'HEAD':
                self.send_image_info(connection, logo_file_name)
            else:
                self.send_image(connection, logo_file_name)
            return

        connection.send_error(404, 'Not Found')

    def send_image_info(self, connection, logo_file_name):
        self.logger.info("send_image_info(%s)" % logo_file_name)

        file_path = 'plugins/config/logos/' + logo_file_name

        if not os.path.exists(file_path):
            self.logger.error("send_image_info(%s) not found" % logo_file_name)
            connection.send_error(404, "Not Found %s" % logo_file_name)

        response_headers = { 'Content-Type': 'image/png',
                             'Accept-Ranges': 'bytes',
                             'Content-Length': os.path.getsize(file_path),
                             'Last-Modified': time.ctime(os.path.getmtime(file_path)),
                             'ETag': md5(file_path),
                             'Connection': 'Close'}

        connection.send_response(200)
        gevent.joinall([gevent.spawn(connection.send_header, k, v) for (k,v) in response_headers.items()])
        connection.end_headers()

    def send_image(self, connection, logo_file_name):
        self.logger.info("send_image(%s)" % logo_file_name)

        file_path = 'plugins/config/logos/' + logo_file_name

        if not os.path.exists(file_path):
            self.logger.error("send_image_info(%s) not found" % logo_file_name)
            connection.send_error(404, "Not Found %s" % logo_file_name)

        if_none_match = connection.headers.get('If-None-Match')
        if if_none_match is not None and if_none_match == md5(file_path):
            logging.debug('[%s]: ETag matches. Return 304 to [%s]' % (self.__class__.__name__, connection.clientip))
            connection.send_response(304)
            connection.send_header('Connection', 'close')
            connection.end_headers()
            return

        with io.open(file_path, 'rb') as content_file:
            exported = content_file.read()

        response_headers = { 'Content-Type': 'image/png',
                             'Content-Length': len(exported)}
        try:
            h = connection.headers.get('Accept-Encoding').split(',')[0]
            self.logger.info("handle(), header: %s" % h)
            compress_method = { 'zlib': zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS),
                                'deflate': zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS),
                                'gzip': zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)}
            exported = compress_method[h].compress(exported) + compress_method[h].flush()
            response_headers = { 'Content-Type': 'image/png',
                                 'Content-Length': len(exported),
                                 'Content-Disposition': 'inline; filename="{}"'.format(logo_file_name),
                                 'Content-Encoding': h }
        except: pass

        connection.send_response(200)
        gevent.joinall([gevent.spawn(connection.send_header, k, v) for (k,v) in response_headers.items()])
        connection.end_headers()
        connection.wfile.write(exported)
        self.logger.info("send_image(), done: %s" % logo_file_name)
