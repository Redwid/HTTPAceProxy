# -*- coding: utf-8 -*-
"""
Epg filter class
"""
import codecs
import datetime
import os
import json
import time

from sh import gunzip
# import xml.etree.ElementTree as ET #cElementTree using c implementation and works faster
import xml.etree.cElementTree as ET


from plugins.model.model_items import NameItem, ChannelItem, ProgrammeItem, M3uItem

__author__ = 'Redwid'

import logging, requests

# EPG urls
# http://epg.ott-play.com/
tv_epg_urls = ['https://iptvx.one/epg/epg.xml.gz',
               'http://www.teleguide.info/download/new3/xmltv.xml.gz',
               'http://programtv.ru/xmltv.xml.gz',
               'http://epg.it999.ru/edem.xml.gz']
# 'http://epg.openboxfan.com/xmltv-t-sd.xml.gz']
# tv_epg_urls = ['http://epg.it999.ru/edem.xml.gz']

# Path to store files
destination_file_path_local = './'

# Cache folder
cache_folder = '.cache'

# Replacement map for channels
# [list_to_check in xml][list_to_insert in m3u ]
replacement_map = [
    [[u'Animal Planet'], u'Animal Planet HD'],
    [[u'Da Vinci', u'Да Винчи'], u'Da Vinci'],
    [[u'Discovery Россия'], u'Discovery Россия HD'],
    [[u'Candy', u'Candy 3D HD'], u'Candy HD'],
    [[u'Dorcel'], u'Dorcel HD'],
    [[u'HD Life', u'HDL'], u'HD-Life'],
    [[u'National Geographic'], u'National Geographic HD'],
    [[u'TLC', u'TLC HD'], u'TLC Россия'],
    [[u'Travel Channel'], u'Travel channel HD'],
    [[u'Travel+Adventure'], u'Travel+Adventure HD'],
    [[u'Outdoor channel', u'Outdoor HD'], u'Outdoor channel HD'],
    [[u'History2', u'H2 HD'], u'History2 HD'],
    [[u'Живая природа'], u'Живая природа HD'],
    [[u'Россия-Планета (Европа)', u'РТР-Планета Европа'], u'РТР-Планета'],
    [[u'Cartoon Network', u'Cartoon Network HD'], u'Cartoon network'],
    [[u'7 канал'], u'7 канал (Казахстан)'],
    [[u'Беларусь 1 HD'], u'Беларусь 1'],
    [[u'Беларусь 2 HD'], u'Беларусь 2'],
    [[u'Беларусь 3 HD'], u'Беларусь 3'],
    [[u'Беларусь 5 HD'], u'Беларусь 5'],
    [[u'Интер', u'Iнтер'], u'Интер'],
    [[u'Paramount Channel HD'], u'Paramount Сhannel HD'],
    [[u'НТВ-Мир'], u'НТВ Мир'],
    [[u'Мир', u'Мир HD'], u'МирТВ'],
    [[u'Мир Premium'], u'Мир HD'],
    [[u'Астана'], u'Астана ТВ'],
    [[u'Первый HD +4'], u'Первый канал HD (+4)'],
    [[u'Первый канал +2'], u'Первый канал (+2)'],
    [[u'5 канал Россия'], u'5 канал (Россия)'],
    [[u'Техно 24', u'24 Техно'], u'24Техно'],
    [[u'Россия 1 +2'], u'Россия 1 (+2)'],
    [[u'BBC', u'BBC World News'], u'BBC World News Europe'],
    [[u'О!'], u'Канал О!'],
    [[u'НСТ', u'НСТ Страшное'], u'НСТ (Страшное)'],
    [[u'Sony Sci-Fi'], u'AXN Sci-Fi'],
    [[u'TiJi'], u'TiJi Россия'],
    [[u'Шант Premium HD', u'Shant Premium HD'], u'Shant HD'],
    [[u'9 канал Израиль'], u'9 канал (Израиль)'],
    [[u'History Russia'], u'History Россия HD'],
    [[u'Nu.ART TV', u'Ню Арт'], u'Nuart'],
    [[u'VH1', u'VH1 European'], u'VH1 Europe'],
    [[u'Viasat Sport HD'], u'Viasat Sport HD Россия'],
    [[u'Матч! HD', u'Матч HD', u'МатчТВ HD'], u'Матч ТВ HD'],
    [[u'Наш футбол HD', u'Матч Премьер'], u'НТВ+ Наш футбол HD'],
    [[u'RT Д Русский'], u'RT Д HD'],
    [[u'Hustler HD'], u'Hustler HD Europe'],
    [[u'Шансон-TB'], u'Шансон ТВ'],
    [[u'НТВ +2'], u'НТВ (+2)'],
    [[u'НТВ'], u'НТВ HD'],
    [[u'ОНТ', u'ОНТ HD'], u'ОНТ Беларусь'],
    [[u'Первый канал', u'Первый HD'], u'Первый канал HD'],
    [[u'Рен ТВ', u'РенТВ'], u'РЕН ТВ'],
    [[u'Россия 1 HD'], u'Россия HD'],
    [[u'ТНТ'], u'ТНТ HD'],
    [[u'Disney'], u'Канал Disney'],
    [[u'A HOME OF HBO 1', u'Amedia Hit'], u'Amedia Hit HD'],
    [[u'A HOME OF HBO 2', u'Amedia Premium HD'], u'Amedia Premium'],
    [[u'Fox Life', u'FoxLife'], u'Fox Life Россия'],
    [[u'Fox', u'Fox HD'], u'Fox Россия'],
    [[u'Paramount Comedy'], u'Paramount Comedy Россия'],
    [[u'TV1000', u'TV 1000 East'], u'TV1000 East'],
    [[u'TV1000 Comedy', u'VIP Comedy'], u'ViP Comedy HD'],
    [[u'TV1000 Premium HD', u'VIP Premiere HD'], u'ViP Premiere HD'],
    [[u'Дом кино Премиум'], u'Дом кино Премиум HD'],
    [[u'КиноТВ', u'Кино ТВ'], u'КиноТВ HD'],
    [[u'Шокирующее'], u'Кинопоказ HD1'],
    [[u'Комедийное'], u'Кинопоказ HD2'],
    [[u'Наш детектив', u'Наше крутое HD'], u'Наш Детектив HD'],
    [[u'Наш кинороман'], u'Наш Кинороман HD'],
    [[u'Кинопремьера'], u'Кинопремьера HD'],
    [[u'TV XXI', u'TV21'], u'ТВ XXI'],
    [[u'Европа Плюс ТВ'], u'Europa Plus TV'],
    [[u'MTV Russia'], u'MTV Россия'],
    [[u'Матч! Игра', u'Матч Игра'], u'Матч! Игра HD'],
    [[u'Матч! Арена', u'Матч Арена'], u'Матч! Арена HD'],
    [[u'Матч! Футбол 1', u'Матч Футбол 1'], u'Матч! Футбол 1 HD'],
    [[u'Матч! Футбол 2', u'Матч Футбол 2'], u'Матч! Футбол 2 HD'],
    [[u'Матч! Футбол 3', u'Матч Футбол 3'], u'Матч! Футбол 3 HD'],
    [[u'Сетанта Спорт + HD', u'Setanta Sports'], u'Сетанта Спорт HD'],
    [[u'Setanta Sports+', u'Сетанта Спорт+'], u'Сетанта Спорт + HD'],
    [[u'Eurosport 2'], u'Eurosport 2 HD'],
    [[u'А1', u'Amedia 1 HD'], u'A1'],
    [[u'TV3 LT', u'TV3 Литва'], u'TV3'],
    [[u'LRT Televizija'], u'LRT'],
    [[u'ТВ3', u'ТВ-3'], u'ТВ3 Россия'],
    [[u'Мульт и музыка', u'МультиМузыка'], u'Страна'],
    [[u'В мире животных HD'], u'Animal Family HD'],
    [[u'Эврика HD'], u'Eureka HD'],
    [[u'Russia Today'], u'RT Д HD'],
    [[u'Viasat Explore'], u'Viasat Explorer'],
    [[u'Eurosport 1 HD'], u'Eurosport HD'],
    [[u'Армения ТВ'], u'Armenia TV'],
    [[u'ID Xtra RU'], u'ID Xtra Россия'],
    [[u'М1 Украина'], u'M1'],
    [[u'Kentron TV'], u'Kentron'],
    [[u'Россия К'], u'Культура'],
    [[u'Extreme sport'], u'Extreme Sports'],
    [[u'KAZsport'], u'Kazsport']
]

