from __future__ import unicode_literals
from builtins import object
from django.utils.translation import ugettext_lazy as _

from django_cradmin.viewhelpers import objecttable
from django_cradmin import crapp
from devilry.devilry_nodeadmin.models import Page
from devilry.apps.core.models import node

class PagesQuerySetForRoleMixin(object):
    """
    Used by listing, update and delete view to ensure
    that only pages that the current role has access to
    is available.
    """
    def get_queryset_for_role(self, site):
        return Page.objects.filter(site=site)


class TitleColumn(objecttable.MultiActionColumn):
    modelfield = 'title'

    def get_buttons(self, obj):
        return [
            objecttable.Button(
                label='Edit',
                url=self.reverse_appurl('edit', args=[obj.id])),
            objecttable.PagePreviewButton(
                label='View',
                url=self.reverse_appurl('preview', args=[obj.id])),
            objecttable.Button(
                label='Delete',
                url=self.reverse_appurl('delete', args=[obj.id]),
                buttonclass="danger"),
        ]


class PagesListView(PagesQuerySetForRoleMixin, objecttable.ObjectTableView):
    model = node.Node
    enable_previews = True
    columns = [
        TitleColumn,
    ]
    #searchfields = ['node_title']

    def get_buttons(self):
        app = self.request.cradmin_app
        return [
            objecttable.Button(_('Create'), url=app.reverse_appurl('create')),
        ]

    def get_multiselect_actions(self):
        app = self.request.cradmin_app
        return [
            objecttable.MultiSelectAction(
                label=_('edit'),
                url=app.reverse_appurl('multiedit')
            ),
        ]

    # def get_context_data(self, **kwargs):
    #     context = super(PagesListView, self).get_context_data(**kwargs)
    #     queryset = self.model.q_is_admin(self.request.user)
    #
    #     print queryset
    #     context['nodes'] = queryset.all()
    #
    #     return context


class App(crapp.App):

    appurls = [
        crapp.Url(
            r'^$', PagesListView.as_view(),
            name=crapp.INDEXVIEW_NAME),
    ]