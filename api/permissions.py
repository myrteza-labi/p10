from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributor

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user == request.user

class IsContributor(BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk') or request.data.get('project')
        if project_id:
            return Contributor.objects.filter(user=request.user, project_id=project_id).exists()
        return False
