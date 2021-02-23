from rest_framework import permissions
from .models import Tournament


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user


class IsOrganizerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_organizer


class IsTournamentOrganizerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        tid = request.resolver_match.kwargs.get('tid')
        tournament = Tournament.objects.get(id=tid)
        return request.user.is_authenticated and tournament.organizer == request.user
