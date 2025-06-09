from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import Project
from api.serializers import ProjectSerializer, PageSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def pages(self, request, pk=None):
        """Get all pages for a specific project"""
        project = self.get_object()
        pages = project.pages.all()
        serializer = PageSerializer(pages, many=True, context={'request': request})
        return Response(serializer.data) 