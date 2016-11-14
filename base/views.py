from django.shortcuts import render
from guardian.shortcuts import get_objects_for_user
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("login")
    buildings = get_objects_for_user(request.user, 'base.view_buildings').order_by('institution')
    return render(
        request,
        'base/index.html',
        {'buildings': buildings}
    )


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth(request, form.get_user())
            return HttpResponseRedirect(reverse("index"))

    else:
        form = AuthenticationForm()
    return render(
        request,
        'base/login.html',
        {'form': form}
    )