from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if isinstance(obj, Project):
            return (obj.created_by == request.user or 
                    request.user in obj.members.all() or 
                    request.user.role == 'ADMIN')
        
        if hasattr(obj, 'project'):
            return (obj.project.created_by == request.user or 
                    request.user in obj.project.members.all() or 
                    request.user.role == 'ADMIN')
        
        return False


class IsAssignedUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        return (obj.assigned_to == request.user or 
                request.user.role == 'ADMIN')
