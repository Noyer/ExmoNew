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
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OpennessExpression'
        db.create_table('exmo2010_opennessexpression', (
            ('code', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='-', max_length=255)),
        ))
        db.send_create_signal('exmo2010', ['OpennessExpression'])

        # Adding model 'Monitoring'
        db.create_table('exmo2010_monitoring', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='-', max_length=255)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('openness_expression', self.gf('django.db.models.fields.related.ForeignKey')(default=8, to=orm['exmo2010.OpennessExpression'])),
            ('time_to_answer', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3)),
            ('no_interact', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('prepare_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('rate_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('revision_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('interact_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('result_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('finishing_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('exmo2010', ['Monitoring'])

        # Adding model 'Questionnaire'
        db.create_table('exmo2010_questionnaire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monitoring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Monitoring'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
        ))
        db.send_create_signal('exmo2010', ['Questionnaire'])

        # Adding model 'QQuestion'
        db.create_table('exmo2010_qquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Questionnaire'])),
            ('qtype', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=600, blank=True)),
        ))
        db.send_create_signal('exmo2010', ['QQuestion'])

        # Adding model 'AnswerVariant'
        db.create_table('exmo2010_answervariant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qquestion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.QQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('exmo2010', ['AnswerVariant'])

        # Adding model 'Organization'
        db.create_table('exmo2010_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('keywords', self.gf('core.fields.TagField')(null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('monitoring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Monitoring'])),
            ('inv_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6, blank=True)),
        ))
        db.send_create_signal('exmo2010', ['Organization'])

        # Adding unique constraint on 'Organization', fields ['name', 'monitoring']
        db.create_unique('exmo2010_organization', ['name', 'monitoring_id'])

        # Adding model 'Parameter'
        db.create_table('exmo2010_parameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('monitoring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Monitoring'])),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
            ('keywords', self.gf('core.fields.TagField')()),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('topical', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('accessible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('hypertext', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('document', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('image', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('npa', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('exmo2010', ['Parameter'])

        # Adding unique constraint on 'Parameter', fields ['code', 'monitoring']
        db.create_unique('exmo2010_parameter', ['code', 'monitoring_id'])

        # Adding unique constraint on 'Parameter', fields ['name', 'monitoring']
        db.create_unique('exmo2010_parameter', ['name', 'monitoring_id'])

        # Adding M2M table for field exclude on 'Parameter'
        db.create_table('exmo2010_parameter_exclude', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parameter', models.ForeignKey(orm['exmo2010.parameter'], null=False)),
            ('organization', models.ForeignKey(orm['exmo2010.organization'], null=False))
        ))
        db.create_unique('exmo2010_parameter_exclude', ['parameter_id', 'organization_id'])

        # Adding model 'Task'
        db.create_table('exmo2010_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Organization'])),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('openness_first', self.gf('django.db.models.fields.FloatField')(default=-1)),
        ))
        db.send_create_signal('exmo2010', ['Task'])

        # Adding unique constraint on 'Task', fields ['user', 'organization']
        db.create_unique('exmo2010_task', ['user_id', 'organization_id'])

        # Adding model 'QAnswer'
        db.create_table('exmo2010_qanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Task'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.QQuestion'])),
            ('text_answer', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('numeral_answer', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('variance_answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.AnswerVariant'], null=True, blank=True)),
        ))
        db.send_create_signal('exmo2010', ['QAnswer'])

        # Adding unique constraint on 'QAnswer', fields ['task', 'question']
        db.create_unique('exmo2010_qanswer', ['task_id', 'question_id'])

        # Adding model 'Score'
        db.create_table('exmo2010_score', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Task'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Parameter'])),
            ('found', self.gf('django.db.models.fields.IntegerField')()),
            ('foundComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('complete', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('completeComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('topical', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('topicalComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accessible', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('accessibleComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hypertext', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hypertextComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('document', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('documentComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('imageComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('exmo2010', ['Score'])

        # Adding unique constraint on 'Score', fields ['task', 'parameter', 'revision']
        db.create_unique('exmo2010_score', ['task_id', 'parameter_id', 'revision'])

        # Adding model 'Claim'
        db.create_table('exmo2010_claim', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Score'])),
            ('open_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('close_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('close_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='close_user', null=True, to=orm['auth.User'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator', to=orm['auth.User'])),
            ('addressee', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='addressee', to=orm['auth.User'])),
        ))
        db.send_create_signal('exmo2010', ['Claim'])

        # Adding model 'Clarification'
        db.create_table('exmo2010_clarification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Score'])),
            ('open_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clarification_creator', to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('close_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('close_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='clarification_close_user', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('exmo2010', ['Clarification'])

        # Adding model 'UserProfile'
        db.create_table('exmo2010_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('preference', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sex', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, db_index=True)),
            ('subscribe', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=48, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('exmo2010', ['UserProfile'])

        # Adding M2M table for field organization on 'UserProfile'
        db.create_table('exmo2010_userprofile_organization', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['exmo2010.userprofile'], null=False)),
            ('organization', models.ForeignKey(orm['exmo2010.organization'], null=False))
        ))
        db.create_unique('exmo2010_userprofile_organization', ['userprofile_id', 'organization_id'])

        # Adding model 'MonitoringInteractActivity'
        db.create_table('exmo2010_monitoringinteractactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monitoring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Monitoring'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('exmo2010', ['MonitoringInteractActivity'])

        # Adding unique constraint on 'MonitoringInteractActivity', fields ['user', 'monitoring']
        db.create_unique('exmo2010_monitoringinteractactivity', ['user_id', 'monitoring_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MonitoringInteractActivity', fields ['user', 'monitoring']
        db.delete_unique('exmo2010_monitoringinteractactivity', ['user_id', 'monitoring_id'])

        # Removing unique constraint on 'Score', fields ['task', 'parameter', 'revision']
        db.delete_unique('exmo2010_score', ['task_id', 'parameter_id', 'revision'])

        # Removing unique constraint on 'QAnswer', fields ['task', 'question']
        db.delete_unique('exmo2010_qanswer', ['task_id', 'question_id'])

        # Removing unique constraint on 'Task', fields ['user', 'organization']
        db.delete_unique('exmo2010_task', ['user_id', 'organization_id'])

        # Removing unique constraint on 'Parameter', fields ['name', 'monitoring']
        db.delete_unique('exmo2010_parameter', ['name', 'monitoring_id'])

        # Removing unique constraint on 'Parameter', fields ['code', 'monitoring']
        db.delete_unique('exmo2010_parameter', ['code', 'monitoring_id'])

        # Removing unique constraint on 'Organization', fields ['name', 'monitoring']
        db.delete_unique('exmo2010_organization', ['name', 'monitoring_id'])

        # Deleting model 'OpennessExpression'
        db.delete_table('exmo2010_opennessexpression')

        # Deleting model 'Monitoring'
        db.delete_table('exmo2010_monitoring')

        # Deleting model 'Questionnaire'
        db.delete_table('exmo2010_questionnaire')

        # Deleting model 'QQuestion'
        db.delete_table('exmo2010_qquestion')

        # Deleting model 'AnswerVariant'
        db.delete_table('exmo2010_answervariant')

        # Deleting model 'Organization'
        db.delete_table('exmo2010_organization')

        # Deleting model 'Parameter'
        db.delete_table('exmo2010_parameter')

        # Removing M2M table for field exclude on 'Parameter'
        db.delete_table('exmo2010_parameter_exclude')

        # Deleting model 'Task'
        db.delete_table('exmo2010_task')

        # Deleting model 'QAnswer'
        db.delete_table('exmo2010_qanswer')

        # Deleting model 'Score'
        db.delete_table('exmo2010_score')

        # Deleting model 'Claim'
        db.delete_table('exmo2010_claim')

        # Deleting model 'Clarification'
        db.delete_table('exmo2010_clarification')

        # Deleting model 'UserProfile'
        db.delete_table('exmo2010_userprofile')

        # Removing M2M table for field organization on 'UserProfile'
        db.delete_table('exmo2010_userprofile_organization')

        # Deleting model 'MonitoringInteractActivity'
        db.delete_table('exmo2010_monitoringinteractactivity')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exmo2010.answervariant': {
            'Meta': {'object_name': 'AnswerVariant'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qquestion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.QQuestion']"})
        },
        'exmo2010.claim': {
            'Meta': {'object_name': 'Claim'},
            'addressee': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'addressee'", 'to': "orm['auth.User']"}),
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'close_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'close_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'close_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Score']"})
        },
        'exmo2010.clarification': {
            'Meta': {'object_name': 'Clarification'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'close_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'close_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'clarification_close_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clarification_creator'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Score']"})
        },
        'exmo2010.monitoring': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Monitoring'},
            'finishing_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interact_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '255'}),
            'no_interact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'openness_expression': ('django.db.models.fields.related.ForeignKey', [], {'default': '8', 'to': "orm['exmo2010.OpennessExpression']"}),
            'prepare_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'rate_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'result_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'revision_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'time_to_answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'})
        },
        'exmo2010.monitoringinteractactivity': {
            'Meta': {'unique_together': "(('user', 'monitoring'),)", 'object_name': 'MonitoringInteractActivity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitoring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Monitoring']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exmo2010.opennessexpression': {
            'Meta': {'object_name': 'OpennessExpression'},
            'code': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '255'})
        },
        'exmo2010.organization': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'monitoring'),)", 'object_name': 'Organization'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inv_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'blank': 'True'}),
            'keywords': ('core.fields.TagField', [], {'null': 'True'}),
            'monitoring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Monitoring']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'exmo2010.parameter': {
            'Meta': {'ordering': "('code', 'name')", 'unique_together': "(('code', 'monitoring'), ('name', 'monitoring'))", 'object_name': 'Parameter'},
            'accessible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exclude': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['exmo2010.Organization']", 'null': 'True', 'blank': 'True'}),
            'hypertext': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('core.fields.TagField', [], {}),
            'monitoring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Monitoring']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'npa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'topical': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'exmo2010.qanswer': {
            'Meta': {'unique_together': "(('task', 'question'),)", 'object_name': 'QAnswer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numeral_answer': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.QQuestion']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Task']"}),
            'text_answer': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'variance_answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.AnswerVariant']", 'null': 'True', 'blank': 'True'})
        },
        'exmo2010.qquestion': {
            'Meta': {'object_name': 'QQuestion'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qtype': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Questionnaire']"})
        },
        'exmo2010.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '600', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitoring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Monitoring']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'exmo2010.score': {
            'Meta': {'ordering': "('task__user__username', 'task__organization__name', 'parameter__code')", 'unique_together': "(('task', 'parameter', 'revision'),)", 'object_name': 'Score'},
            'accessible': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'accessibleComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'complete': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'completeComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'documentComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'found': ('django.db.models.fields.IntegerField', [], {}),
            'foundComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hypertext': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hypertextComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imageComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Parameter']"}),
            'revision': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Task']"}),
            'topical': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'topicalComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'exmo2010.task': {
            'Meta': {'ordering': "('organization__name', 'user__username')", 'unique_together': "(('user', 'organization'),)", 'object_name': 'Task'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'openness_first': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Organization']"}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exmo2010.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['exmo2010.Organization']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'}),
            'preference': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sex': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'subscribe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['exmo2010']