from django.contrib import admin
from .models import Ticket, Media, Course, UserProfile, MediaViewCount
# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

class MediaFilter(admin.SimpleListFilter):
    title= 'Courses'
    parameter_name= 'Courses'
    def lookups(self,request,model_admin):
        courses = [(c.name, c.name) for c in Course.objects.all()]        
        print("lookup",courses)
        return courses
    def queryset(self, request, queryset):
        cname = self.value()
        print("Query Value:",cname)
        c = Course.objects.filter(name=cname)
        if len(c) == 0: # all
            return Media.objects.all()
        return c[0].mlist.all()

# メディアの平均視聴時間
def averageVideoView(lst):
    aveView = 0.0
    aveTime = 0.0
    ll = len(lst)
    if ll == 0:
        return "None"
    for v in lst:
        aveView += 100*(v.totalViewSec/v.media.duration)
        aveTime += 100*(v.currentTime/v.media.duration)
    aveView /= ll
    aveTime /= ll
    return "Ct:"+str(ll)+",T:{t}%,V:{v}%".format(t=int(aveTime),v=int(aveView))





@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("order","name","lecturer","courses")
    search_fields = ("name","lecturer")
    list_filter = (MediaFilter,)
    def courses(self,obj):
        cs = Course.objects.filter(mlist__id=obj.id)
        lst = []
        for x in cs:
            lst.append(x.name)
        return lst

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(MediaViewCount)
class MediaViewCountAdmin(admin.ModelAdmin):
    list_display = ("media","curTimeP","totalViewTime","view_speed","viewstart_time","lastview_time")
    def curTimeP(self,obj):
        return str(int(100*obj.currentTime/obj.media.duration))+"%"
    def totalViewTime(self,obj):
        return str(int(100*obj.totalViewSec/obj.media.duration))+"%"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user_name","video_view","affi","position","zip","city","lastlogin_date")
    def user_name(self, obj):
        print("UserProfile Name!",vars(self))
        print("Object",vars(obj))
        return obj.user.first_name+" "+obj.user.last_name

    def video_view(self, obj):

        return averageVideoView(obj.viewcount.all())
