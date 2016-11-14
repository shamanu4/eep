from django.conf.urls import url
from base.views import index, login

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
]