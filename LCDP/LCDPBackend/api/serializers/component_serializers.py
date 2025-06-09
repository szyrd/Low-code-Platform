from rest_framework import serializers
from api.models import Component, Page

class ComponentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Component model with validation
    """
    page_name = serializers.ReadOnlyField(source='page.name')
    
    class Meta:
        model = Component
        fields = ['id', 'page', 'page_name', 'type', 'properties', 'created_at', 'updated_at']
        read_only_fields = ['id', 'page_name', 'created_at', 'updated_at']

    def validate_type(self, value):
        """
        Validate that the component type is in the allowed list
        """
        allowed_types = [choice[0] for choice in Component.COMPONENT_TYPES]
        if value not in allowed_types:
            raise serializers.ValidationError(
                f"Invalid component type '{value}'. Allowed types: {', '.join(allowed_types)}"
            )
        return value

    def validate_properties(self, value):
        """
        Validate component properties based on type
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("Properties must be a JSON object")
        
        # Type-specific validation could be added here
        # For now, just ensure it's a valid dict
        return value

    def validate(self, attrs):
        """
        Validate the component data
        """
        # Ensure the page belongs to the user making the request
        if 'page' in attrs:
            page = attrs['page']
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                if page.owner != request.user:
                    raise serializers.ValidationError("You can only add components to your own pages")
        
        return attrs


class ComponentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating components with page validation
    """
    
    class Meta:
        model = Component
        fields = ['type', 'properties']

    def validate_type(self, value):
        """
        Validate that the component type is in the allowed list
        """
        allowed_types = [choice[0] for choice in Component.COMPONENT_TYPES]
        if value not in allowed_types:
            raise serializers.ValidationError(
                f"Invalid component type '{value}'. Allowed types: {', '.join(allowed_types)}"
            )
        return value

    def validate_properties(self, value):
        """
        Validate component properties
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("Properties must be a JSON object")
        
        return value


class ComponentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating components
    """
    
    class Meta:
        model = Component
        fields = ['type', 'properties']
        
    def validate_type(self, value):
        """
        Validate that the component type is in the allowed list
        """
        allowed_types = [choice[0] for choice in Component.COMPONENT_TYPES]
        if value not in allowed_types:
            raise serializers.ValidationError(
                f"Invalid component type '{value}'. Allowed types: {', '.join(allowed_types)}"
            )
        return value
