from rest_framework import serializers
from api.models import Page, Component, Project
import json

class PageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Page model with validation
    """
    owner = serializers.StringRelatedField(read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    
    class Meta:
        model = Page
        fields = ['id', 'name', 'layout_config', 'project', 'project_name', 'project_id', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def validate_layout_config(self, value):
        """
        Validate that layout_config follows the expected JSON schema
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("layout_config must be a JSON object")
        
        # Check for required fields
        if 'components' not in value:
            raise serializers.ValidationError("layout_config must contain a 'components' field")
        
        components = value.get('components', [])
        if not isinstance(components, list):
            raise serializers.ValidationError("components must be a list")
        
        # Validate each component
        for i, component in enumerate(components):
            if not isinstance(component, dict):
                raise serializers.ValidationError(f"Component {i} must be an object")
            
            # Required fields for each component
            required_fields = ['id', 'type', 'x', 'y', 'w', 'h', 'props']
            for field in required_fields:
                if field not in component:
                    raise serializers.ValidationError(f"Component {i} missing required field: {field}")
            
            # Validate component type
            valid_types = [
                # Basic Components
                'Button', 'Input', 'Text', 'Table',
                # Form Components
                'Form', 'Select',
                # Input Components
                'CurrencyInput', 'DatePicker', 'FilePicker', 'PhoneInput', 'RichTextEditor',
                # Button Components
                'ButtonGroup', 'IconButton', 'MenuButton',
                # Display Components
                'Chart', 'Custom', 'Iframe', 'List', 'MapChart', 'StatsBox',
                # Layout Components
                'Container', 'Divider', 'JSONForm', 'Modal', 'Tabs',
                # Media Components
                'Audio', 'DocumentViewer', 'Image', 'Video',
                # Toggle Components
                'Checkbox', 'CheckboxGroup', 'RadioGroup', 'Switch', 'SwitchGroup',
                # Slider Components
                'CategorySlider', 'NumberSlider', 'RangeSlider',
                # Content Components
                'Map', 'Progress', 'Rating'
            ]
            if component['type'] not in valid_types:
                raise serializers.ValidationError(f"Component {i} has invalid type: {component['type']}")
            
            # Validate position and size are numbers
            for field in ['x', 'y', 'w', 'h']:
                if not isinstance(component[field], (int, float)):
                    raise serializers.ValidationError(f"Component {i} field {field} must be a number")
            
            # Validate props is an object
            if not isinstance(component['props'], dict):
                raise serializers.ValidationError(f"Component {i} props must be an object")
        
        return value

    def validate_name(self, value):
        """
        Validate page name
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Page name cannot be empty")
        
        if len(value) > 255:
            raise serializers.ValidationError("Page name cannot exceed 255 characters")
        
        return value.strip()
    
    def create(self, validated_data):
        """
        Ensure the project belongs to the current user
        """
        project = validated_data.get('project')
        if project and project.owner != self.context['request'].user:
            raise serializers.ValidationError("You can only create pages in your own projects")
        
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class PageDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Page with its components
    """
    components = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField(read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    
    class Meta:
        model = Page
        fields = ['id', 'name', 'layout_config', 'project', 'project_name', 'project_id', 'components', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_components(self, obj):
        from api.serializers.component_serializers import ComponentSerializer
        components = Component.objects.filter(page=obj)
        return ComponentSerializer(components, many=True).data

class PageListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for page lists
    """
    owner = serializers.StringRelatedField(read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    component_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = ['id', 'name', 'project', 'project_name', 'project_id', 'owner', 'component_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_component_count(self, obj):
        return Component.objects.filter(page=obj).count()
