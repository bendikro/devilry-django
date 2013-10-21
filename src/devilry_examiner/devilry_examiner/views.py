from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from extjs4.views import Extjs4AppView


class AppView(Extjs4AppView):
    template_name = "devilry_examiner/app.django.html"
    appname = 'devilry_examiner'
    title = _('Examiner - Devilry')


class DashboardView(TemplateView):
    template_name = "devilry_examiner/dashboard.html"
