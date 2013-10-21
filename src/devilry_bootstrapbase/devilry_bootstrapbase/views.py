from django.views.generic.base import TemplateView


class BootstrapExampleView(TemplateView):
    template_name = "devilry_bootstrapbase/example.django.html"

    #def get_context_data(self, **kwargs):
        #context = super(BootstrapExampleView, self).get_context_data(**kwargs)
        #context['latest_articles'] = Article.objects.all()[:5]
        #return context
