from django.views.generic import TemplateView
from django.views.generic import DetailView
from devilry.apps.core.models import Delivery

class DeliveryDetailsView(DetailView):
    model = Delivery
    template_name = "devilry_student/deliverydetails.django.html"
    pk_url_kwargs = 'pk'

    