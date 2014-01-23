from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from devilry_gradingsystem.pluginregistry import gradingsystempluginregistry
from devilry_gradingsystem.pluginregistry import GradingSystemPluginInterface


class SchemaPluginApi(GradingSystemPluginInterface):
    id = 'devilry_gradingsystemplugin_schema'
    title = _('Fill in a schema')
    description = _('You define a schema that your examiners/correctors have to use to provide feedback.')

    def get_edit_feedback_url(self, deliveryid):
        return reverse('devilry_gradingsystemplugin_schema_feedbackeditor', kwargs={'deliveryid': deliveryid})

    #def get_bulkedit_feedback_url(self, assignmentid):
    #    return reverse('devilry_gradingsystemplugin_schema_feedbackbulkeditor', kwargs={'assignmentid': assignmentid})

gradingsystempluginregistry.add(SchemaPluginApi)
