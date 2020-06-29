# -*- coding: utf-8 -*-
'''
Logo plugin

Logos sources:
https://github.com/Jasmeet181/mediaportal-ru-logos
https://github.com/zag2me/TheLogoDB/tree/master/Images
'''
import os

import gevent
import io

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
        path_file_ext = connection.path[connection.path.rfind('.') + 1:]
        if connection.splittedpath[1] == 'logos' and connection.splittedpath.__len__() == 2:
            self.logger.info("handle(), path_file_ext: %s" % path_file_ext)
            query_components = dict(qc.split("=") for qc in connection.query.split("&"))
            self.logger.info("handle(), query_components: %s" % query_components)
            if query_components['c']:
                self.logger.info("handle(), query_components: %s" % query_components['c'])
                self.send_image(query_components['c'], connection)
                return

        connection.send_error(404, 'Not Found')

    def send_image(self, logo_name, connection):
        self.logger.info("send_image(%s)" % logo_name)

        file_path = 'plugins/config/logos/' + logo_name + '.png'

        if not os.path.exists(file_path):
            connection.send_error(404, "Not Found %s" % logo_name)

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
                                 'Content-Disposition': 'inline; filename="{}.png"'.format(logo_name),
                                 'Content-Encoding': h }
        except: pass

        connection.send_response(200)
        gevent.joinall([gevent.spawn(connection.send_header, k, v) for (k,v) in response_headers.items()])
        connection.end_headers()
        connection.wfile.write(exported)
        self.logger.info("send_image(), done: %s.svg" % logo_name)
