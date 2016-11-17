from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login as login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from guardian.shortcuts import assign_perm, remove_perm, get_perms, get_objects_for_user
from base.models import User, Institution, Building, Component, Feature, Meter
from base.forms import InstitutionForm, BuildingForm, ComponentTypeForm, ComponentForm, FeatureTypeForm, FeatureForm, \
    MeterTypeForm, MeterForm


def index(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))

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
    return render(
        request,
        'base/index.html',
        {
            'institutions': institutions,
            'buildings': buildings,
            'create_objects_perm': create_objects_perm,
            'create_components_perm': create_components_perm
        }
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse("index"))
    else:
        form = AuthenticationForm()
    return render(
        request,
        'base/login.html',
        {'form': form}
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def no_permissions(request):
    return render(request, 'base/no_access.html', {})


def institution_perms(request, institution_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    try:
        inst = Institution.objects.get(pk=institution_id)
    except Institution.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    else:
        if user.has_perm('base.delegate_permissions'):
            descendants = user.get_descendants()
            permissions = get_perms(user, inst)
            permissions.append('delegate_permissions')
            if user.has_perm('base.create_objects'):
                permissions.append('create_objects')
            if user.has_perm('base.create_components'):
                permissions.append('create_components')
            list = []
            for des in descendants:
                a = get_perms(des, inst)
                if des.has_perm('base.create_objects'):
                    a.append('create_objects')
                if des.has_perm('base.delegate_permissions'):
                    a.append('delegate_permissions')
                if des.has_perm('base.create_components'):
                    a.append('create_components')
                b = {'name': des,
                     'perms': a}
                list.append(b)
            if request.GET.get('u') and request.GET.get('p'):
                perm_user = User.objects.get(id=request.GET['u'])
                cur_perm = request.GET['p']
                builds = Building.objects.filter(institution=institution_id)
                if cur_perm == 'lead_institution':
                    assign_perm('lead_institution', perm_user, inst)
                    assign_perm('view_institution', perm_user, inst)
                    for build in builds:
                        assign_perm('lead_building', perm_user, build)
                        assign_perm('view_building', perm_user, build)
                elif cur_perm == 'view_institution':
                    assign_perm('view_institution', perm_user, inst)
                    for build in builds:
                        assign_perm('view_building', perm_user, build)
                elif cur_perm == 'create_objects' or cur_perm == 'delegate_permissions' or cur_perm == 'create_components':
                    permission = Permission.objects.get(codename=cur_perm)
                    perm_user.user_permissions.add(permission)
                return HttpResponseRedirect(reverse("institution_perms", kwargs={'institution_id': inst.id}))
            return render(
                request,
                'base/add_perms.html',
                {
                    'descendants': descendants,
                    'inst': inst,
                    'permissions': permissions,
                    'list': list,
                }
            )
        else:
            return HttpResponseRedirect(reverse("no_permissions"))


def building_perms(request, pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    try:
        build = Building.objects.get(pk=pk)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    else:
        if user.has_perm('base.delegate_permissions'):
            descendants = user.get_descendants()
            permissions = get_perms(user, build)
            permissions.append('delegate_permissions')
            if user.has_perm('base.create_objects'):
                permissions.append('create_objects')
            if user.has_perm('base.create_components'):
                permissions.append('create_components')
            list = []
            for des in descendants:
                a = get_perms(des, build)
                if des.has_perm('base.create_objects'):
                    a.append('create_objects')
                if des.has_perm('base.delegate_permissions'):
                    a.append('delegate_permissions')
                if des.has_perm('base.create_components'):
                    a.append('create_components')
                b = {'name': des,
                     'perms': a}
                list.append(b)
            if request.GET.get('u') and request.GET.get('p'):
                perm_user = User.objects.get(id=request.GET['u'])
                cur_perm = request.GET['p']
                if cur_perm == 'lead_building':
                    assign_perm('view_building', perm_user, build)
                    assign_perm('lead_building', perm_user, build)
                if cur_perm == 'view_building':
                    assign_perm('view_building', perm_user, build)
                elif cur_perm == 'create_objects' or cur_perm == 'delegate_permissions' or cur_perm == 'create_components':
                    permission = Permission.objects.get(codename=cur_perm)
                    perm_user.user_permissions.add(permission)
                return HttpResponseRedirect(reverse("building_perms", kwargs={'pk': build.id}))
            return render(
                request,
                'base/add_perms.html',
                {
                    'build': build,
                    'descendants': descendants,
                    'permissions': permissions,
                    'list': list,
                }
            )
        else:
            return HttpResponseRedirect(reverse("no_permissions"))


def create_object(request, type):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    if user.has_perm('base.create_objects'):
        institutions = get_objects_for_user(user, 'base.view_institution')
        if request.method == 'POST':
            if type == '1':
                form = InstitutionForm(request.POST)
            else:
                form = BuildingForm(institutions, request.POST)
            if form.is_valid():
                form.save()
                name = form.cleaned_data['name']
                if type == '1':
                    obj = Institution.objects.get(name=name)
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
        return HttpResponseRedirect(reverse("no_permissions"))


def remove_perms(request, id, user_id, type):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))
    if type == '1':
        obj = Institution.objects.get(pk=id)
        perm = 'lead_institution'
    else:
        obj = Building.objects.get(pk=id)
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
            if type == '1':
                return HttpResponseRedirect(reverse("institution_perms", kwargs={'institution_id': obj.id}))
            else:
                return HttpResponseRedirect(reverse("building_perms", kwargs={'pk': obj.id}))
        return render(
            request,
            'base/remove_perms.html',
            {
                'obj': obj,
                'user': user,
                'permissions': permissions
            }
        )
    else:
        return HttpResponseRedirect(reverse("no_permissions"))


def edit_object(request, id, type):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))
    if type == '1':
        obj = Institution.objects.get(pk=id)
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
        if type == '2':
            obj = Building.objects.get(pk=id)
        elif type == '3':
            obj = Feature.objects.get(pk=id)
        else:
            obj = Meter.objects.get(pk=id)
        if user.has_perm('lead_building', obj):
            institutions = get_objects_for_user(user, 'base.view_institution')
            buildings = get_objects_for_user(user, 'base.view_building').order_by('institution')
            if type == '2':
                form = BuildingForm(institutions, request.POST or None, instance=obj)
            elif type == '3':
                form = FeatureForm(request.POST or None, instance=obj)
            else:
                form = MeterForm(institutions, buildings, request.POST or None, instance=obj)
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
            return HttpResponseRedirect(reverse("no_permissions"))


