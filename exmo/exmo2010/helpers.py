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
#from contrib.admin
from django.utils.translation import ugettext_lazy, ugettext as _
from django.utils.text import capfirst, get_text_list
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse
from exmo.helpers import disable_for_loaddata
from django.core.mail import EmailMessage
from exmo.exmo2010.models import UserProfile



def construct_change_message(request, form, formsets):
        """
        Construct a change message from a changed object.
        """
        change_message = []
        if form.changed_data:
            change_message.append(_('Changed %s.') % get_text_list(form.changed_data, _('and')))

        if formsets:
            for formset in formsets:
                for added_object in formset.new_objects:
                    change_message.append(_('Added %(name)s "%(object)s".')
                                          % {'name': force_unicode(added_object._meta.verbose_name),
                                             'object': force_unicode(added_object)})
                for changed_object, changed_fields in formset.changed_objects:
                    change_message.append(_('Changed %(list)s for %(name)s "%(object)s".')
                                          % {'list': get_text_list(changed_fields, _('and')),
                                             'name': force_unicode(changed_object._meta.verbose_name),
                                             'object': force_unicode(changed_object)})
                for deleted_object in formset.deleted_objects:
                    change_message.append(_('Deleted %(name)s "%(object)s".')
                                          % {'name': force_unicode(deleted_object._meta.verbose_name),
                                             'object': force_unicode(deleted_object)})
        change_message = ' '.join(change_message)
        return change_message or _('No fields changed.')



from django.core.mail import send_mail
from django.template import loader, Context
from django.conf import settings
def comment_notification(sender, **kwargs):
    comment = kwargs['comment']
    request = kwargs['request']
    score = comment.content_object

    #update user.email
    if not comment.user.email and comment.user_email:
        comment.user.email = comment.user_email
        comment.user.save()

    subject = u'%(prefix)s%(monitoring)s - %(org)s: %(code)s' % {
            'prefix': settings.EMAIL_SUBJECT_PREFIX,
            'monitoring': score.task.organization.monitoring,
            'org': score.task.organization.name.split(':')[0],
            'code': score.parameter.code,
            }
    admin_rcpt = nonadmin_rcpt = []

    headers = {
        'X-iifd-exmo': 'comment_notification',
        'X-iifd-exmo-comment-organization-url': score.task.organization.url,
    }


    #admin comment user list
    admin_users = []
    #A-expert + B-expert-manager
    admin_users.extend(User.objects.filter(groups__name__in = [UserProfile.expertA_group,UserProfile.expertB_manager_group]), is_active = True)
    #superusers
    admin_users.extend(User.objects.filter(is_superuser = True, is_active = True))
    #B-expert
    if score.task.user.is_active: admin_users.extend(score.task.user)
    for user.is_active in admin_users:
        if user.email:
            if user == comment.user:
                if user.notify_self_comment:
                    #self comment
                    admin_rcpt.append(user.email)
            else:
                if user.notify_comment:
                    admin_rcpt.append(user.email)
    #get only uniq emails
    admin_rcpt=list(set(admin_rcpt))

    #non-admin comment user list
    nonadmin_users = []
    #organization
    nonadmin_users.extend(UserProfile.objects.filter(organization = score.task.organization, is_active = True))
    for user in nonadmin_users:
        if user.is_active and user.email and user.email not in admin_rcpt:
            if user == comment.user:
                if user.notify_self_comment:
                    #self comment
                    nonadmin_rcpt.append(user.email)
            else:
                if user.notify_comment:
                    nonadmin_rcpt.append(user.email)
    #get only uniq emails
    nonadmin_rcpt=list(set(nonadmin_rcpt))


    url = '%s://%s%s' % (request.is_secure() and 'https' or 'http', request.get_host(), reverse('exmo.exmo2010.view.score.score_view', args=[score.pk]))
    t = loader.get_template('exmo2010/score_comment_email.html')
    c = Context({ 'score': score, 'user': comment.user, 'admin': False, 'comment':comment, 'url': url })
    message = t.render(c)
    for rcpt_ in nonadmin_rcpt:
        if  rcpt_ == comment.user.email:
            #self
            headers['X-iifd-exmo-comment-self'] = 'True'
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [rcpt_], [], headers = headers,)
        email.send()


    t = loader.get_template('exmo2010/score_comment_email.html')
    c = Context({ 'score': comment.content_object, 'user': comment.user, 'admin': True, 'comment':comment, 'url': url })
    message_admin = t.render(c)
    for rcpt_ in admin_rcpt:
        if  rcpt_ == comment.user.email:
            #self
            headers['X-iifd-exmo-comment-self'] = 'True'
        email = EmailMessage(subject, message_admin, settings.DEFAULT_FROM_EMAIL, [rcpt_], [], headers = headers)
        email.send()



