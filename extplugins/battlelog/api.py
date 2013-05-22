import requests
import urlparse
import urllib


class BattlelogAPI(object):
    battlelog_url = 'http://battlelog.battlefield.com/bf3/'

    def __init__(self):
        self.session = requests.session()

    def _request(self, path):
        headers = {'X-Requested-With': 'XMLHttpRequest', 'X-AjaxNavigation': '1'}
        url = urlparse.urljoin(self.battlelog_url, path)
        return self.session.request('GET', url, headers=headers).json()

    def getUser(self, user_name):
        _user_name = urllib.quote_plus(unicode(user_name).encode('utf-8'))
        _res = self._request('user/%s/' % _user_name)
        return BattlelogUser(_res['context'])


class BattlelogUser(object):

    def __init__(self, rawuser):
        self._rawuser = rawuser
        self.userId = self._rawuser['profileCommon']['user']['userId']
        self.userName = self._rawuser['profileCommon']['user']['username']
        self.clanTag = None
        self.platoonId = None
        self.platoonName = None

        self.personaId = None
        self.personaName = None

        self._get_persona()
        self._get_platoon()

    def _get_platoon(self):
        platoons = self._rawuser.get('profileCommon').get('platoons')
        # get userplatoon
        for platoon in platoons:
            if platoon.get('tag') == self.clanTag:
                self.platoonId = platoon.get('id')
                self.platoonName = platoon.get('name')

    def _get_persona(self):
        soldierBox = self._rawuser.get('soldiersBox')
        # get bf3 persona for pc plattform
        persona = [soldier['persona'] for soldier in soldierBox if soldier['persona']['namespace'] == 'cem_ea_id']

        self.personaId = persona[0].get('personaId')
        self.personaName = persona[0].get('personaName')
        self.clanTag = persona[0].get('clanTag')
