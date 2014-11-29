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


import crypt
from namespace import Namespace, Command, EntityNamespace, IndexCommand, description


@description("foo")
class UsersNamespace(EntityNamespace):

    def __init__(self, context):
        super(UsersNamespace, self).__init__(context)

        self.add_property(
            descr='User name',
            name='username',
            get='/username',
            list=True)

        self.add_property(
            descr='Full name',
            name='fullname',
            get='/full_name',
            list=True)

        self.add_property(
            descr='User ID',
            name='uid',
            get='/id',
            set=None,
            list=True)

        self.add_property(
            descr='Primary group',
            name='group',
            get=self.display_group)

        self.add_property(
            descr='Login shell',
            name='shell',
            get='/shell')

        self.add_property(
            descr='Home directory',
            name='home',
            get='/home',
            list=True)

        self.add_property(
            descr='Password',
            name='unixhash',
            get=None,
            set='/unixhash',
            list=False
        )

        self.primary_key = '/username'

    def query(self):
        return self.context.connection.call_sync('users.query')

    def get_one(self, name):
        return self.context.connection.call_sync('users.query', [('username', '=', name)]).pop()

    def set(self, entity, name, value, context):
        if name == 'unixhash':
            pass

    def display_group(self, entity):
        group = self.context.connection.call_sync('groups.query', [('id', '=', entity['group'])]).pop()
        return group['name'] if group else 'GID:{0}'.format(entity['group'])


@description("blah")
class GroupsNamespace(EntityNamespace):
    def __init__(self, context):
        super(GroupsNamespace, self).__init__(context)

        self.add_property(
            descr='Group name',
            name='name',
            get='/name')

        self.add_property(
            descr='Group ID',
            name='gid',
            get='/id',
            set=None)

        self.add_property(
            descr='Builtin group',
            name='builtin',
            get='/builtin',
            set=None)

    def query(self):
        return self.context.connection.call_sync('groups.query')

    def get_one(self, name, context):
        return context.connection.call_sync('groups.query', [('name', '=', name)]).pop()

    def set(self, entity, name, value, context):
        pass


@description("Service namespace")
class AccountNamespace(Namespace):
    def __init__(self, context):
        super(AccountNamespace, self).__init__()
        self.context = context

    def commands(self):
        return {
            '?': IndexCommand(self)
        }

    def namespaces(self):
        return {
            'users': UsersNamespace(self.context),
            'groups': GroupsNamespace(self.context)
        }


def _init(context):
    context.attach_namespace('/account', AccountNamespace(context))