class EpgFilter(object):

    def __init__(self, AceConfig, AceProxy):
        self.AceConfig = AceConfig
        self.logger = logging.getLogger('epg_plugin')
        pass

    def get_destination_file_path(self):
        return destination_file_path_local

    def insert_value_if_needed(self, list, list_to_check, value_to_insert):
        for value0 in list:
            if value0.text in list_to_check:
                value = self.get_value_from_list(value_to_insert, list)
                if value is None:
                    list.insert(0, NameItem(value_to_insert))
                else:
                    list.remove(value)
                    list.insert(0, value)
                return True
        return False

    def add_custom_entries(self, channel_item):
        channel_list = channel_item.display_name_list

        for item in replacement_map:
            if self.insert_value_if_needed(channel_list, item[0], item[1]):
                if item[1] == u'МирТВ':
                    self.delete_from_list(channel_list, u'Мир HD')
                return

        pass

    def delete_from_list(self, list, item):
        value = self.get_value_from_list(item, list)
        if value is not None:
            list.remove(value)

    def get_value_from_list(self, value, list):
        for item in list:
            if item.text == value:
                return item

        return None

    def download_file(self, url, file_name):
        self.logger.info("download_file(%s, %s)" % (url, file_name))

        destination_file_path_cache_folder = self.get_destination_file_path() + cache_folder
        file_name = destination_file_path_cache_folder + '/' + file_name
        file_name_no_gz = file_name.replace('.gz', '')

        etag_file_name, file_extension = os.path.splitext(file_name)
        etag_file_name = etag_file_name + '.etag'
        data = self.load_last_modified_data(etag_file_name)
        headers = {}
        if data is not None:
            file_name_no_gz = file_name.replace('.gz', '')
            if os.path.exists(file_name_no_gz):
                if 'etag' in data:
                    headers['If-None-Match'] = data['etag']
                if data['last_modified'] != 'None':
                    headers['If-Modified-Since'] = data['last_modified']

        if not os.path.exists(destination_file_path_cache_folder):
            os.makedirs(destination_file_path_cache_folder)

        get_response = requests.get(url, headers=headers, verify=False, timeout=(5,30))
        if get_response.status_code == 304:
            self.logger.info("download_file() ignore as file 'Not Modified'")
            return file_name_no_gz

        self.store_last_modified_data(etag_file_name, get_response.headers)

        self.logger.info("download_file() downloading file_name: %s" % (file_name))
        with open(file_name, 'wb') as f:
            for chunk in get_response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        self.logger.info("download_file done: %s, file size: %d" % (file_name, os.path.getsize(file_name)))
        return file_name

    def store_last_modified_data(self, file_name, headers):
        self.logger.info("store_last_modified_data(%s)" % (file_name))

        data = {'etag': str(headers.get('ETag')), 'last_modified' : str(headers.get('Last-Modified'))}
        self.logger.info("store_last_modified_data(), data: %s" % (str(data)))
        with codecs.open(file_name, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(data))

    def load_last_modified_data(self, file_name):
        try:
            with codecs.open(file_name, encoding='utf-8') as json_file:
                data = json.load(json_file)
                return data
        except:
            self.logger.error("ERROR can\'t read file: %s" % (file_name))
        return None

    def get_m3u_url(self):
        return 'http://{}:{}/ttv'.format(self.AceConfig.httphost, self.AceConfig.httpport)

    def download_m3u(self):
        self.logger.info('download_m3u()')
        file_name = self.download_file(self.get_m3u_url(), 'm3u.m3u')
        self.logger.info('download_m3u() done')
        return file_name

    def download_all_epgs(self):
        self.logger.info("download_all_epgs()")
        start_time = time.time()
        index = 1
        downloaded_list = []
        for url in tv_epg_urls:
            self.download_epg(index, url, downloaded_list)
            index = index + 1
        self.logger.info("download_all_epgs(), done, time: %sms" % (time.time() - start_time))
        return downloaded_list

    def download_epg(self, index, url, downloaded_list):
        self.logger.info("download_epg(%s)" % url)
        start_time = time.time()
        file_name = 'epg-' + str(index) + '.xml.gz'
        try:
            file_name = self.download_file(url, file_name)

            if file_name.endswith('.gz'):
                xml_file_name = file_name.replace('.gz', '')
                if os.path.exists(xml_file_name):
                    os.remove(xml_file_name)
                gunzip(file_name)
                file_name = xml_file_name

            downloaded_list.append(file_name)
        except Exception as e:
            self.logger.error('ERROR in download_epg(%s) %s' % (url, e))
        self.logger.info("download_epg(%s), xml size: %s, time: %sms" % (url, self.sizeof_fmt(os.path.getsize(file_name)), time.time() - start_time))

    def load_xmlt(self, m3u_entries, epg_file, channel_list, programme_list):
        self.logger.info("load_xmlt(%s)" % epg_file)
        start_time = time.time()

        start_time_0 = time.time()
        tree = ET.parse(epg_file)
        root = tree.getroot()
        self.logger.info("load_xmlt(%s), parsing, time: %sms " % (epg_file, time.time() - start_time_0))

        start_time_0 = time.time()
        for item in root.findall('./channel'):
            channel_item = ChannelItem(item)

            self.add_custom_entries(channel_item)

            value = self.is_channel_present_in_list_by_name(channel_list, channel_item)
            channel_in_m3u = self.is_channel_present_in_m3u(channel_item, m3u_entries)
            if value is None and channel_in_m3u:
                channel_list.append(channel_item)

            # if value is not None and channel_in_m3u:
            #     merge_values(value, channel_item)
        self.logger.info("load_xmlt(%s), channel parsing, time: %sms " % (epg_file, time.time() - start_time_0))

        start_time_0 = time.time()
        for item in root.findall('./programme'):
            if self.is_channel_present_in_list_by_id(channel_list, item.attrib['channel']):
                program_item = ProgrammeItem(item)
                programme_list.append(program_item)
        self.logger.info("load_xmlt(%s), programme parsing, time: %sms " % (epg_file, time.time() - start_time_0))

        self.logger.info("load_xmlt(%s), channel_list size: %d, programme_list: %d, time: %sms " % (epg_file, len(channel_list), len(programme_list), time.time() - start_time))

    def merge_values(self, channel_0, channel_1):
        display_name_list_0 = channel_0.display_name_list
        display_name_list_1 = channel_1.display_name_list
        for name_1 in display_name_list_1:
            if name_1 not in display_name_list_0:
                display_name_list_0.append(name_1)

        if 'icon' not in display_name_list_0 and 'icon' in display_name_list_1:
            display_name_list_0.icon = display_name_list_1.icon

    def download_and_parse_m3u(self):
        self.logger.info("download_and_parse_m3u()")

        m3u_entries = []
        for i in range(5):
            m3u_filename = self.download_file(self.get_m3u_url(), 'm3u.m3u')
            self.logger.info("download_and_parse_m3u() download done: #%d" % (i))

            m3u_file = codecs.open(m3u_filename, 'r', encoding='utf-8')
            line = m3u_file.readline()

            if '#EXTM3U' not in line:
                self.logger.error('ERROR in download_and_parse_m3u(), file does not start with #EXTM3U, #%d', i)
                continue

            entry = M3uItem(None)

            for line in m3u_file:
                line = line.strip()
                if line.startswith('#EXTINF:'):
                    m3u_fields = line.split('#EXTINF:-1 ')[1]
                    entry = M3uItem(m3u_fields)
                elif len(line) != 0:
                    entry.url = line
                    if M3uItem.is_valid(entry, True):
                        m3u_entries.append(entry)
                    entry = M3uItem(None)

            m3u_file.close()
            break

        self.logger.info("download_and_parse_m3u(), m3u_entries size: %d" % (len(m3u_entries)))
        return m3u_entries

    def is_channel_present_in_m3u(self, channel_item, m3u_entries):
        list = channel_item.display_name_list
        for value in m3u_entries:
            for display_name in list:
                #if 'Paramount Сhannel HD' == value['tvg-name']:
                #    print('!')
                if self.compare(display_name.text, value.name) or self.compare(display_name.text, value.tvg_name):
                    return True
        return False

    def is_channel_present_in_list_by_id(self, channel_list, channel_item):
        for value in channel_list:
            if value.id == channel_item:
                return True
        return False

    def is_channel_present_in_list_by_name(self, channel_list, channel_item):
        list0 = channel_item.display_name_list
        for channel in channel_list:
            list1 = channel.display_name_list
            for name1 in list0:
                for name2 in list1:
                    if self.compare(name1.text, name2.text):
                        return channel
        return None


    def compare(self, string1, string2):
        # if type(string1) is dict:
        #     string1 = string1['text']

        # if type(string1) is ChannelItem:
        #     string1 = string1.text

        # if type(string1) is NameItem:
        #     string1 = string1.text

        # if type(string2) is dict:
        #     string2 = string2['text']

        # if type(string2) is ChannelItem:
        #     string2 = string2.text
        #
        # if type(string2) is NameItem:
        #     string2 = string2.text

        if string1 == string2 or string1.lower() == string2.lower():
            return True

        return False

    def write_xml(self, channel_list, programme_list):
        self.logger.info("write_xml()")

        tv = ET.Element("tv")

        for channel_item in channel_list:
            channel_item.to_et_sub_element(tv)

        destination_file_path_cache_folder = self.get_destination_file_path() + cache_folder
        try:
            channels_tree = ET.ElementTree(tv)
            channels_tree.write(destination_file_path_cache_folder + '/channels.xml', encoding='utf-8', xml_declaration=True)
            self.logger.info("write_xml() channels, %d" % (len(channel_list)))
        except Exception as e:
            self.logger.error('ERROR in write_xml()', exc_info=True)

        for programme in programme_list:
            programme.to_et_sub_element(tv)

        tree = ET.ElementTree(tv)

        file_path = self.get_destination_file_path() + cache_folder + '/epg-all.xml'

        if os.path.exists(file_path):
            os.remove(file_path)

        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        file_size = os.path.getsize(file_path)
        self.logger.info("write_xml(%s) done, file size: %s (%s)" % (file_path, file_size, self.sizeof_fmt(file_size)))
        return file_path

    def sizeof_fmt(self, num, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def load_cached_channels(self, m3u_entries):
        self.logger.info("load_cached_channels()")
        destination_file_path_cache_folder = self.get_destination_file_path() + cache_folder

        counter_cached = 0
        try:
            tree = ET.parse(destination_file_path_cache_folder + '/channels.xml')
            root = tree.getroot()

            for item in root.findall('./channel'):
                channel_item = ChannelItem(item)
                channel_in_m3u = self.is_channel_present_in_m3u(channel_item, m3u_entries)
                if not channel_in_m3u:
                    name = channel_item.get_display_name()
                    try:
                        m3u_entries.append(M3uItem('tvg-name="{}" tvg-id="{}",{}'.format(name, channel_item.id, name.text)))
                    except Exception as e:
                        self.logger.error('ERROR in load_old_channels()', exc_info=True)

                    self.logger.info("load_cached_channels(), channel_in_m3u, name: %s" % (name))
                    counter_cached = counter_cached + 1
        except Exception as e:
            self.logger.error('ERROR in load_old_channels()', exc_info=True)
        self.logger.info("load_cached_channels(), counter_cached: %d" % (counter_cached))

    def download(self):
        self.logger.info("download()")
        start_time = time.time()

        all_m3u_entries = self.download_and_parse_m3u()
        self.load_cached_channels(all_m3u_entries)

        downloaded = self.download_all_epgs()

        channel_list = []
        programme_list = []
        for file in downloaded:
            self.load_xmlt(all_m3u_entries, file, channel_list, programme_list)

        self.logger.info("Not preset:")
        counter = 0
        for value in all_m3u_entries:

            # if 'Paramount Сhannel HD' == value.tvg_name:
            #     print('!')
            found = False
            for channel in channel_list:
                found = False
                display_name_list = channel.display_name_list
                for display_name in display_name_list:
                    if self.compare(display_name.text, value.name) or self.compare(display_name.text, value.tvg_name):
                        found = True
                        break
                if found:
                    break
            if not found:
                # str_value = str(value)
                self.logger.info("  %s" % (unicode(value)))
                counter = counter + 1
        self.logger.info("Not preset, counter: %s" % (str(counter)))

        # print('Empty:')
        # for programme in programme_list:
        #     title_list = programme['titles']
        #     if title_list:
        #         pass
        #     else:
        #         print(programme)
        #
        #     desc_list = programme['descs']
        #     if desc_list:
        #         pass
        #     else:
        #         print(programme)

        file_path = self.write_xml(channel_list, programme_list)

        self.logger.info("download(), done in: %s" % (time.time() - start_time))
        return file_path
