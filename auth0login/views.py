from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from urllib.parse import urlencode
from django.template import loader
from django.contrib.auth.models import Group, User
from .models import setTicket, Course, Media, UserProfile, MediaViewCount
from django.core.exceptions import ObjectDoesNotExist

from .vimeo_api import GetVimeoThummnail, GetVimeoDuration
from django.utils import timezone

import traceback
import json
import requests


def index(request):
    user = request.user
#    return redirect(dashboard)
    print("Check Auth in Index",user)
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'index.html')


# obtain touser from auth user
#def get_tmi_online_user(user):




@login_required
def dashboard(request):
    user = request.user
    try:  # check if login (for admin user)
        auth0user = user.social_auth.get(provider='auth0')
        print("Got User! in Dashboard", user,auth0user)
    # check if userProfile is created.
        up =  UserProfile.objects.get(user=user)
        up.save()
        print("Get UserProfile!",up)
    except ObjectDoesNotExist:
        print("Can't get userProfile!")
        up =  UserProfile.objects.create(user=user)
        return redirect(user_settings)
    except:
        print("No login",user)
        traceback.print_exc()
        return redirect(logout)
   
   
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

    html_template =  loader.get_template( 'dashboard.html' )
    return HttpResponse(html_template.render(context, request))

#    return render(request, 'dashboard.html', {
#        'auth0User': auth0user,
#        'userdata': json.dumps(userdata, indent=4)
#    })


@login_required
def user_settings(request):
    user = request.user
    try:
        auth0user = user.social_auth.get(provider='auth0')
        up , ok= UserProfile.objects.get_or_create(user=user)
    except:
        return redirect(logout)

    context = {}
    context['segment'] = 'settings'
    context['auth0pic'] = auth0user.extra_data['picture']
    context['profinp'] = 'view'
    context['username'] = user.username
    context['first_name'] = user.first_name
    context['last_name'] = user.last_name
    context['up'] = up  # UserProfile
    context['email'] = auth0user.extra_data['email']
 
    html_template =  loader.get_template( 'settings.html' )
    return HttpResponse(html_template.render(context, request))


@login_required
def profile(request):
    user = request.user
    try:
        auth0user = user.social_auth.get(provider='auth0')
        up , cd= UserProfile.objects.get_or_create(user=user)
        print("Print UserProfile is created",up,cd)
    except:
        return redirect(logout)
    print("Print UserProfile is created2",up)
    print("User",up.user)

    if request.method == "POST":
        print(request.POST)
        user.last_name = request.POST['last_name']
        user.first_name = request.POST['first_name']
        user.email = request.POST['email']
        up.position = request.POST['position']
        up.zip = request.POST['zip']
        up.city = request.POST['city']
        up.affi = request.POST['affi']
        user.save()
        up.save()


    context = {}
    context['segment'] = 'settings'
    context['auth0pic'] = auth0user.extra_data['picture']
    context['profinp'] = 'edit'
    context['up'] = up  # UserProfile
    context['email'] = auth0user.extra_data['email']

    html_template =  loader.get_template( 'profile.html' )
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
        # needs to find ticket
        if setTicket(user,token):
            return redirect(videos)
        context['err_message'] = "Error with Keyword! Please retry."        

    auth0user = user.social_auth.get(provider='auth0')
    context['segment'] = 'register'
    context['auth0pic'] = auth0user.extra_data['picture']

    html_template =  loader.get_template( 'register.html' )
    return HttpResponse(html_template.render(context, request))


def get_thumbnail(media):  # vimeo の embed から thumbnail を取得
    response = requests.get("https://vimeo.com/api/oembed.json?url=https://vimeo.com/"+media.vid)
    print("Get Video Thum:"+media.vid, response.status_code)
    if response.status_code == 404:
        url = GetVimeoThummnail(media.vid)
        if len(url)>0:
            media.thumb_url = url
            media.save()
        return
    dict = json.loads(response.text)
    print(dict)
    if 'thumbnail_url' in dict:
        media.thumb_url = dict['thumbnail_url']
        media.save()
    else: #thumbnail is not public...
        url = GetVimeoThummnail(media.vid)
        if len(url)>0:
            media.thumb_url = url
            media.save()
        return

def get_duration(media):  # vimeo の API から duration を取得
    dur = GetVimeoDuration(media.vid)
    print("Get Video Duraion:"+media.vid, dur)
    media.duration = int(dur)
    media.save()

