# -*- coding: utf-8 -*-

# Battlelog plugin for BigBrotherBot(B3)
# Copyright (c) 2013 Harry Gabriel <rootdesign@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import b3
from b3.plugin import Plugin
import b3.clients
import b3.events
from threading import Thread

#from battlelog.db import BattlelogStorage
from db import BattlelogStorage
#from battlelog.api import BattlelogAPI, BattlelogAPI
from api import BattlelogAPI, BattlelogAPI

__version__ = '1.0.0'
__author__ = 'ozon'


class BattlelogPlugin(Plugin):

    def onLoadConfig(self):
        pass

    def onStartup(self):
        self.battlelog_api = BattlelogAPI()

        # load the admin plugin
        self._adminPlugin = self.console.getPlugin('admin')

        # add attr to Client object
        if not hasattr(b3.clients.Client, 'clanTag'):
            setattr(b3.clients.Client, 'clanTag', None)
        if not hasattr(b3.clients.Client, 'platoonName'):
            setattr(b3.clients.Client, 'platoonName', None)

        # register event "Client Connect"
        # todo: try to use EVT_CLIENT_CONNECT
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)

        self.battlelog_cache = BattlelogStorage(self)

    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_AUTH:
            self.do_client_battlelog_update(event.client)

    def _setClientData(self, client, clanTag, platoonName):
        self.debug('Set clanTag: %s, platoonName: %s for %s' % (clanTag, platoonName, client.name))
        setattr(client, 'clanTag', clanTag)
        setattr(client, 'platoonName', platoonName)

    def callback_client_update(self, client, data):
        clanTag = data.clanTag
        platoonName = data.platoonName
        # set client attr
        self._setClientData(client, clanTag, platoonName)
        # save result to DB
        self.battlelog_cache.create(client)

    def do_client_battlelog_update(self, client):
        self.debug('Start battlelog update for %s' % client.name)
        _result = self.battlelog_cache.getUserD(cid=client.id)
        if _result and 'clanTag' in _result and 'platoonName' in _result:
            self.debug('Found infos in DB')
            self._setClientData(client, _result['clanTag'], _result['platoonName'])
        else:
            self.debug('Update infos from Battlelog')
            Battlelog_query(self.battlelog_api, clientname=client.name, callback=self.callback_client_update,
                            callback_args=(client,)).start()


class Battlelog_query(Thread):
    def __init__(self, battlelog_api, name=None, clientname=None, callback=None, callback_args=()):
        Thread.__init__(self, name=name, )
        self.__ipinfo_api = battlelog_api
        self.__clientname = clientname
        self.__callback = callback
        self.__callback_args = callback_args

    def run(self):
        battlelog_user = self.__ipinfo_api.getUser(self.__clientname)

        if self.__callback:
            self.__callback(*self.__callback_args, data=battlelog_user)



if __name__ == '__main__':
    from b3.fake import fakeConsole, superadmin, joe, simon, fakeAdminPlugin
    import time

    myplugin = BattlelogPlugin(fakeConsole, 'conf/plugin_battlelog.ini')
    myplugin.console.game.gameName = 'bf3'
    myplugin.onStartup()
    time.sleep(2)

    myplugin.console.game.gameType = 'Domination0'
    myplugin.console.game._mapName = 'XP2_Skybar'
    superadmin.connects(cid=0)
    # make joe connect to the fake game server on slot 1
    joe.connects(cid=1)
    # make joe connect to the fake game server on slot 2
    simon.connects(cid=2)
    # superadmin put joe in group user
    superadmin.says('!putgroup joe user')
    superadmin.says('!putgroup simon user')

    joe.name = 'O2ON'

    superadmin.connects(cid=0)

