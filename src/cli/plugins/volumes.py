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


import time
from namespace import Namespace, EntityNamespace, IndexCommand, Command, description
from output import output_msg, output_table, format_datetime


class VolumeCreateNamespace(Namespace):
    pass


class VolumeCreateCommand(Command):
    def run(self, context, args, kwargs):
        name = args.pop(0)
        type = kwargs.pop('mode', 'auto')
        disks = args
        topology = {}




@description("Volumes namespace")
class VolumesNamespace(EntityNamespace):
    class ShowTopologyCommand(Command):
        def run(self, context, args, kwargs):
            pass

    def __init__(self, name, context):
        super(VolumesNamespace, self).__init__(name, context)

        self.add_property(
            descr='Volume name',
            name='name',
            get='/name',
            list=True)

        self.add_property(
            descr='Status',
            name='builtin',
            get='/status',
            set=None,
            list=True)

        self.primary_key = '/name'

    def query(self):
        return self.context.connection.call_sync('volume.query')


def _init(context):
    context.attach_namespace('/', VolumesNamespace('volumes', context))