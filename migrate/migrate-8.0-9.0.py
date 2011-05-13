#!/usr/bin/python
# -*- coding: utf-8 -*-
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

###
# WARNING! Disable DEBUG in settings.py if you have LARGE dump.
###

###
# WARNING! This script migrate ONLY exmo2010 models. Auth, django, and other models must be load separately and before this.
###

###
# WARNING! This script migrate from JSON dump to WORK database.
# It's doesn't prepare any JSON. All data write to DB directly with using django ORM.
###

import simplejson
dump = 'data-8.0.json'

print "Load data from %s" % dump
old_data = simplejson.load(open(dump))
print "Done"

import os
import sys
import gc

gc.enable()

os.environ['DJANGO_SETTINGS_MODULE'] = "exmo.settings"
path = "%s/.." % os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.realpath(path))

import exmo.exmo2010.models as em
from django.contrib.auth import models as auth

#disconnect post_save_model signal.
from django.db.models.signals import post_save
from exmo.exmo2010.helpers import post_save_model
post_save.disconnect(post_save_model)

# deleted models from 8.0. migrate this data to keywords. see below.
keyword_models=['OrganizationType',
                'Federal',
                'Entity',
                'Category',
                'Subcategory',
                'ParameterType',
                ]


'''
get data for Keyword model from:
    OrganizationType.name
    Federal.name
    Entity.name
    Category.name
    Subсategory.name
    ParameterType.name
'''

print "Creating keywords from %s models" % ", ".join(keyword_models)
for obj in old_data:
    if obj['model'] in ["exmo2010.%s" % name.lower() for name in keyword_models]:
        keyword, created = em.Keyword.objects.get_or_create(keyword=obj['fields']['name'])
print "Done"

print "Creating keywords from organization keywords and keyname"
#put keywords and keyname from organizations to Keyword model
for obj in old_data:
    if obj['model'] == "exmo2010.organization":
        kwd=[]
        if obj['fields']['keywords']:
            kwd=obj['fields']['keywords'].split(' ')
        if obj['fields']['keyname']:
            kwd+=obj['fields']['keyname'].split(' ')
        for keyword in kwd:
            oobject, created = em.Keyword.objects.get_or_create(keyword=keyword)
print "Done"


print "Migrate OpennessExpression model"
#migrate Monitoring and OpennessExpression without changes.
#we save all pks. It's important for organization and task migration.
for obj in old_data:
    if obj['model'] == 'exmo2010.opennessexpression':
        oobject, created = em.OpennessExpression.objects.get_or_create(
            code=obj['pk'],
            name=obj['fields']['name']
        )
print "Done"

print "Migrate Monitoring model"
for obj in old_data:
    if obj['model'] == 'exmo2010.monitoring':
        monitoring, created = em.Monitoring.objects.get_or_create(
            pk = obj['pk'],
            name=obj['fields']['name'],
            openness_expression=em.OpennessExpression.objects.get(pk=obj['fields']['openness_expression'])
        )
        monitoring.create_calendar()
print "Done"


print "Migrate Task and Organization models"
#migrating Task model. Create organization for every task on fly. Organization create without keywords! Keywords will be add below.
#We save task.pk. It's important for score migration.
for obj in old_data:
    if obj['model'] == 'exmo2010.task':
        for obj_org in old_data:
            if obj_org['model'] == 'exmo2010.organization' and obj_org['pk'] == obj['fields']['organization']:
                org, created = em.Organization.objects.get_or_create(
                    monitoring = em.Monitoring.objects.get(pk=obj['fields']['monitoring']),
                    name = obj_org['fields']['name'],
                    url = obj_org['fields']['url'],
                    comments = obj_org['fields']['comments'],
                )
                break
        task, created = em.Task.objects.get_or_create(
                    pk = obj['pk'],
                    organization = org,
                    user = auth.User.objects.get(pk=obj['fields']['user']),
                    status = obj['fields']['status'],
                )
print "Done"

print "Add keywords to organizations"
#add keywords to organizations. based on organization name.
for obj in old_data:
    if obj['model'] == 'exmo2010.organization':
        #I belive, that all organizations have at least one task...
        org_list = em.Organization.objects.filter(name = obj['fields']['name'])
        kwd=[]
        if obj['fields']['keywords']:
            kwd=obj['fields']['keywords'].split(' ')
        if obj['fields']['keyname']:
            kwd+=obj['fields']['keyname'].split(' ')
        for obj_entity in old_data:
            if obj_entity['model'] == 'exmo2010.entity' and obj_entity['pk'] == obj['fields']['entity']:
                kwd.append(obj_entity['fields']['name'])
                for obj_federal in old_data:
                    if obj_federal['model'] == 'exmo2010.federal' and obj_federal['pk'] == obj_entity['fields']['federal']:
                        kwd.append(obj_federal['fields']['name'])
                        break
                break
        for org in org_list:
            for keyword in kwd:
                #all keywords added early
                org.keywords.add(em.Keyword.objects.get(keyword = keyword))
print "Done"



