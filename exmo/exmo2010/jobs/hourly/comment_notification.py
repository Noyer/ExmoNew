# -*- coding: utf-8 -*-
# This file is part of EXMO2010 software.
# Copyright 2010, 2011 Al Nikolov
# Copyright 2010, 2011 non-profit partnership Institute of Information Freedom Development
# Copyright 2012, 2013 Foundation "Institute for Information Freedom Development"
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

"""
Задача для рассылки дайджестов

Can be run as a cronjob to send comment digest
"""

from django_extensions.management.jobs import HourlyJob

from digest_email.digest import ScoreCommentDigest
from digest_email.models import Digest


class Job(HourlyJob):
    help = "Comment daily digest notification"

    def execute(self):
        digest = ScoreCommentDigest(Digest.objects.get(name = 'notify_comment'))
        digest.send()
