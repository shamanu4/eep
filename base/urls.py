from django.conf.urls import url
from base.views import index, login_view, logout_view, no_permissions, create_object, \
    remove_perms, edit_object, view_object, create_item, create_item_for_object, delegate_perms, invite

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^delegate_perms_(?P<id>\d+)_type_(?P<type>\d+)/$', delegate_perms, name='delegate_perms'),
    url(r'^create_object_type_(?P<type>\d+)', create_object, name='create_object'),
    url(r'^no_access/$', no_permissions, name='no_permissions'),
    url(r'^remove_object_(?P<id>\d+)_user_(?P<user_id>\d+)_type_(?P<type>\d+)/$', remove_perms, name='remove_perms'),
    url(r'^edit_object_(?P<obj_id>\d+)_comp_(?P<id>\d+)_type_(?P<type>\d+)', edit_object, name='edit_object'),
    url(r'^view_object_(?P<id>\d+)_type_(?P<type>\d+)', view_object, name='view_object'),
    url(r'^create_comp_or_feature_type_(?P<type>\d+)', create_item, name='create_item'),
    url(r'^create_item_type_(?P<type>\d+)_for_object_(?P<id>\d+)', create_item_for_object, name='create_item_for_object'),
    url(r'^invite/', invite, name='invite'),


]