def view_object(request, id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))
    try:
        obj = Building.objects.get(pk=id)

    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    else:
        if user.has_perm('view_building', obj):
            comps = Component.objects.filter(building=obj.id)
            features_list = []
            for comp in comps:
                features = Feature.objects.filter(component_id=comp.id)
                for feature in features:
                    features_list.append(feature)
            meters = Meter.objects.filter(building_id=obj.id)
            return render(
                request,
                'base/view_object.html',
                {
                    'obj': obj,
                    'comps': comps,
                    'features_list': features_list,
                    'meters': meters
                }
            )
        else:
            return HttpResponseRedirect(reverse("no_permissions"))


def create_comp_or_feature(request, type):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))
    if user.has_perm('base.create_components'):
        buildings = get_objects_for_user(user, 'base.lead_building')
        institutions = get_objects_for_user(user, 'base.view_institution')
        if request.method == 'POST':
            if type == '3':
                form = ComponentTypeForm(request.POST)
            elif type == '4':
                form = ComponentForm(buildings, request.POST)
            elif type == '5':
                form = FeatureTypeForm(request.POST)
            elif type == '6':
                form = FeatureForm(request.POST)
            elif type == '7':
                form = MeterTypeForm(request.POST)
            else:
                form = MeterForm(institutions, buildings, request.POST)
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            if type == '3':
                form = ComponentTypeForm()
            elif type == '4':

                form = ComponentForm(buildings)
            elif type == '5':
                form = FeatureTypeForm()
            elif type == '6':
                form = FeatureForm()
            elif type == '7':
                form = MeterTypeForm()
            else:
                form = MeterForm(institutions, buildings)
        return render(
            request,
            'base/create_object.html',
            {
                'type': type,
                'form': form
            })
    else:
        return HttpResponseRedirect(reverse("no_permissions"))