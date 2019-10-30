from django.contrib import admin

from web.models import *


# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'menus',]
    list_editable = ['title', 'url', 'menus',  ]


admin.site.register(Role)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(UserInfo)
admin.site.register(Payment)
admin.site.register(Customer)
admin.site.register(menu)
