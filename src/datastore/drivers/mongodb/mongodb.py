#+
# Copyright 2014 iXsystems, Inc.
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#####################################################################

import uuid
from pymongo import MongoClient


class MongodbDatastore(object):
    def __init__(self):
        self.conn = None
        self.db = None
        self.operators_table = {
            '>': '$gt',
            '<': '$lt',
            '>=': '$gte',
            '<=': '$lte',
            'in': '$in',
            'nin': 'nin',
            '~': '$regex'
        }

    def _build_query(self, params):
        result = {}
        for name, op, value in params:
            if name == 'id':
                name = '_id'

            if op == '=':
                result[name] = value
                continue

            if op == '!=':
                result[name] = {'$not': value}

            if name not in result.keys():
                result[name] = {}

            if op in self.operators_table:
                result[name][self.operators_table[op]] = value

        return result

    def connect(self, dsn):
        self.conn = MongoClient(dsn)
        self.db = self.conn.freenas

    def collection_create(self, name, pkey_type='uuid', attributes={}):
        self.db['collections'].insert({
            '_id': name,
            'pkey-type': pkey_type,
            'last-id': 0,
            'attributes': attributes
        })

    def collection_exists(self, name):
        return self.db['collections'].find_one({"_id": name}) is not None

    def collection_get_attrs(self, name):
        item = self.db['collections'].find_one({"_id": name})
        return item['attributes']

    def collection_set_attrs(self, name):
        item = self.db['collections'].find_one({"_id": name})
        return item['attributes']

    def collection_list(self):
        return [x['name'] for x in self.db['collections'].find()]

    def collection_delete(self, name):
        self.db['collections'].remove({'_id': name})
        self.db.drop_collection(name)

    def collection_get_pkey_type(self, name):
        item = self.db['collections'].find_one({"_id": name})
        return item['pkey-type']

    def query(self, collection, *args, **kwargs):
        sort = kwargs.pop('sort', None)
        dir = kwargs.pop('dir', None)
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', None)
        single = kwargs.pop('single', False)
        result = []
        cur = self.db[collection].find(self._build_query(args))

        if sort:
            dir = 1 if dir == 'asc' else -1
            cur = cur.sort(sort, dir)

        if offset:
            cur = cur.skip(offset)

        if limit:
            cur = cur.limit(limit)

        if single:
            i = next(cur, None)
            if i is None:
                return i

            i['id'] = i.pop('_id')
            return i

        for i in cur:
            i['id'] = i.pop('_id')
            result.append(i)

        return result

    def get_one(self, collection, *args, **kwargs):
        obj = self.db[collection].find_one(self._build_query(args))
        if obj is None:
            return None

        obj['id'] = obj.pop('_id')
        return obj

    def get_by_id(self, collection, id):
        obj = self.db[collection].find_one({'_id': id})
        if obj is None:
            return None

        obj['id'] = obj.pop('_id')
        return obj

    def insert(self, collection, obj, pkey=None, upsert=False):
        if hasattr(obj, '__getstate__'):
            obj = obj.__getstate__()

        if type(obj) is not dict:
            obj = {'value': obj}

        if 'id' in obj:
            pkey = obj.pop('id')

        if pkey is None:
            pkey_type = self.collection_get_pkey_type(collection)
            if pkey_type in ('serial', 'integer'):
                ret = self.db['collections'].find_and_modify({'_id': collection}, {'$inc': {'last-id': 1}})
                pkey = ret['last-id']
            elif pkey_type == 'uuid':
                pkey = uuid.uuid4()

        obj['_id'] = pkey
        self.db[collection].insert(obj)
        return pkey

    def update(self, collection, pkey, obj):
        if hasattr(obj, '__getstate__'):
            obj = obj.__getstate__()

        if type(obj) is not dict:
            obj = {'value': obj}

        if 'id' in obj:
            del obj['id']

        self.db[collection].update({'_id': pkey}, obj)

    def upsert(self, collection, pkey, obj):
        return self.insert(collection, obj, pkey=pkey, upsert=True)

    def delete(self, collection, pkey):
        self.db[collection].remove(pkey)
