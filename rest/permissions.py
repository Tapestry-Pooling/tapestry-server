from rest_framework import permissions


class IsLabOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.lab_id.id or request.user.is_staff


class IsTestOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.assigned.lab_id == request.user.lab_id or request.user.is_staff


class IsUserOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.lab_id == request.user.lab_id or request.user.is_staff


class IsLabMemberOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return int(view.kwargs['lab_pk']) == request.user.lab_id.id or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.lab_id == request.user.lab_id or request.user.is_staff


class IsLabTestOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return int(view.kwargs['lab_pk']) == request.user.lab_id.id or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.assigned_to.lab_id == request.user.lab_id or request.user.is_staff

