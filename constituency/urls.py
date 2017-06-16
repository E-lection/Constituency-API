from django.conf.urls import url

from . import views

app_name = 'constituency'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote_encrypted/$', views.vote_encrypted, name='vote_encrypted'),
    url(r'^get_votes/$', views.get_votes, name='get_votes')
]
