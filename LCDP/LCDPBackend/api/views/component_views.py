from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import Component, Page
from api.serializers.component_serializers import (
    ComponentSerializer, 
    ComponentCreateSerializer, 
    ComponentUpdateSerializer
)


class ComponentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Component model with authentication
    """
    queryset = Component.objects.all()  # Default queryset for router registration
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return components for pages owned by the current user
        """
        user = self.request.user
        if not user.is_authenticated:
            return Component.objects.none()
            
        page_id = self.request.query_params.get('page_id', None)
        
        if page_id:
            # Filter by specific page (ensure user owns the page)
            page = get_object_or_404(Page, pk=page_id, owner=user)
            return Component.objects.filter(page=page).order_by('created_at')
        
        # Return all components for user's pages
        user_pages = Page.objects.filter(owner=user)
        return Component.objects.filter(page__in=user_pages).order_by('-updated_at')
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'create':
            return ComponentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ComponentUpdateSerializer
        return ComponentSerializer
    
    def perform_create(self, serializer):
        """
        Create component and associate with the specified page
        """
        page_id = self.request.data.get('page_id') or self.request.query_params.get('page_id')
        if not page_id:
            raise ValueError("page_id is required")
        
        page = get_object_or_404(Page, pk=page_id, owner=self.request.user)
        serializer.save(page=page)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific component, ensuring user owns the page
        """
        component = get_object_or_404(
            Component, 
            pk=kwargs.get('pk'), 
            page__owner=request.user
        )
        serializer = self.get_serializer(component)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        Update a component, ensuring user owns the page
        """
        component = get_object_or_404(
            Component, 
            pk=kwargs.get('pk'), 
            page__owner=request.user
        )
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(component, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a component, ensuring user owns the page
        """
        component = get_object_or_404(
            Component, 
            pk=kwargs.get('pk'), 
            page__owner=request.user
        )
        component.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def by_page(self, request):
        """
        Filter components by page id (for user's pages only)
        """
        page_id = request.query_params.get('page_id', None)
        if not page_id:
            return Response({'error': 'page_id parameter is required'}, status=400)
        
        try:
            page = get_object_or_404(Page, pk=page_id, owner=request.user)
            components = Component.objects.filter(page=page).order_by('created_at')
            serializer = self.get_serializer(components, many=True)
            return Response(serializer.data)
        except Page.DoesNotExist:
            return Response({'error': 'Page not found or access denied'}, status=404)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Filter components by type (for user's pages only)
        """
        component_type = request.query_params.get('type', None)
        if not component_type:
            return Response({'error': 'type parameter is required'}, status=400)
        
        user_pages = Page.objects.filter(owner=request.user)
        components = Component.objects.filter(
            page__in=user_pages, 
            type=component_type
        ).order_by('-updated_at')
        
        serializer = self.get_serializer(components, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """
        Delete multiple components by IDs
        """
        component_ids = request.data.get('ids', [])
        if not component_ids:
            return Response({'error': 'ids parameter is required'}, status=400)
        
        # Ensure all components belong to user's pages
        components = Component.objects.filter(
            id__in=component_ids,
            page__owner=request.user
        )
        
        deleted_count = components.count()
        components.delete()
        
        return Response({
            'message': f'Successfully deleted {deleted_count} components'
        }, status=status.HTTP_200_OK)
