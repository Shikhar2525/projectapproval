from django.contrib import admin
from .models import team,UserProfile,ProjectUpload,Comment
# Register your models here.
admin.site.register(team)
admin.site.register(UserProfile)
admin.site.register(ProjectUpload)
admin.site.register(Comment)