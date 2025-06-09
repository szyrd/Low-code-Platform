from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from api.models import Page, Project
from api.serializers.page_serializers import PageSerializer, PageDetailSerializer, PageListSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a page to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the page.
        return obj.owner == request.user


class PageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Page model with authentication
    """
    queryset = Page.objects.all()  # Default queryset for router registration
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """
        This view should return a list of all pages for the currently authenticated user.
        Optionally filter by project if project parameter is provided.
        """
        user = self.request.user
        if user.is_authenticated:
            queryset = Page.objects.filter(owner=user).order_by('-updated_at')
            
            # Filter by project if provided
            project_id = self.request.query_params.get('project', None)
            if project_id is not None:
                queryset = queryset.filter(project_id=project_id)
            
            return queryset
        return Page.objects.none()
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'list':
            return PageListSerializer
        elif self.action == 'retrieve':
            return PageDetailSerializer
        return PageSerializer
    
    def perform_create(self, serializer):
        """
        Save the page with the current user as owner
        Ensure the project belongs to the current user
        """
        project = serializer.validated_data.get('project')
        if project and project.owner != self.request.user:
            raise PermissionDenied("You can only create pages in your own projects")
        
        serializer.save(owner=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific page, ensuring user ownership
        """
        page = get_object_or_404(Page, pk=kwargs.get('pk'), owner=request.user)
        serializer = self.get_serializer(page)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        Update a page, ensuring user ownership
        """
        page = get_object_or_404(Page, pk=kwargs.get('pk'), owner=request.user)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(page, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a page, ensuring user ownership
        """
        page = get_object_or_404(Page, pk=kwargs.get('pk'), owner=request.user)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Returns the 5 most recently updated pages for the current user
        """
        recent_pages = self.get_queryset()[:5]
        serializer = PageListSerializer(recent_pages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """
        Create a copy of an existing page
        """
        original_page = get_object_or_404(Page, pk=pk, owner=request.user)
        
        # Create new page with modified name
        new_name = f"{original_page.name} (Copy)"
        counter = 1
        while Page.objects.filter(name=new_name, project=original_page.project).exists():
            new_name = f"{original_page.name} (Copy {counter})"
            counter += 1
        
        new_page = Page.objects.create(
            name=new_name,
            layout_config=original_page.layout_config,
            project=original_page.project,
            owner=request.user
        )
        
        serializer = PageSerializer(new_page)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
