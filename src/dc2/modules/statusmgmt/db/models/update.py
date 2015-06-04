# -*- coding: utf-8 -*-
#
#
# DataCenter Deployment Control
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
__all__ = ['Update']


try:
    from dc2.core.database import DB
except ImportError as e:
    raise(e)

import datetime

class Update(DB.Model):
    __tablename__ = 'updates'

    id = DB.Column(DB.Integer, primary_key=True)
    update = DB.Column(DB.String, nullable=False)
    status_id = DB.Column(DB.Integer, DB.ForeignKey('states.id'))
    status = DB.relationship('Status', uselist=False, foreign_keys="Update.status_id")
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())
    created_by_user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    updated_by_user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    created_by = DB.relationship("User", uselist=False, foreign_keys="Update.created_by_user_id")
    updated_by = DB.relationship("User", uselist=False, foreign_keys="Update.updated_by_user_id")

    @property
    def to_dict(self):
        return dict(
            id=self.id,
            update=self.update,
            status=self.status.title if self.status is not None else None,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat() if self.updated_at is not None else None,
            created_by=self.created_by.username,
            updated_by=self.updated_by.username if self.updated_by is not None else None
        )