@login_required
def videos(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    try:
        up = UserProfile.objects.get(user=user)
    except: #とりあえず、エラー回避 (ここには来ないはず)
        up = None

    # 各コースを見て、それぞれのグループを有しているかを確認
    gall = user.groups.all()
    gnames = [g.name for g in gall]
    
#    course_all = Course.objects.all()
    course_all = Course.objects.order_by('order')
    cs_titles = []
    n = 0
    for cs in course_all:
        if any((cs.group == g) for g in gall):  # ここでグループチェック
            nn = []
            for media in cs.mlist.order_by('order'):   #メディアチェック
                if media.enabled:
                    if media.thumb_url == '':  #サムネールが無い場合
                        get_thumbnail(media)
                    if media.duration == 0:    #時間が無い場合
                        get_duration(media)
                    viewPercent = 0
                    currentTime = 0
                    if up is not None:
                        mc = up.viewcount.filter(media=media)
                        if len(mc)>0:
                            currentTime = mc[0].currentTime
                            viewPercent = int(currentTime*100/media.duration)
                            print("Percent:",currentTime, media.duration,viewPercent )
                    nn.append((media.theme, media.name,media.lecturer, media.vid,n, media.thumb_url,
                               int(media.duration/60), media.duration%60, media.viewCount, media.likeCount,
                               viewPercent, currentTime
                                ))
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


# ビデオの視聴状況のレポート
@login_required
def set_video(request):
    user = request.user
#    print("User:",user) # user があるのか？
    if 'vid' in request.POST:
        vid = request.POST['vid']
    else:
        print("Not good!")
        return HttpResponse("{}")

    if 'currentTime' in request.POST:
        ct = request.POST['currentTime']
        sp = request.POST['cspeed']
    # まずは、 UserProfileの取得
        try:
            up = UserProfile.objects.get(user=user)
#            print("Got!",vid,ct,sp)
    # vid があるかをチェック
            media = Media.objects.get(vid=vid)

            vlist = up.viewcount.filter(media=media)
            if len(vlist) == 0:
 #               print("No count!")
                mvc = MediaViewCount.objects.create(media=media,
                    currentTime=int(float(ct)))
                up.viewcount.add(mvc)
                media.viewCount = media.viewCount+1
                media.save()
                mvc.save()
                up.save()
            else:
                # すでに視聴履歴があった場合は、時刻を update
                mvc = vlist[0]
                mvc.currentTime = int(float(ct))
                mvc.lastview_time = timezone.now() #保存時点
                mvc.save()
            print("Saved mediaViewCount",mvc)

        except ObjectDoesNotExist:
            print("Can't get userProfile! or media")
            return HttpResponse("No up or media")

    return HttpResponse("{}")



# １つのビデオだけをみる
@login_required
def view_video(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    try:
        up = UserProfile.objects.get(user=user)
    except: #とりあえず、エラー回避 (ここには来ないはず)
        up = None    
#
    if 'vid' in request.GET:
        view_id = request.GET['vid']
        #print("Show video of"+view_id)
    
    # 各コースを見て、それぞれのグループを有しているかを確認
    gall = user.groups.all()
    gnames = [g.name for g in gall]
    
#    course_all = Course.objects.all()
    course_all = Course.objects.order_by('order')
    cs_titles = []
    n = 0
    for cs in course_all:
        if any((cs.group == g) for g in gall):  # ここでグループチェック
            nn = []
            for media in cs.mlist.order_by('order'):   #メディアチェック
                if media.enabled:
                    if media.vid == view_id: #　対象のビデオかどうか
                        currentTime = 0
                        if up is not None:
                            mc = up.viewcount.filter(media=media)
                            if len(mc)>0:
                                currentTime = mc[0].currentTime
                                print("set currentTime ",currentTime)
                        nn.append((media.theme, media.name,media.lecturer, media.vid, currentTime, int(currentTime/60),currentTime%60))
                        n += 1
            if len(nn)> 0:
                cs_titles.append((cs.name,nn))

    context = {}
    context['segment'] = 'videos'
    context['auth0pic'] = auth0user.extra_data['picture']
    context['cs_titles'] = cs_titles
    context['vs'] = cs_titles[0][1][0]
    context['novideo'] = False
    if len(cs_titles)== 0:
        context['novideo'] = True

    html_template =  loader.get_template( 'view_video.html' )
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
