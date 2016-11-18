from django.conf.urls import url
from base.views import index, login_view, logout_view, institution_perms, building_perms, no_permissions, create_object, remove_perms, edit_object, view_object, create_comp_or_feature

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^institution_(?P<institution_id>\d+)/$', institution_perms, name='institution_perms'),
    url(r'^building_(?P<pk>\d+)/$', building_perms, name='building_perms'),
    url(r'^create_object_type_(?P<type>\d+)', create_object, name='create_object'),
    url(r'^no_access/$', no_permissions, name='no_permissions'),
    url(r'^remove_object_(?P<id>\d+)_user_(?P<user_id>\d+)_type_(?P<type>\d+)/$', remove_perms, name='remove_perms'),
    url(r'^edit_object_(?P<obj_id>\d+)_comp_(?P<id>\d+)_type_(?P<type>\d+)', edit_object, name='edit_object'),
    url(r'^view_object_(?P<id>\d+)', view_object, name='view_object'),
    url(r'^create_comp_or_feature_type_(?P<type>\d+)', create_comp_or_feature, name='create_comp_or_feature'),


]
