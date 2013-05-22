class BattlelogStorage(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self._table = 'battlelog_users'

    def getUserD(self, cid):
        q = 'SELECT * from %s WHERE id = %s LIMIT 1' % (self._table, cid)
        cursor = self.plugin.console.storage.query(q)
        if cursor and not cursor.EOF:
            r = cursor.getRow()
            return r

    def create(self, client):
        data = {
            'id': client.id,
            'clanTag': client.clanTag,
            'platoonName': client.platoonName,
        }
        q = self._insertquery()
        try:
            cursor = self.plugin.console.storage.query(q, data)
            if cursor.rowcount > 0:
                self.plugin.debug("rowcount: %s, id:%s" % (cursor.rowcount, cursor.lastrowid))
            else:
                self.plugin.warning("inserting into %s failed" % self._table)
        except Exception, e:
            if e[0] == 1146:
                self.plugin.error("Could not save to database : %s" % e[1])
                self.plugin.info("Refer to this plugin readme file for instruction on how to create the required tables")
            else:
                raise e

    def _insertquery(self):
        return """INSERT INTO {table_name}
             (id, clanTag, platoonName)
             VALUES (%(id)s, %(clanTag)s, %(platoonName)s) """.format(table_name=self._table)

    def update(self):
        # todo: implement update
        pass

class DataStorage(object):

    def __init__(self, plugin):
        #default name of the table for this data object
        self._table = None
        self.plugin = plugin

    def _insertquery(self):
            raise NotImplementedError

    def save(self):
            """should call self._save2db with correct parameters"""
            raise NotImplementedError

    def _save2db(self, data):
        q = self._insertquery()
        try:
            cursor = self.plugin.console.storage.query(q, data)
            if cursor.rowcount > 0:
                self.plugin.debug("rowcount: %s, id:%s" % (cursor.rowcount, cursor.lastrowid))
            else:
                self.plugin.warning("inserting into %s failed" % self._table)
        except Exception, e:
            if e[0] == 1146:
                self.plugin.error("Could not save to database : %s" % e[1])
                self.plugin.info("Refer to this plugin readme file for instruction on how to create the required tables")
            else:
                raise e


class PlatoonsDB(DataStorage):

    # db table fields
    id = None
    platoon_id = None
    tag = None
    name = None
    time_add = None

    def __init__(self, plugin):
        DataStorage.__init__(self, plugin)
        self._table = 'bf3_platoons'

    def _insertquery(self):
        return """INSERT INTO {table_name}
             (platoon_id, tag, name, time_add)
             VALUES (%(platoon_id)s, %(tag)s, %(name)s, %(time_add)s) """.format(table_name=self._table)

    def save(self):
        data = {
            'platoon_id': self.platoon_id,
            'tag': self.tag,
            'name': self.name,
            'time_add': self.plugin.console.time(),
         }
        if self.plugin._save2db:
            self._save2db(data)