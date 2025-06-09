from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    PageViewSet, 
    ComponentViewSet, 
    ProjectViewSet,
    CustomTokenObtainPairView,
    register_view,
    user_profile
)
from .views.generation_views import generate_project, generation_status
from .views.ai_views import (
    PSOLayoutOptimizationView,
    ColorSchemeOptimizationView,
    NLPComponentGenerationView,
    SmartRecommendationView,
    TranslationView,
    optimization_history,
    nlp_feedback,
    ai_statistics,
    batch_optimize_layouts,
    generate_component_variations
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'pages', PageViewSet, basename='page')
router.register(r'components', ComponentViewSet, basename='component')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', register_view, name='register'),
    path('auth/profile/', user_profile, name='user_profile'),
    
    # Generation endpoints
    path('projects/<int:project_id>/generate/', generate_project, name='generate_project'),
    path('projects/<int:project_id>/generation/status/', generation_status, name='generation_status'),
    
    # AI功能端点
    path('ai/pso/optimize-layout/', PSOLayoutOptimizationView.as_view(), name='pso_optimize_layout'),
    path('ai/pso/optimize-colors/', ColorSchemeOptimizationView.as_view(), name='pso_optimize_colors'),
    path('ai/nlp/generate-component/', NLPComponentGenerationView.as_view(), name='nlp_generate_component'),
    path('ai/nlp/recommend/', SmartRecommendationView.as_view(), name='nlp_recommend'),
    path('ai/nlp/translate/', TranslationView.as_view(), name='nlp_translate'),
    path('ai/nlp/variations/', generate_component_variations, name='nlp_variations'),
    path('ai/history/', optimization_history, name='optimization_history'),
    path('ai/feedback/', nlp_feedback, name='nlp_feedback'),
    path('ai/statistics/', ai_statistics, name='ai_statistics'),
    path('ai/batch/optimize-layouts/', batch_optimize_layouts, name='batch_optimize_layouts'),
] 