def claim_notification(sender, **kwargs):
    claim = kwargs['claim']
    request = kwargs['request']
    score = claim.score
    subject = _('%(prefix)s%(monitoring)s - %(org)s: %(code)s - New claim') % {
            'prefix': settings.EMAIL_SUBJECT_PREFIX,
            'monitoring': score.task.organization.monitoring,
            'org': score.task.organization.name.split(':')[0],
            'code': score.parameter.code,
            }


    url = '%s://%s%s' % (request.is_secure() and 'https' or 'http', request.get_host(), reverse('exmo.exmo2010.view.score.score_view', args=[score.pk]))
    t = loader.get_template('exmo2010/claim_email.html')
    c = Context({ 'score': claim.score, 'claim': claim, 'url': url })
    message = t.render(c)
    headers = {
        'X-iifd-exmo': 'claim_notification'
    }
    rcpt = []
    for user in User.objects.filter(is_superuser = True):
        if user.email and user.is_active:
            rcpt.append(user.email)
    if score.task.user.email:
        rcpt.append(score.task.user.email)
    rcpt=list(set(rcpt))
    if rcpt:
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [rcpt], [], headers = headers)
        email.send()



from reversion import revision
@disable_for_loaddata
def post_save_model(sender, instance, created, **kwargs):
    must_register = False
    if revision.is_registered(instance.__class__):
        revision.unregister(instance.__class__)
        must_register = True
    #update task openness hook
    from exmo.exmo2010 import models
    if instance.__class__ == models.Score:
        instance.task.update_openness()
    if instance.__class__ == models.Monitoring:
        for task in models.Task.objects.filter(organization__monitoring = instance).select_related(): task.update_openness()
    if instance.__class__ == models.Parameter:
        for task in models.Task.objects.filter(score__parameter = instance).select_related(): task.update_openness()
    if must_register:
        revision.register(instance.__class__)



def create_profile(sender, instance, created, **kwargs):
    if created:
        from exmo.exmo2010 import models
        profile = models.UserProfile(user = instance)
        profile.save()



def create_calendar(sender, instance, created, **kwargs):
    if created:
        instance.create_calendar()



def score_change_notify(sender, **kwargs):
    form = kwargs['form']
    score = form.instance
    request = kwargs['request']
    changes = []
    if form.changed_data:
        for change in form.changed_data:
            change_dict = {'field': change, 'was': form.initial.get(change, form.fields[change].initial), 'now': form.cleaned_data[change]}
            changes.append(change_dict)
    if score.task.approved:
        from exmo.exmo2010 import models
        rcpt = []
        for profile in models.UserProfile.objects.filter(organization = score.task.organization):
            if profile.user.is_active and profile.user.email and profile.notify_score_change:
                rcpt.append(profile.user.email)
        rcpt = list(set(rcpt))
        subject = _('%(prefix)s%(monitoring)s - %(org)s: %(code)s - Score changed') % {
            'prefix': settings.EMAIL_SUBJECT_PREFIX,
            'monitoring': score.task.organization.monitoring,
            'org': score.task.organization.name.split(':')[0],
            'code': score.parameter.code,
        }
        headers = {
            'X-iifd-exmo': 'score_changed_notification'
        }
        url = '%s://%s%s' % (request.is_secure() and 'https' or 'http', request.get_host(), reverse('exmo.exmo2010.view.score.score_view', args=[score.pk]))
        t = loader.get_template('exmo2010/score_email.html')
        c = Context({ 'score': score, 'url': url, 'changes': changes, })
        message = t.render(c)
        for rcpt_ in rcpt:
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [rcpt_], [], headers = headers)
            email.send()
