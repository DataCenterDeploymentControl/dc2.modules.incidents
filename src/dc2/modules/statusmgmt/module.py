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
    from flask import Blueprint
    from flask_restful import Api
except ImportError as e:
    raise e

try:
    from dc2.core.application import app
except ImportError as e:
    raise e


__all__ = ['init_blueprint', 'init_manager_commands']

if 'RUN_VIA_MANAGER' in app.config and app.config['RUN_VIA_MANAGER']:
    from .db import models

from .api import init_endpoints

def init_blueprint(module=None):
    if module is not None:
        bp = Blueprint(module['name'], module['import_name'])
        bp_api = Api(bp)
        init_endpoints(bp_api)
        return bp
    return None



def init_manager_commands(manager=None):
    if manager is None:
        raise ValueError('manager can not be None')
    pass
     # from .manager import init_seed_commands
     # init_seed_commands()
