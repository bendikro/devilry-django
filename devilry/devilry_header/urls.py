from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views.about_me import AboutMeView
from .views.change_language import ChangeLanguageView


urlpatterns = patterns('devilry.devilry_header',
    url('^about_me$',
        login_required(AboutMeView.as_view()),
        name='devilry_header_aboutme'),
    url('^change_language$',
        login_required(ChangeLanguageView.as_view()),
        name='devilry_change_language'),
)
