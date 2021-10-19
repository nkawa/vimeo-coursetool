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

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(MediaViewCount)
class MediaViewCountAdmin(admin.ModelAdmin):
    pass



