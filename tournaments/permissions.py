from rest_framework import permissions
from .models import Tournament
from django.shortcuts import get_object_or_404


class IsOrganizerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_organizer


class IsParticipantOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('POST', 'DELETE'):
            return request.user.is_authenticated

        return False


class IsTournamentOrganizerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        tid = request.resolver_match.kwargs.get('tid')
        tournament = get_object_or_404(Tournament, id=tid)
        return request.user.is_authenticated and request.user == tournament.organizer
