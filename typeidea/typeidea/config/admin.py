from django.contrib import admin

from .models import Link, SideBar


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'href', 'owner', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)

admin.site.register(Link, LinkAdmin)



class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content', 'owner', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)

admin.site.register(SideBar, SideBarAdmin)
