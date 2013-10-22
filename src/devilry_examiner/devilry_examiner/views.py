from django.views.generic.base import TemplateView


class DashboardView(TemplateView):
    template_name = "devilry_examiner/dashboard.django.html"
