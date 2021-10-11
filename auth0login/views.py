from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from urllib.parse import urlencode
from django.template import loader
from django.contrib.auth.models import Group, User
from .models import setTicket, Course, Media

import json


def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'index.html')


@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email']
    }

    context = {}
    context['segment'] = 'dashboard'
    context['auth0user'] = auth0user
    context['auth0pic'] = auth0user.extra_data['picture']
    print(context)

    html_template =  loader.get_template( 'dashboard.html' )
    return HttpResponse(html_template.render(context, request))

#    return render(request, 'dashboard.html', {
#        'auth0User': auth0user,
#        'userdata': json.dumps(userdata, indent=4)
#    })


@login_required
def user_settings(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email']
    }

    context = {}
    context['segment'] = 'settings'
    context['auth0pic'] = auth0user.extra_data['picture']


    html_template =  loader.get_template( 'settings.html' )
    return HttpResponse(html_template.render(context, request))


@login_required
def usages(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    context = {}
    context['segment'] = 'usages'
    context['auth0pic'] = auth0user.extra_data['picture']

    html_template =  loader.get_template( 'usages.html' )
    return HttpResponse(html_template.render(context, request))

@login_required
def register(request):
    user = request.user
    context = {}
    context['err_message'] = ""
    if request.method == "POST":
        token = request.POST['ticket_name']
        print("Ticket Keyword is ",token)
        # needs to find ticket
        if setTicket(user,token):
            return redirect(videos)
        context['err_message'] = "Error with Keyword! Please retry."        

    auth0user = user.social_auth.get(provider='auth0')
    context['segment'] = 'register'
    context['auth0pic'] = auth0user.extra_data['picture']

    html_template =  loader.get_template( 'register.html' )
    return HttpResponse(html_template.render(context, request))



@login_required
def videos(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    
    # 各コースを見て、それぞれのグループを有しているかを確認
    gall = user.groups.all()
    gnames = [g.name for g in gall]
    
    print(gall)
    course_all = Course.objects.all()
    cs_titles = []
    n = 0
    for cs in course_all:
        if any((cs.group == g) for g in gall):
            nn = []
            for media in cs.mlist.all():
                if media.enabled:
                    nn.append((media.theme, media.name,media.lecturer, media.vid,n ))
                    n += 1
            cs_titles.append((cs.name,nn))

    context = {}
    context['segment'] = 'videos'
    context['auth0pic'] = auth0user.extra_data['picture']
    context['cs_titles'] = cs_titles
    context['novideo'] = False
    if len(cs_titles)== 0:
        context['novideo'] = True

    html_template =  loader.get_template( 'videos.html' )
    return HttpResponse(html_template.render(context, request))


def privacy(request):
    context = {}
    user = request.user
    if not user.is_anonymous:
        auth0user = user.social_auth.get(provider='auth0')
        context['auth0pic'] = auth0user.extra_data['picture']
    else:
        context['auth0pic'] = ""
    context['segment'] = 'privacy'
    html_template =  loader.get_template( 'privacy.html' )
    return HttpResponse(html_template.render(context, request))

def terms(request):
    context = {}
    user = request.user
    if not user.is_anonymous:
        auth0user = user.social_auth.get(provider='auth0')
        context['auth0pic'] = auth0user.extra_data['picture']
    else:
        context['auth0pic'] = ""
    context['segment'] = 'terms'
    html_template =  loader.get_template( 'terms.html' )
    return HttpResponse(html_template.render(context, request))



def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)
