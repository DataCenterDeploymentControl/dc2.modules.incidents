# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

__author__ = 'stephan.adig'

try:
    from flask_restful import Resource as RestResource
    from flask_restful.reqparse import RequestParser
    from flask import g, request
except ImportError as e:
    raise e


try:
    from dc2.core.application import app
    from dc2.core.database import DB
    from dc2.core.database.errors import lookup_error
    from dc2.core.helpers import hash_generator
    from dc2.core.auth.decorators import needs_authentication, has_groups
except ImportError as e:
    raise e

try:
    from ...db.models import Status
    from ...db.models import Update
    from dc2.core.modules.usersgroups.db.models import User
except ImportError as e:
    raise(e)


_status_parser = RequestParser()
_status_parser.add_argument('title', type=str, location='json', dest='title', required=True)
_status_parser.add_argument('status', type=str, location='json', dest='status', required=True, default='new')
_status_parser.add_argument('description', type=str, location='json', dest='description', required=True)
_status_parser.add_argument('impact', type=str, location='json', dest='impact', required=True, default='internal')
_status_parser.add_argument('updates', type=list, location='json', dest='updates', required=True)
class StateCollection(RestResource):

    def __init__(self, *args, **kwargs):
        super(StateCollection, self).__init__(*args, **kwargs)
        # self._ctl_hostentries = HostEntryController(DB.session)

    @needs_authentication
    @has_groups(['users', 'admin'])
    def get(self):
        try:
            statelist = Status.query.all()
            return [status.to_dict for status in statelist], 200
        except Exception as e:
            app.logger.exception(msg='Exception occured')
            return {'status': { 'error': True, 'message': e.args}}, 404

    @needs_authentication
    @has_groups(['users', 'groups'])
    def post(self):
        try:
            if g.auth_user is not None:
                user = User.query.filter_by(username=g.auth_user).first()
                args = _status_parser.parse_args()
                new_status = Status()
                new_status.title = args.title
                new_status.status = args.status
                new_status.description = args.description
                new_status.impact = args.impact
                new_status.created_by = user
                update_arr = []
                for update in args.updates:
                    up = Update()
                    up.update = update['update']
                    up.created_by = user
                    update_arr.append(up)
                new_status.updates = update_arr

                DB.session.add(new_status)
                DB.session.commit()
                return {'result': {
                    'status': new_status.to_dict
                    }
                }
            return {'status': {'error': True, 'message': 'No User'}}, 404
        except Exception as e:
            app.logger.exception(msg='Exception occured')
            return {'status': {'error': True, 'message': e.args}}, 404


class StateEntries(RestResource):
    def __init__(self, *args, **kwargs):
        super(StateEntries, self).__init__(*args, **kwargs)

    @needs_authentication
    @has_groups(['users', 'admin'])
    def put(self, id=None):
        if id is not None:
            try:
                args = _status_parser.parse_args()
                if g.auth_user is not None:
                    user = User.query.filter_by(username=g.auth_user).first()
                    old_status = Status.query.filter_by(id=id).first()
                    old_status.title = args.title
                    old_status.status = args.status
                    old_status.description = args.description
                    old_status.impact = args.impact
                    old_status.updated_by = user
                    for up in args.updates:
                        print(up)
                        if 'id' not in up:
                            print('id not in up')
                            new_up = Update()
                            new_up.update = up['update']
                            new_up.created_by = user
                            old_status.updates.append(new_up)
                    DB.session.commit()
                    return {'result': {'status': old_status.to_dict}}, 200
                return {'status': {'error': True, 'message': 'No User Given'}}, 404
            except Exception as e:
                app.logger.exception(msg='Exception occured')
                return {'status': {'error': True, 'message': e.args}}, 404
        return {'status': {'error': True, 'message': 'No ID Given'}}, 404

    @needs_authentication
    @has_groups(['users', 'admin'])
    def delete(self, id=None):
        if id is not None:
            try:
                old_status = Status.query.filter_by(id=id).first()
                DB.session.delete(old_status)
                DB.session.commit()
                return {'result': {'status': 'ok'}}, 200
            except Exception as e:
                app.logger.exception(msg="Exception occured")
                return {'status': {'error': True, 'message': e.args}}, 404
        return {'status': {'error': True, 'message': 'no ID Given'}}, 404
