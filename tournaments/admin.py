from django.contrib import admin

from .models import Participation, Tournament, AnonymousParticipation


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'open_date', 'status')


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tournament', 'status')


class AnonymousParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'tournament', 'status')


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(AnonymousParticipation, AnonymousParticipationAdmin)
