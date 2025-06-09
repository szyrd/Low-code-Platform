"""
AI功能相关视图 - PSO和NLP API端点
"""

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..ai_optimizer import ComponentLayoutOptimizer, ColorSchemeOptimizer
from ..nlp_generator import ChineseNLPProcessor, SmartRecommendationEngine, TranslationService
from ..models import OptimizationHistory, Project, Page


class PSOLayoutOptimizationView(APIView):
    """PSO布局优化视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            components = request.data.get('components', [])
            constraints = request.data.get('constraints', {})
            project_id = request.data.get('project_id')
            page_id = request.data.get('page_id')
            
            if not components:
                return Response({
                    'success': False,
                    'message': '组件列表不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 设置默认约束
            default_constraints = {
                'canvas_width': 1200,
                'canvas_height': 800,
                'min_spacing': 10,
                'max_iterations': 100,
                'swarm_size': 30
            }
            default_constraints.update(constraints)
            
            # 执行PSO优化
            optimizer = ComponentLayoutOptimizer(
                swarm_size=default_constraints['swarm_size'],
                max_iterations=default_constraints['max_iterations']
            )
            
            result = optimizer.optimize_layout(components, default_constraints)
            
            # 保存优化历史
            if project_id:
                try:
                    project = Project.objects.get(id=project_id, owner=request.user)
                    page = None
                    if page_id:
                        page = Page.objects.get(id=page_id, project=project)
                    
                    OptimizationHistory.objects.create(
                        project=project,
                        page=page,
                        optimization_type='PSO',
                        input_data={
                            'components': components,
                            'constraints': default_constraints
                        },
                        output_data=result,
                        performance_metrics={
                            'fitness_score': result.get('fitness_score', 0),
                            'iterations': result.get('iterations', 0),
                            'improvement': result.get('improvement', 0)
                        },
                        user=request.user
                    )
                except (Project.DoesNotExist, Page.DoesNotExist):
                    pass  # 不影响主要功能
            
            return Response({
                'success': True,
                'result': result,
                'message': f'布局优化完成，经过{result.get("iterations", 0)}次迭代'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'优化失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ColorSchemeOptimizationView(APIView):
    """颜色方案优化视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            base_color = request.data.get('base_color', '#3498db')
            requirements = request.data.get('requirements', {})
            
            # 设置默认要求
            default_requirements = {
                'num_colors': 5,
                'min_contrast_ratio': 4.5,
                'accessibility_level': 'AA'
            }
            default_requirements.update(requirements)
            
            # 执行颜色优化
            optimizer = ColorSchemeOptimizer()
            result = optimizer.optimize_color_scheme(base_color, default_requirements)
            
            return Response({
                'success': True,
                'result': result,
                'message': '配色方案优化完成'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'配色优化失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NLPComponentGenerationView(APIView):
    """NLP组件生成视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            description = request.data.get('description', '').strip()
            language = request.data.get('language', 'zh')
            
            if not description:
                return Response({
                    'success': False,
                    'message': '请提供组件描述'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if len(description) > 500:
                return Response({
                    'success': False,
                    'message': '描述过长，请控制在500字符以内'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 使用NLP处理器生成组件
            processor = ChineseNLPProcessor()
            result = processor.generate_component(description, request.user.id)
            
            return Response(result)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'组件生成失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SmartRecommendationView(APIView):
    """智能组件推荐视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            context = request.data.get('context', '')
            existing_components = request.data.get('existing_components', [])
            current_page_type = request.data.get('page_type', 'general')
            
            if not context:
                return Response({
                    'success': False,
                    'message': '请提供推荐上下文'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 使用智能推荐引擎
            recommender = SmartRecommendationEngine()
            recommendations = recommender.get_smart_recommendations(
                context, existing_components, current_page_type, request.user.id
            )
            
            return Response({
                'success': True,
                'recommendations': recommendations,
                'message': f'基于上下文推荐了{len(recommendations)}个组件'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'推荐生成失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TranslationView(APIView):
    """多语言翻译视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            components = request.data.get('components', [])
            source_language = request.data.get('source_language', 'zh')
            target_language = request.data.get('target_language', 'en')
            
            if not components:
                return Response({
                    'success': False,
                    'message': '组件列表不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 执行翻译
            translator = TranslationService()
            translated_components = translator.auto_translate_interface(
                components, source_language, target_language
            )
            
            return Response({
                'success': True,
                'translated_components': translated_components,
                'message': f'成功翻译{len(translated_components)}个组件'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'翻译失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def optimization_history(request):
    """获取优化历史记录"""
    try:
        project_id = request.GET.get('project_id')
        optimization_type = request.GET.get('type')
        limit = int(request.GET.get('limit', 10))
        
        queryset = OptimizationHistory.objects.filter(user=request.user)
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        if optimization_type:
            queryset = queryset.filter(optimization_type=optimization_type)
        
        history = queryset[:limit]
        
        history_data = []
        for record in history:
            history_data.append({
                'id': record.id,
                'project_name': record.project.name,
                'page_name': record.page.name if record.page else None,
                'optimization_type': record.optimization_type,
                'performance_metrics': record.performance_metrics,
                'created_at': record.created_at.isoformat()
            })
        
        return Response({
            'success': True,
            'history': history_data,
            'total': queryset.count()
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取历史记录失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nlp_feedback(request):
    """NLP生成结果反馈"""
    try:
        data = request.data
        description = data.get('description')
        generated_component = data.get('generated_component')
        feedback_score = data.get('feedback_score')  # 1-5分
        is_correct = data.get('is_correct')
        corrected_component = data.get('corrected_component')
        
        if not description or not generated_component:
            return Response({
                'success': False,
                'message': '缺少必要参数'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 保存反馈数据
        from ..models import NLPTrainingData
        training_data = NLPTrainingData.objects.create(
            description=description,
            generated_component=generated_component,
            user_feedback=feedback_score,
            is_correct=is_correct,
            corrected_component=corrected_component,
            created_by=request.user
        )
        
        return Response({
            'success': True,
            'message': '感谢您的反馈，这将帮助我们改进AI功能',
            'training_data_id': training_data.id
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'反馈保存失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_statistics(request):
    """AI功能使用统计"""
    try:
        user = request.user
        
        # 统计优化历史
        optimization_stats = {}
        for opt_type in ['PSO', 'NLP', 'LAYOUT', 'COLOR']:
            count = OptimizationHistory.objects.filter(
                user=user, 
                optimization_type=opt_type
            ).count()
            optimization_stats[opt_type] = count
        
        # 统计NLP训练数据
        from ..models import NLPTrainingData
        nlp_stats = {
            'total_generations': NLPTrainingData.objects.filter(created_by=user).count(),
            'positive_feedback': NLPTrainingData.objects.filter(
                created_by=user, 
                user_feedback__gte=4
            ).count(),
            'corrections_made': NLPTrainingData.objects.filter(
                created_by=user, 
                corrected_component__isnull=False
            ).count()
        }
        
        # 缓存命中率统计
        from ..models import AICache
        cache_stats = {
            'total_cache_entries': AICache.objects.count(),
            'total_hits': sum(cache.hit_count for cache in AICache.objects.all())
        }
        
        return Response({
            'success': True,
            'statistics': {
                'optimization_usage': optimization_stats,
                'nlp_usage': nlp_stats,
                'cache_performance': cache_stats
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'统计数据获取失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 批量处理视图
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def batch_optimize_layouts(request):
    """批量布局优化"""
    try:
        data = request.data
        pages_data = data.get('pages', [])
        global_constraints = data.get('constraints', {})
        
        if not pages_data:
            return Response({
                'success': False,
                'message': '页面数据不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = []
        optimizer = ComponentLayoutOptimizer()
        
        for page_data in pages_data:
            page_id = page_data.get('page_id')
            components = page_data.get('components', [])
            page_constraints = {**global_constraints, **page_data.get('constraints', {})}
            
            try:
                result = optimizer.optimize_layout(components, page_constraints)
                results.append({
                    'page_id': page_id,
                    'success': True,
                    'result': result
                })
            except Exception as e:
                results.append({
                    'page_id': page_id,
                    'success': False,
                    'error': str(e)
                })
        
        successful_count = sum(1 for r in results if r['success'])
        
        return Response({
            'success': True,
            'results': results,
            'summary': {
                'total_pages': len(pages_data),
                'successful_optimizations': successful_count,
                'failed_optimizations': len(pages_data) - successful_count
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'批量优化失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_component_variations(request):
    """生成组件变体"""
    try:
        data = request.data
        base_description = data.get('description', '')
        variation_count = min(int(data.get('count', 3)), 10)  # 最多10个变体
        
        if not base_description:
            return Response({
                'success': False,
                'message': '请提供基础描述'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        processor = ChineseNLPProcessor()
        variations = []
        
        # 生成变体描述
        variation_templates = [
            f"{base_description}，大尺寸",
            f"{base_description}，小尺寸", 
            f"{base_description}，红色主题",
            f"{base_description}，蓝色主题",
            f"{base_description}，简约风格",
            f"{base_description}，详细版本",
            f"简化的{base_description}",
            f"高级{base_description}",
            f"{base_description}，带图标",
            f"{base_description}，无边框"
        ]
        
        for i in range(variation_count):
            if i < len(variation_templates):
                variation_desc = variation_templates[i]
            else:
                variation_desc = f"{base_description}，变体{i+1}"
            
            try:
                result = processor.generate_component(variation_desc, request.user.id)
                if result.get('success'):
                    variations.append({
                        'description': variation_desc,
                        'component': result['component'],
                        'confidence': result.get('confidence', 0)
                    })
            except Exception as e:
                continue  # 跳过失败的变体
        
        return Response({
            'success': True,
            'variations': variations,
            'base_description': base_description,
            'generated_count': len(variations)
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'变体生成失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 