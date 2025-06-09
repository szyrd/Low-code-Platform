from api.views.page_views import PageViewSet
from api.views.component_views import ComponentViewSet
from api.views.project_views import ProjectViewSet
from api.views.auth_views import CustomTokenObtainPairView, register_view, user_profile

__all__ = ['PageViewSet', 'ComponentViewSet', 'ProjectViewSet', 'CustomTokenObtainPairView', 'register_view', 'user_profile']
