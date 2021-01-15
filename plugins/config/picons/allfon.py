# -*- coding: utf-8 -*-
'''
AllFonTV channels picon
'''
# Channels logo location
logobase = 'http://1ttv.org/uploads/'
# Channels logo/path mapping
logomap = {
    u'24 ДОК': logobase + 'FznqTpJ71LS3RLESzMOHhNDxJMwBE8.png',
    u'2x2': logobase + 'hTpJUV15GSTxZ5kJQGLcn42kCzKyEH.png',
    u'5 канал': logobase + 'nIUDYY41OO4Xo0ntGpGv2rfpOR5ngt.png',
    u'A1': logobase + 'NbdxfVLZtRUQzzfvQPNRVMVAl2Hp0O.png',
    u'A2': logobase + 'KY8tm4Runi4FpgUYcAn5WoeXqiD3Y5.png',
    u'Ani': logobase + 'vui1cRrE05CZv1N9Qb20jJ6mTFOJue.png',
    u'Da Vinci': logobase + 'Yl6p1IDDkZxxiUa3p2JxI66mIlOPns.png',
    u'Nickelodeon': logobase + 'j66xpaZbfiYIgQxv76QAPckPVjmLNs.png',
    u'Paramount Comedy': logobase + '5EtvAWXB7VK1Yw82yvO28sY28dU4ZC.png',
    u'Russia Today': logobase + 'rL14fwCe8q10mKTchOwLkfwQVki9XK.png',
    u'TiJi': logobase + 'mD3GW0E7rdPwc4stjk7xrLI2gZn4Hq.png',
    u'Travel+Adventure': logobase + 'b1HifWKMyefmDDvaDAJTwNNTaD8LF4.png',
    u'TV XXI': logobase + 'TKchoTWZFRMmGDBok08zoEFJ8mJJCe.png',
    u'TV1000 Русское кино': logobase + 'ch5DX6f8hxDnmyzrjotUoKHNGzcw9P.png',
    u'Viasat Explore': logobase + 'uCqpsdKP0ialUUYxUk2fXshYdYfxzW.png',
    u'Авто Плюс': logobase + 'WkRxjy6fJEBJ5NZiaGn2j05eqfFfQq.png',
    u'Бобёр': logobase + '2Edln8vEbg7UUSVUo7lIJPR780OWAR.png',
    u'Время': logobase + 'F44yKDJQLsX0llpZ2wupg8V5vHx5fF.png',
    u'Детский мир': logobase + '00Vf3rPABNnbNQ6Rv0dnfcg3JsJelA.png',
    u'Дом кино': logobase + 'jlC78Fy13KWjQUN6l3FtbsRLZDvc0x.png',
    u'Домашний': logobase + 'qmqrH2E2EX11qitbIvq0CYsxQjsHGm.png',
    u'Драйв': logobase + 'IzUNez8spn44tivGiApqajydfeOwxg.png',
    u'Еврокино': logobase + '34mszCG0j0Vf6kFcMrLPnFEA8UPdu6.png',
    u'Звезда': logobase + '0HLRrFHt2QIkbJpLc1fy0RVe7hqCEC.png',
    u'Иллюзион +': logobase + '8LToTNvWRBHvb5IKoteKm8EwAGw8mv.png',
    u'История': logobase + 'PNRaeOUFzOPFtrclFBBRTckj6Lvo0u.png',
    u'Калейдоскоп ТВ': logobase + 'YJMqmzlZ87QeXYm9XpjH0XzpjljNcU.png',
    u'Канал Disney': logobase + 'JxEjTeXwExjnxutQGKJBmMI85tpNqK.png',
    u'Кинокомедия': logobase + 'y087hci8ityixcnyxinxoafhiu.png',
    u'Киномикс': logobase + 'y6b876ih8g7R876hfug3897wrhj.png',
    u'Киносерия': logobase + 'o07C0d3hHzAtT4in0l3E4U1I6rQoTY.png',
    u'КХЛ': logobase + '216.png',
#    u'Матч Премьер': logobase + '',
    u'Матч ТВ': logobase + 'hQDOuQjUVczvUU2ocLE0tkC1siCqpo.png',
    u'Матч! Арена': logobase + 'DDjh1dM2D09Wcl3L6YmEd1si3P17n0.png',
    u'Матч! Боец': logobase + 'xj1tPp6g9LmQH5KAN0gFpWYoa9RdbL.png',
    u'Матч! Игра': logobase + 'urIB7TbFWo36EmXW9eG3w4qre7MdX9.png',
    u'МАТЧ! Футбол 1': logobase + '9PM8M6cN21wQ3M5isVZgjNepzUI4Ry.png',
    u'МАТЧ! Футбол 2': logobase + '8MA3WloO6RsWX8N7Ck5ugek2Kirf4B.png',
    u'МАТЧ! Футбол 3': logobase + 'OLHdmyfUev4mMX0OGniJrlUwHnMKOg.png',
    u'Мир Сериала': logobase + 'XWDsU7aoUyPPoKfcX7WMYQheuzHJL0.png',
    u'Моя Планета': logobase + 'Qa41eifERrD77xQsmpRGbeTq95Ldlv.png',
    u'Мужское Кино': logobase + 'y997iu65e65h4w5d3s4dy.png',
    u'МУЛЬТ': logobase + 'ZVzHvGF8mZ6RTsSh6aWsPbF1FBLjyp.png',
    u'Ностальгия': logobase + 'tIfiXoDaXoZevuGu9pZJSvX8unv1xl.png',
    u'НСТ': logobase + 'fKYzdlWRz68qd9mRZnWuxMY73EyaSz.png',
    u'Охота и рыбалка': logobase + '5l2P20J6ebTh0ptOr27Hh704niP3nU.png',
#    u'Парк развлечений': logobase + '',
    u'Первый': logobase + 'WimZD6efLd6QotrPP9uiJeF7t50nFv.png',
    u'Психология 21': logobase + 'AyLAdiqcKu5X8ykdLf2bO9HsxMlJdO.png',
    u'РЕН ТВ': logobase + 'LJvkfB2kYaDzij1Y13Fy6syUCkP5Y6.png',
    u'Ретро ТВ': logobase + '5vuRj5ip04YKBNM60rdB7aFueKvypo.png',
    u'Россия 1': logobase + 'UUrfoqi6NQcc9gRLnCc8ODZJ2T3ShE.png',
    u'Россия 24': logobase + 'LWfGV6eICPYL7psaBfw2dOgGrOtHFS.png',
    u'РТВ - Любимое кино': logobase + 'LSR5M6VxB0YDwv6803zrGFkq7vGQ3J.png',
    u'Русский детектив': logobase + '7I7VjbsFMIkZdoSbHFXiKEVZKNUbOM.png',
    u'Русский Иллюзион': logobase + 'E9Imfr8aHN5midPVpNhJ3fo49FHbQE.png',
    u'Русский роман': logobase + '2smriIFxtj7Ojh4jyZq0K1XrT98XjS.png',
    u'Русский Экстрим': logobase + 'upndVpIdjY3vb5vrituof5UcKISNcQ.png',
    u'Санкт-Петербург': logobase + 'sb81YtPOvlHidztMnC5tZPSKkb1uMI.png',
    u'СТС': logobase + 'is620Pu6DreVLLnpHkpcXXZC9PI2Hi.png',
    u'ТВ3': logobase + '07bjT0brQLyETHscCfGFtvsdaRiUdH.png',
    u'ТНТ': logobase + 'Vtt1KKIpLY4LTQGnV03sdBYyX3hyWR.png',
    u'ТНТ4': logobase + 'yTclqOAW0EWwhw9vt0spVSUcS70ZR0.png',
    u'Точка ТВ': logobase + 'JWwPbPnkWooIpKd5WYsdpfO3Mh14oA.png',
    u'Феникс+ Кино': logobase + 'idiNkkBsxLwxWCF2VZrc9LQEevKh0d.png',
    u'Че': logobase + 'Hv36ZG48lg1mm2wdxAo3ju1EFS41Ga.png',
    u'Ю': logobase + 'YvnG7hXCwMmHnakp2KkCbqeCigHcuK.png',
}
