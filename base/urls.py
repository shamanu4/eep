from django.conf.urls import url
from base.views import index, login_view, logout_view, institution_perms, building_perms, no_permissions, create_institution, create_building, remove_inst_perms, remove_build_perms

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^institution_(?P<institution_id>\d+)/$', institution_perms, name='institution_perms'),
    url(r'^building_(?P<pk>\d+)/$', building_perms, name='building_perms'),
    url(r'^create_institution$', create_institution, name='create_institution'),
    url(r'^create_building', create_building, name='create_building'),
    url(r'^no_access/$', no_permissions, name='no_permissions'),
    url(r'^remove_inst_(?P<institution_id>\d+)_user_(?P<user_id>\d+)/$', remove_inst_perms, name='remove_inst_perms'),
    url(r'^remove_build_(?P<id>\d+)_user_(?P<user_id>\d+)/$', remove_build_perms, name='remove_build_perms'),
]