from rest_framework import permissions


class IsAuthorListView(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_user():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed only for author
        return obj.author == request.user


class IsAuthorDetailView(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed only for author
        return obj.author == request.user
