#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
import pprint
import traceback
from pymongo import Connection
from datetime import datetime
connection = Connection()

class MongoDB:
    def __init__(self, app):
        db = connection.sakedata
        self.app = app
        self.pp = pprint.PrettyPrinter(indent=4)
        self.coll = db.sake
        self.coll.ensure_index('sake')


    def set_sake(self, datas):
        try:
            data = self._makedata(datas)
            uid = datas['name']

            user = self.coll.find_one({ 'user_name' : uid })
            if user:
                self.coll.update(user, data, upsert=True)
            else:
                self.coll.insert(data)

            return True
        except:
            self.app.logger.error('set_sake ERROR: %s' % traceback.format_exc())
            return False


    def get_sake(self, sake_name):
        results = []
        userdata = self.coll.find({'sake' : sake_name})
        if not userdata:
            return results

        for row in userdata:
            try:
                row.pop('_id')
                row['updated_at'] = row['updated_at'].strftime('%Y/%m/%d %H:%M:%S')
                results.append(row)
            except:
                self.app.logger.warn('get_sake ERROR: %s' % traceback.format_exc())

        #self.pp.pprint(results)
        return results


    def _makedata(self, datas):
        return {
            'user_name' : datas['name'],
            'sake'      : datas['sake'],
            'updated_at': datetime.now(),
        }
