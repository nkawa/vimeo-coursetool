from django.contrib import admin
from .models import Ticket, Media, Course, UserProfile
# Register your models here.

admin.site.register(Ticket)
admin.site.register(Media)
admin.site.register(Course)
admin.site.register(UserProfile)