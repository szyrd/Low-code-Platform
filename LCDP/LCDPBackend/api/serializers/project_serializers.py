from rest_framework import serializers
from api.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model
    """
    owner = serializers.StringRelatedField(read_only=True)
    pages_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'device_type', 'owner', 'pages_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_pages_count(self, obj):
        return obj.pages.count()
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_name(self, value):
        """
        Validate project name
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Project name cannot be empty")
        
        if len(value) > 255:
            raise serializers.ValidationError("Project name cannot exceed 255 characters")
        
        # Check for unique project name per user
        user = self.context['request'].user
        if Project.objects.filter(name=value.strip(), owner=user).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("You already have a project with this name")
        
        return value.strip()

class ProjectListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for project lists
    """
    owner = serializers.StringRelatedField(read_only=True)
    pages_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'device_type', 'owner', 'pages_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_pages_count(self, obj):
        return obj.pages.count() 