# -*- coding: utf-8 -*-
from plugins.model.model_items import NameItem

replace_map = [
        [[u"Animal Planet"], u"Animal Planet HD"],
        [[u"Da Vinci", u"Да Винчи"], u"Da Vinci"],
        [[u"Discovery Россия"], u"Discovery Россия HD"],
        [[u"Candy", u"Candy 3D HD"], u"Candy HD"],
        [[u"Dorcel"], u"Dorcel HD"],
        [[u"HD Life", u"HDL"], u"HD-Life"],
        [[u"National Geographic"], u"National Geographic HD"],
        [[u"TLC", u"TLC HD"], u"TLC Россия"],
        [[u"Travel Channel"], u"Travel channel HD"],
        [[u"Travel+Adventure"], u"Travel+Adventure HD"],
        [[u"Outdoor channel", u"Outdoor HD"], u"Outdoor channel HD"],
        [[u"History2", u"H2 HD"], u"History2 HD"],
        [[u"Живая природа"], u"Живая природа HD"],
        [[u"Россия-Планета (Европа)", u"РТР-Планета Европа"], u"РТР-Планета"],
        [[u"Cartoon Network", u"Cartoon Network HD"], u"Cartoon network"],
        [[u"7 канал"], u"7 канал (Казахстан)"],
        [[u"Беларусь 1 HD"], u"Беларусь 1"],
        [[u"Беларусь 2 HD"], u"Беларусь 2"],
        [[u"Беларусь 3 HD"], u"Беларусь 3"],
        [[u"Беларусь 5 HD"], u"Беларусь 5"],
        [[u"Интер", u"Iнтер"], u"Интер"],
        [[u"Paramount Channel HD"], u"Paramount Сhannel HD"],
        [[u"НТВ-Мир"], u"НТВ Мир"],
        [[u"Мир", u"Мир HD"], u"МирТВ"],
        [[u"Мир Premium"], u"Мир HD"],
        [[u"Астана"], u"Астана ТВ"],
        [[u"Первый HD +4"], u"Первый канал HD (+4)"],
        [[u"Первый канал +2"], u"Первый канал (+2)"],
        [[u"5 канал Россия"], u"5 канал (Россия)"],
        [[u"Техно 24"], u"24Техно"],
        [[u"Россия 1 +2"], u"Россия 1 (+2)"],
        [[u"BBC", u"BBC World News"], u"BBC World News Europe"],
        [[u"О!"], u"Канал О!"],
        [[u"НСТ", u"НСТ Страшное"], u"НСТ (Страшное)"],
        [[u"Sony Sci-Fi"], u"AXN Sci-Fi"],
        [[u"TiJi"], u"TiJi Россия"],
        [[u"Шант Premium HD", u"Shant Premium HD"], u"Shant HD"],
        [[u"9 канал Израиль"], u"9 канал (Израиль)"],
        [[u"History Russia"], u"History Россия HD"],
        [[u"Nu.ART TV", u"Ню Арт"], u"Nuart"],
        [[u"VH1", u"VH1 European"], u"VH1 Europe"],
        [[u"Viasat Sport HD"], u"Viasat Sport HD Россия"],
        [[u"Матч! HD", u"Матч HD", u"МатчТВ HD"], u"Матч ТВ HD"],
        [[u"Наш футбол HD"], u"НТВ+ Наш футбол HD"],
        [[u"RT Д Русский"], u"RT Д HD"],
        [[u"Hustler HD"], u"Hustler HD Europe"],
        [[u"Шансон-TB"], u"Шансон ТВ"],
        [[u"НТВ +2"], u"НТВ (+2)"],
        [[u"НТВ"], u"НТВ HD"],
        [[u"ОНТ", u"ОНТ HD"], u"ОНТ Беларусь"],
        [[u"Первый канал", u"Первый HD"], u"Первый канал HD"],
        [[u"Рен ТВ", u"РенТВ"], u"РЕН ТВ"],
        [[u"Россия 1 HD"], u"Россия HD"],
        [[u"ТНТ"], u"ТНТ HD"],
        [[u"Disney"], u"Канал Disney"],
        [[u"A HOME OF HBO 1", u"Amedia Hit"], u"Amedia Hit HD"],
        [[u"A HOME OF HBO 2", u"Amedia Premium HD"], u"Amedia Premium"],
        [[u"Fox Life", u"FoxLife"], u"Fox Life Россия"],
        [[u"Fox", u"Fox HD"], u"Fox Россия"],
        [[u"Paramount Comedy"], u"Paramount Comedy Россия"],
        [[u"TV1000", u"TV 1000 East"], u"TV1000 East"],
        [[u"TV1000 Comedy", u"VIP Comedy"], u"ViP Comedy HD"],
        [[u"TV1000 Premium HD", u"VIP Premiere HD"], u"ViP Premiere HD"],
        [[u"Дом кино Премиум"], u"Дом кино Премиум HD"],
        [[u"КиноТВ", u"Кино ТВ"], u"КиноТВ HD"],
        [[u"Шокирующее"], u"Кинопоказ HD1"],
        [[u"Комедийное"], u"Кинопоказ HD2"],
        [[u"Наш детектив", u"Наше крутое HD"], u"Наш Детектив HD"],
        [[u"Наш кинороман"], u"Наш Кинороман HD"],
        [[u"Кинопремьера"], u"Кинопремьера HD"],
        [[u"TV XXI", u"TV21"], u"ТВ XXI"],
        [[u"Европа Плюс ТВ"], u"Europa Plus TV"],
        [[u"MTV Russia"], u"MTV Россия"],
        [[u"Матч! Игра", u"Матч Игра"], u"Матч! Игра HD"],
        [[u"Матч! Арена", u"Матч Арена"], u"Матч! Арена HD"],
        [[u"Матч! Футбол 1", u"Матч Футбол 1"], u"Матч! Футбол 1 HD"],
        [[u"Матч! Футбол 2", u"Матч Футбол 2"], u"Матч! Футбол 2 HD"],
        [[u"Матч! Футбол 3", u"Матч Футбол 3"], u"Матч! Футбол 3 HD"],
        [[u"Сетанта Спорт + HD", u"Setanta Sports"], u"Сетанта Спорт HD"],
        [[u"Setanta Sports+", u"Сетанта Спорт+"], u"Сетанта Спорт + HD"],
        [[u"Eurosport 2"], u"Eurosport 2 HD"],
        [[u"А1", u"Amedia 1 HD"], u"A1"],
        [[u"TV3 LT", u"TV3 Литва"], u"TV3"],
        [[u"LRT Televizija"], u"LRT"],
        [[u"ТВ3", u"ТВ-3"], u"ТВ3 Россия"],
        [[u"Мульт и музыка", u"МультиМузыка"], u"Страна"]
]


class Names:

        def __init__(self):
                pass

        def add_custom_entries(self, channel_item):
                list = channel_item.display_name_list

                for item in replace_map:
                        if self.insert_value_if_needed(list, item[0], item[1]):
                                return
                pass

        def insert_value_if_needed(self, list, list_to_check, value_to_insert):
                for value0 in list:
                        if value0.text in list_to_check:
                                value = self.get_value_from_list(value_to_insert, list)
                                if(value is None):
                                        list.insert(0, NameItem(value_to_insert))
                                else:
                                        list.remove(value)
                                        list.insert(0, value)
                                return True
                return False

        def delete_from_list(self, list, item):
                value = self.get_value_from_list(item, list)
                if value is not None:
                        list.remove(value)

        def get_value_from_list(value, list):
                for item in list:
                        if item.text == value:
                                return item

                return None