print "Migrate Score and Parameter models"
#migrate scores and parameters on fly... Parameter exclude and keywords must be filled later (because m2m).
for obj in old_data:
    if obj['model'] == 'exmo2010.score':
        task = em.Task.objects.get(pk=obj['fields']['task'])
        #get parameter
        for obj_param in old_data:
            if obj_param['model'] == 'exmo2010.parameter' and obj_param['pk'] == obj['fields']['parameter']:
                #get parameter type
                param_type = None
                for obj_param_type in old_data:
                    if obj_param_type['model'] == 'exmo2010.parametertype' and obj_param_type['pk'] == obj_param['fields']['type']:
                        param_type = obj_param_type
                        break
                #get parameter weight
                param_w = 0
                for obj_param_w in old_data:
                    if obj_param_w['model'] == 'exmo2010.parametermonitoringproperty' and \
                      obj_param_w['fields']['parameter'] == obj_param['pk'] and \
                      obj_param_w['fields']['monitoring'] == task.organization.monitoring.pk:
                        param_w = obj_param_w['fields']['weight']
                        break
                #get code. code = 10000*category.code+100*subcat.code+param.code
                code = obj_param['fields']['code']
                #get subcat code
                cat_code = subcat_code = 1
                for obj_param_subcat in old_data:
                    if obj_param_subcat['model'] == 'exmo2010.subcategory' and \
                      obj_param_subcat['pk'] == obj_param['fields']['group']:
                        subcat_code = obj_param_subcat['fields']['code']
                        #get cat code
                        for obj_param_cat in old_data:
                            if obj_param_cat['model'] == 'exmo2010.category' and \
                              obj_param_cat['pk'] == obj_param_subcat['fields']['group']:
                                cat_code = obj_param_cat['fields']['code']
                                break
                        break
                code = code + (cat_code * 10000) + (subcat_code * 100)
                #create parameter
                parameter, created = em.Parameter.objects.get_or_create(
                    code = code,
                    name = obj_param['fields']['name'],
                    description = obj_param['fields']['description'],
                    monitoring = task.organization.monitoring,
                    weight = param_w,
                    complete = param_type['fields']['complete'],
                    topical = param_type['fields']['topical'],
                    accessible = param_type['fields']['accessible'],
                    hypertext = param_type['fields']['hypertext'],
                    document = param_type['fields']['document'],
                    image = param_type['fields']['image'],
                )
                break
        #create score with created parameter
        em.Score.objects.get_or_create(
            pk = obj['pk'],
            task = task,
            parameter = parameter,
            found = obj['fields']['found'],
            complete = obj['fields']['complete'],
            completeComment = obj['fields']['completeComment'],
            topical = obj['fields']['topical'],
            topicalComment = obj['fields']['topicalComment'],
            accessible = obj['fields']['accessible'],
            accessibleComment = obj['fields']['accessibleComment'],
            hypertext = obj['fields']['hypertext'],
            hypertextComment = obj['fields']['hypertextComment'],
            document = obj['fields']['document'],
            documentComment = obj['fields']['documentComment'],
            image = obj['fields']['image'],
            imageComment = obj['fields']['imageComment'],
            comment = obj['fields']['comment'],
        )
print "Done"

print "Add keywords to parameters"
#add keywords to parameters. based on parameter name.
for obj_param in old_data:
    if obj_param['model'] == 'exmo2010.parameter':
        param_list = em.Parameter.objects.filter(name = obj_param['fields']['name'])
        kwd=[]
        for obj_param_subcat in old_data:
            if obj_param_subcat['model'] == 'exmo2010.subcategory' and \
              obj_param_subcat['pk'] == obj_param['fields']['group']:
                kwd.append(obj_param_subcat['fields']['name'])
                for obj_param_cat in old_data:
                    if obj_param_cat['model'] == 'exmo2010.category' and \
                      obj_param_cat['pk'] == obj_param_subcat['fields']['group']:
                        kwd.append(obj_param_cat['fields']['name'])
                        break
                break
        for param in param_list:
            for keyword in kwd:
                #all keywords added early
                param.keywords.add(em.Keyword.objects.get(keyword = keyword))
        #fill exclude for parameters
        for org_pk in obj_param['fields']['exclude']:
            for obj_org in old_data:
                if obj_org['model'] == 'exmo2010.organization' and obj_org['pk'] == org_pk:
                    for param in param_list:
                        org = em.Organization.objects.filter(monitoring = param.monitoring, name = obj_org['fields']['name'])
                        for o in org:
                            param.exclude.add(o)
                    break
print "Done"



print "Mirgate UserProfile model"
for obj in old_data:
    if obj['model'] == 'exmo2010.userprofile':
        profile, created = em.UserProfile.objects.get_or_create(
            user = auth.User.objects.get(pk=obj['fields']['user']),
            notify_score_change = obj['fields']['notify_score_change'],
        )
        for org_pk in obj['fields']['organization']:
            for obj_org in old_data:
                if obj_org['model'] == 'exmo2010.organization' and obj_org['pk'] == org_pk:
                    org = em.Organization.objects.filter(name = obj_org['fields']['name'])
                    for o in org:
                        profile.organization.add(o)
print "Done"
