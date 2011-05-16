# This file is part of EXMO2010 software.
# Copyright 2010, 2011 Al Nikolov
# Copyright 2010, 2011 Institute for Information Freedom Development
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from exmo.exmo2010.models import Task
from exmo.exmo2010.models import Monitoring
from django import template

register = template.Library()

def model_status(choices, status):
    for s in choices:
        if status == s[0]:
            return s[1]
        elif status == s[1]:
            return s[0]
    else:
        return None

def monitoring_status(status):
    return model_status(Monitoring.MONITORING_STATUS_FULL, status)

def task_status(status):
    return model_status(Task.TASK_STATUS, status)

register.simple_tag(task_status)
register.simple_tag(monitoring_status)