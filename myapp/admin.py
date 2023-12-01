from import_export import resources
from import_export.admin import ImportExportMixin
from django.contrib import admin
from .models import UserProfile
class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile

class UserProfileAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = UserProfileResource

admin.site.register(UserProfile)

