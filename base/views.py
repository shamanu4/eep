from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm, remove_perm, get_perms, get_objects_for_user
from base.models import User, Institution, Building, Component, Feature, Meter
from base.forms import InstitutionForm, BuildingForm, ComponentTypeForm, ComponentForm, FeatureTypeForm, FeatureForm, \
    MeterTypeForm, MeterForm, MeterDataForm, RateForm, ReceiptForm, UserForm
from invitations.models import Invitation


def index(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        institutions = get_objects_for_user(user, 'base.view_institution')
        buildings = get_objects_for_user(user, 'base.view_building').order_by('institution')
        if user.has_perm('base.create_objects'):
            create_objects_perm = True
        else:
            create_objects_perm = False
        if user.has_perm('base.create_components'):
            create_components_perm = True
        else:
            create_components_perm = False
        if user.has_perm('base.invite_users'):
            invite_users_perm = True
        else:
            invite_users_perm = False
        return render(
            request,
            'base/index.html',
            {
                'institutions': institutions,
                'buildings': buildings,
                'create_objects_perm': create_objects_perm,
                'create_components_perm': create_components_perm,
                'invite_users_perm': invite_users_perm
            }
        )


def no_permissions(request):
    return render(request, 'base/no_access.html', {})


def view_object(request, id, type):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        if type == '1':
            obj = get_object_or_404(Institution, pk=id)
            view_perm = 'view_institution'
            lead_perm = 'lead_institution'
        else:
            obj = get_object_or_404(Building, pk=id)
            view_perm = 'view_building'
            lead_perm = 'lead_building'
        if user.has_perm(view_perm, obj):
            if user.has_perm(lead_perm, obj):
                lead_perm = True
            else:
                lead_perm = False
            if user.has_perm('base.delegate_permissions'):
                delegate_perm = True
            else:
                delegate_perm = False
            if type == '2':
                comps = Component.objects.filter(building=obj.id)
                values = comps.values_list('id')
                features = Feature.objects.filter(component_id__in=values)
                meters = Meter.objects.filter(building_id=obj.id)
                builds = None
            else:
                comps = None,
                features = None
                meters = None
                builds = get_objects_for_user(user, 'base.view_building').order_by('institution')
            return render(
                request,
                'base/view_object.html',
                {
                    'obj': obj,
                    'comps': comps,
                    'features': features,
                    'meters': meters,
                    'lead_perm': lead_perm,
                    'delegate_perm': delegate_perm,
                    'builds': builds,
                    'type': type
                }
            )
        else:
            return HttpResponseRedirect('/no_access/')


def delegate_perms(request, id, type):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        user = request.user
        if type == '1':
            obj = get_object_or_404(Institution, id=id)
        else:
            obj = get_object_or_404(Building, id=id)
        if user.has_perm('base.delegate_permissions'):
            descendants = user.get_descendants()
            permissions = get_perms(user, obj)
            permissions.append('delegate_permissions')
            if user.has_perm('base.create_objects'):
                permissions.append('create_objects')
            if user.has_perm('base.create_components'):
                permissions.append('create_components')
            if user.has_perm('base.invite_users'):
                permissions.append('invite_users')
            list = []
            for des in descendants:
                a = get_perms(des, obj)
                if des.has_perm('base.create_objects'):
                    a.append('create_objects')
                if des.has_perm('base.delegate_permissions'):
                    a.append('delegate_permissions')
                if des.has_perm('base.create_components'):
                    a.append('create_components')
                if des.has_perm('base.invite_users'):
                    a.append('invite_users')
                b = {'name': des,
                     'perms': a}
                list.append(b)
            if request.GET.get('u') and request.GET.get('p'):
                perm_user = User.objects.get(id=request.GET['u'])
                cur_perm = request.GET['p']
                if type == '1':
                    builds = Building.objects.filter(institution_id=id)
                    if cur_perm == 'lead_institution':
                        assign_perm('lead_institution', perm_user, obj)
                        assign_perm('view_institution', perm_user, obj)
                        for build in builds:
                            assign_perm('lead_building', perm_user, build)
                            assign_perm('view_building', perm_user, build)
                    elif cur_perm == 'view_institution':
                        assign_perm('view_institution', perm_user, obj)
                        for build in builds:
                            assign_perm('view_building', perm_user, build)
                    elif cur_perm == 'create_objects' or cur_perm == 'delegate_permissions' or cur_perm == 'create_components' or cur_perm == 'invite_users':
                        permission = Permission.objects.get(codename=cur_perm)
                        perm_user.user_permissions.add(permission)
                else:
                    if cur_perm == 'lead_building':
                        assign_perm('view_building', perm_user, obj)
                        assign_perm('lead_building', perm_user, obj)
                    if cur_perm == 'view_building':
                        assign_perm('view_building', perm_user, obj)
                    elif cur_perm == 'create_objects' or cur_perm == 'delegate_permissions' or cur_perm == 'create_components' or cur_perm == 'invite_users':
                        permission = Permission.objects.get(codename=cur_perm)
                        perm_user.user_permissions.add(permission)
                return HttpResponseRedirect(reverse("delegate_perms", kwargs={'id': obj.id, 'type': type}))
            return render(
                request,
                'base/add_perms.html',
                {
                    'type': type,
                    'obj': obj,
                    'descendants': descendants,
                    'permissions': permissions,
                    'list': list,
                }
            )
        else:
            return HttpResponseRedirect('/no_access/')


def remove_perms(request, id, user_id, type):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    if type == '1':
        obj = get_object_or_404(Institution, pk=id)
        perm = 'lead_institution'
    else:
        obj = get_object_or_404(Building, pk=id)
        perm = 'lead_building'
    if request.user.has_perm(perm, obj):
        user = User.objects.get(pk=user_id)
        permissions = get_perms(user, obj)
        descendants = user.get_descendants()
        if user.has_perm('base.create_objects'):
            permissions.append('create_objects')
        if user.has_perm('base.delegate_permissions'):
            permissions.append('delegate_permissions')
        if user.has_perm('base.create_components'):
            permissions.append('create_components')
        if request.GET.get('p'):
            cur_perm = request.GET['p']
            if cur_perm == 'create_objects' or cur_perm == 'delegate_permissions' or cur_perm == 'create_components':
                permission = Permission.objects.get(codename=cur_perm)
                user.user_permissions.remove(permission)
                for des in descendants:
                    des.user_permissions.remove(permission)
            else:
                remove_perm(cur_perm, user, obj)
                for des in descendants:
                    remove_perm(cur_perm, des, obj)
            return HttpResponseRedirect(reverse("delegate_perms", kwargs={'id': obj.id, 'type': type}))
        return render(
            request,
            'base/remove_perms.html',
            {
                'obj': obj,
                'user': user,
                'permissions': permissions,
                'type': type
            }
        )
    else:
        return HttpResponseRedirect('/no_access/')


def create_object(request, type):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        if user.has_perm('base.create_objects'):
            institutions = get_objects_for_user(user, 'base.lead_institution')
            if request.method == 'POST':
                if type == '1':
                    form = InstitutionForm(request.POST)
                else:
                    form = BuildingForm(institutions, request.POST)
                if form.is_valid():
                    form.save()
                    name = form.cleaned_data['name']
                    if type == '1':
                        obj = get_object_or_404(Institution, name=name)
                        assign_perm('lead_institution', user, obj)
                        assign_perm('view_institution', user, obj)
                        ancestors = user.get_ancestors()
                        for ancestor in ancestors:
                            assign_perm('lead_institution', ancestor, obj)
                            assign_perm('view_institution', ancestor, obj)
                    else:
                        institution = form.cleaned_data['institution']
                        obj = Building.objects.get(name=name, institution=institution)
                        assign_perm('lead_building', user, obj)
                        assign_perm('view_building', user, obj)
                        ancestors = user.get_ancestors()
                        for ancestor in ancestors:
                            assign_perm('lead_building', ancestor, obj)
                            assign_perm('view_building', ancestor, obj)
                    return HttpResponseRedirect('/')
            else:
                if type == '1':
                    form = InstitutionForm()
                else:
                    form = BuildingForm(institutions)
            return render(
                request,
                'base/create_object.html',
                {
                    'form': form,
                    'type': type
                }
            )
        else:
            return HttpResponseRedirect('/no_access/')


def edit_object(request, obj_id, id, type):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    if type == '1':
        obj = get_object_or_404(Institution, pk=obj_id)
        form = InstitutionForm(request.POST or None, instance=obj)
        if user.has_perm('lead_institution', obj):
            if request.method == 'POST':
                form.save()
                return HttpResponseRedirect(reverse("index"))
            return render(
                request,
                'base/edit_object.html',
                {
                    'form': form,
                    "obj": obj
                }
            )
        else:
            return HttpResponseRedirect('/no_permissions/')
    else:
        perm_obj = get_object_or_404(Building, pk=obj_id)
        if type == '2':
            obj = perm_obj
        elif type == '3':
            obj = get_object_or_404(Feature, pk=id)
        elif type == '4':
            obj = get_object_or_404(Meter, pk=id)
        else:
            obj = get_object_or_404(Component, pk=id)
        if user.has_perm('lead_building', perm_obj):
            if type == '2':
                institutions = get_objects_for_user(user, 'base.lead_institution')
                form = BuildingForm(institutions, request.POST or None, instance=obj)
            elif type == '3':
                components = Component.objects.filter(building_id=obj_id)
                form = FeatureForm(components, request.POST or None, instance=obj)
            elif type == '4':
                inst = Institution.objects.filter(id=perm_obj.institution_id)
                build = Building.objects.filter(id=obj_id)
                form = MeterForm(inst, build, request.POST or None, instance=obj)
            else:
                build = Building.objects.filter(id=obj_id)
                form = ComponentForm(build, request.POST or None, instance=obj)
            if request.method == 'POST':
                form.save()
                return HttpResponseRedirect(reverse("index"))
            return render(
                request,
                'base/edit_object.html',
                {
                    'form': form,
                    "obj": obj
                }
            )
        else:
            return HttpResponseRedirect('/no_access/')


def create_item(request, type):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    if user.has_perm('base.create_components'):
        if request.method == 'POST':
            if type == '3':
                form = ComponentTypeForm(request.POST)
            elif type == '4':
                form = FeatureTypeForm(request.POST)
            elif type == '5':
                form = MeterTypeForm(request.POST)
            else:
                form = RateForm(request.POST)
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            if type == '3':
                form = ComponentTypeForm()
            elif type == '4':
                form = FeatureTypeForm()
            elif type == '5':
                form = MeterTypeForm()
            else:
                form = RateForm()
        return render(
            request,
            'base/create_object.html',
            {
                'type': type,
                'form': form
            })
    else:
        return HttpResponseRedirect('/no_access/')


def create_item_for_object(request, type, id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        obj = get_object_or_404(Building, id=id)
        if user.has_perm('lead_building', obj):
            meter = Meter.objects.filter(building_id=obj.id)
            inst = Institution.objects.filter(id=obj.institution_id)
            build = Building.objects.filter(id=id)
            components = Component.objects.filter(building_id=obj.id)
            if request.method == 'POST':
                if type == '1':
                    form = MeterDataForm(meter, request.POST)
                elif type == '2':
                    form = ReceiptForm(inst, build, request.POST)
                elif type == '3' :
                    form = ComponentForm(build, request.POST)
                elif type == '4':
                    form = FeatureForm(components, request.POST)
                else:
                    form = MeterForm(inst, build, request.POST)
                form.save()
                return HttpResponseRedirect(reverse("view_object", kwargs={'id': obj.id, 'type': 2}))
            else:
                if type == '1':
                    form = MeterDataForm(meter)
                elif type == '2':
                    form = ReceiptForm(inst, build)
                elif type == '3':
                    form = ComponentForm(build)
                elif type == '4':
                    form = FeatureForm(components)
                else:
                    form = MeterForm(inst, build)
            return render(
                request,
                'base/create_object.html',
                {
                    'type': type,
                    'form': form
                })
        else:
            return HttpResponseRedirect('/no_access/')


# def invite(request):
#     user = request.user
#     if not user.is_authenticated():
#         return HttpResponseRedirect('accounts/login/')
#     else:
#         text = ''
#         if user.has_perm('base.invite_users'):
#             if request.GET.get('e'):
#                 email = request.GET['e']
#                 invite = Invitation.create(email, inviter=request.user)
#                 invite.send_invitation(request)
#                 text = 'Запрошення на адресу %s надіслане' % email
#             return render(request, 'base/invite.html', {
#                 'text': text
#             })
#         else:
#             return HttpResponseRedirect('/no_access/')


def cabinet(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        descendants = user.get_descendants()
        return render(
            request,
            'base/cabinet.html',
            {
                'user': user,
                'descendants': descendants
            }
        )


def edit_user(request, id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        obj = get_object_or_404(User, id=id)
        descendants = user.get_descendants(include_self=True)
        if obj in descendants:
            form = UserForm(request.POST or None, instance=obj)
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/cabinet/')
            return render(
                request,
                'base/edit_object.html',
                {
                    'form': form,
                    "obj": obj
                }
            )
        else:
            return HttpResponseRedirect('/no_access/')
