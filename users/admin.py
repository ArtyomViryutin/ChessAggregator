from django.contrib import admin

from .models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_organizer', 'profile')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'birthdate')


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
