"""
NLP组件生成器模块
用于LCDP平台的自然语言处理和智能组件生成
"""

import re
import json
import jieba
import hashlib
from typing import Dict, List, Optional, Tuple
from django.utils import timezone
from django.conf import settings
from .models import ComponentTemplate, NLPTrainingData, AICache

# 中文分词和关键词提取
jieba.initialize()


class ChineseNLPProcessor:
    """中文自然语言处理器"""
    
    def __init__(self):
        # 组件类型关键词映射
        self.component_keywords = {
            'Button': ['按钮', 'button', '点击', '提交', '确认', '取消', '保存', '删除', '编辑', '查看'],
            'Input': ['输入', 'input', '输入框', '文本框', '输入框', '文本输入', '输入字段'],
            'Text': ['文本', 'text', '标题', '标签', '描述', '说明', '提示'],
            'Table': ['表格', 'table', '列表', '数据表', '表单', '数据展示'],
            'Form': ['表单', 'form', '表格', '输入表单', '数据输入'],
            'Select': ['选择', 'select', '下拉', '选择框', '下拉框', '选项'],
            'Checkbox': ['复选框', 'checkbox', '多选', '勾选', '选择'],
            'RadioGroup': ['单选', 'radio', '单选框', '单选组'],
            'Switch': ['开关', 'switch', '切换'],
            'Slider': ['滑块', 'slider', '滑动', '数值选择'],
            'Image': ['图片', 'image', '图像', '照片'],
            'Video': ['视频', 'video', '播放器'],
            'Chart': ['图表', 'chart', '统计图', '数据可视化', '柱状图', '饼图', '折线图', '曲线图', '面积图', '环形图', 'bar', 'pie', 'line', 'area', 'doughnut'],
            'Map': ['地图', 'map', '位置'],
            'Modal': ['弹窗', 'modal', '对话框', '弹出框'],
            'Tabs': ['标签页', 'tabs', '选项卡'],
            'Progress': ['进度条', 'progress', '进度'],
            'Rating': ['评分', 'rating', '星级'],
            'Container': ['容器', 'container', '布局'],
            'Divider': ['分割线', 'divider', '分隔符']
        }
        
        # 属性关键词映射
        self.property_keywords = {
            'color': {
                '红色': 'red', '蓝色': 'blue', '绿色': 'green', '黄色': 'yellow',
                '黑色': 'black', '白色': 'white', '灰色': 'gray', '紫色': 'purple',
                '橙色': 'orange', '粉色': 'pink', '主要': 'primary', '次要': 'secondary',
                '成功': 'success', '警告': 'warning', '危险': 'danger', '信息': 'info'
            },
            'size': {
                '大': 'large', '中': 'medium', '小': 'small', '很大': 'xl', '很小': 'xs',
                '大型': 'large', '中型': 'medium', '小型': 'small'
            },
            'type': {
                '主要': 'primary', '次要': 'secondary', '默认': 'default',
                '文本': 'text', '链接': 'link', '虚线': 'dashed'
            },
            'position': {
                '左': 'left', '右': 'right', '中': 'center', '上': 'top', '下': 'bottom',
                '居中': 'center', '左对齐': 'left', '右对齐': 'right'
            }
        }
        
        # 组件模板
        self.component_templates = {
            'Button': {
                'type': 'Button',
                'properties': {
                    'text': '按钮',
                    'color': 'primary',
                    'size': 'medium',
                    'disabled': False,
                    'loading': False
                }
            },
            'Input': {
                'type': 'Input',
                'properties': {
                    'placeholder': '请输入...',
                    'type': 'text',
                    'required': False,
                    'disabled': False,
                    'maxlength': 100
                }
            },
            'Text': {
                'type': 'Text',
                'properties': {
                    'content': '文本内容',
                    'fontSize': '14px',
                    'color': '#333',
                    'fontWeight': 'normal'
                }
            },
            'Table': {
                'type': 'Table',
                'properties': {
                    'columns': [],
                    'data': [],
                    'pagination': True,
                    'bordered': True
                }
            },
            'Select': {
                'type': 'Select',
                'properties': {
                    'options': [],
                    'placeholder': '请选择...',
                    'multiple': False,
                    'clearable': True
                }
            },
            'Chart': {
                'type': 'Chart',
                'properties': {
                    'type': 'bar',
                    'data': [
                        {'name': 'A', 'value': 30, 'color': '#4F46E5'},
                        {'name': 'B', 'value': 80, 'color': '#10B981'},
                        {'name': 'C', 'value': 45, 'color': '#F59E0B'},
                        {'name': 'D', 'value': 60, 'color': '#EF4444'}
                    ],
                    'color': '#4F46E5',
                    'title': ''
                }
            }
        }
    
    def extract_component_intent(self, description: str) -> Tuple[Optional[str], Dict]:
        """从自然语言描述中提取组件意图"""
        # 分词
        words = list(jieba.cut(description.lower()))
        
        # 识别组件类型
        component_type = self._identify_component_type(words, description)
        
        # 提取属性
        properties = self._extract_properties(words, description, component_type)
        
        return component_type, properties
    
    def _identify_component_type(self, words: List[str], description: str) -> Optional[str]:
        """识别组件类型"""
        scores = {}
        
        # 计算每种组件类型的匹配分数
        for comp_type, keywords in self.component_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in description or keyword in words:
                    score += 1
                    # 完全匹配给更高分数
                    if keyword in description:
                        score += 0.5
            
            if score > 0:
                scores[comp_type] = score
        
        # 返回得分最高的组件类型
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return None
    
    def _extract_properties(self, words: List[str], description: str, 
                           component_type: Optional[str]) -> Dict:
        """提取组件属性"""
        properties = {}
        
        # 提取颜色
        for keyword, value in self.property_keywords['color'].items():
            if keyword in description:
                properties['color'] = value
                break
        
        # 提取尺寸
        for keyword, value in self.property_keywords['size'].items():
            if keyword in description:
                properties['size'] = value
                break
        
        # 提取特定的文本内容
        text_content = self._extract_text_content(description, component_type)
        if text_content:
            if component_type == 'Button':
                properties['text'] = text_content
            elif component_type == 'Text':
                properties['content'] = text_content
            elif component_type == 'Input':
                properties['placeholder'] = text_content
        
        # 提取数字属性
        numbers = re.findall(r'\d+', description)
        if numbers and component_type in ['Input', 'Slider']:
            if component_type == 'Input':
                properties['maxlength'] = int(numbers[0])
            elif component_type == 'Slider':
                properties['max'] = int(numbers[0])
        
        # 提取布尔属性
        if '必填' in description or '必须' in description:
            properties['required'] = True
        if '禁用' in description or '不可用' in description:
            properties['disabled'] = True
        if '多选' in description:
            properties['multiple'] = True
        
        return properties
    
    def _extract_text_content(self, description: str, component_type: Optional[str]) -> Optional[str]:
        """提取文本内容"""
        # 使用正则表达式提取引号内的内容
        quoted_matches = re.findall(r'["""]([^"""]+)["""]', description)
        if quoted_matches:
            return quoted_matches[0]
        
        # 提取"内容是"、"文字是"等模式
        content_patterns = [
            r'内容是(.+?)(?:[，。,.]|$)',
            r'文字是(.+?)(?:[，。,.]|$)',
            r'显示(.+?)(?:[，。,.]|$)',
            r'标题(.+?)(?:[，。,.]|$)'
        ]
        
        for pattern in content_patterns:
            matches = re.findall(pattern, description)
            if matches:
                return matches[0].strip()
        
        return None
    
    def generate_component(self, description: str, user_id: Optional[int] = None) -> Dict:
        """生成组件配置"""
        # 检查缓存
        cache_key = self._generate_cache_key(description)
        cached_result = self._get_cached_result(cache_key, 'NLP_COMPONENT')
        if cached_result:
            return cached_result
        
        # 提取组件意图
        component_type, extracted_props = self.extract_component_intent(description)
        
        if not component_type:
            # 尝试智能推理
            component_type = self._intelligent_fallback(description)
        
        if not component_type:
            return {
                'success': False,
                'message': '无法理解您的描述，请尝试更具体的描述',
                'suggestions': self._generate_suggestions(description)
            }
        
        # 获取基础模板
        template = self.component_templates.get(component_type, {}).copy()
        if not template:
            return {
                'success': False,
                'message': f'不支持的组件类型: {component_type}'
            }
        
        # 应用提取的属性
        template['properties'].update(extracted_props)
        
        # 智能填充默认值
        self._fill_smart_defaults(template, description, component_type)
        
        result = {
            'success': True,
            'component': template,
            'confidence': self._calculate_confidence(description, component_type, extracted_props),
            'description': description
        }
        
        # 保存训练数据
        if user_id:
            self._save_training_data(description, template, user_id)
        
        # 缓存结果
        self._cache_result(cache_key, 'NLP_COMPONENT', result)
        
        return result
    
    def _intelligent_fallback(self, description: str) -> Optional[str]:
        """智能后备推理"""
        # 基于描述长度和内容推理
        if len(description) < 10:
            if any(char in description for char in ['输入', '框']):
                return 'Input'
            elif any(char in description for char in ['按', '钮', '点']):
                return 'Button'
        
        # 基于动词推理
        verbs = ['点击', '输入', '选择', '显示', '查看']
        for verb in verbs:
            if verb in description:
                if verb in ['点击']:
                    return 'Button'
                elif verb in ['输入']:
                    return 'Input'
                elif verb in ['选择']:
                    return 'Select'
                elif verb in ['显示', '查看']:
                    return 'Text'
        
        return None
    
    def _fill_smart_defaults(self, template: Dict, description: str, component_type: str):
        """智能填充默认值"""
        properties = template.get('properties', {})
        
        if component_type == 'Button':
            # 智能生成按钮文本
            if not properties.get('text') or properties['text'] == '按钮':
                properties['text'] = self._generate_button_text(description)
        
        elif component_type == 'Input':
            # 智能生成输入框占位符
            if not properties.get('placeholder') or properties['placeholder'] == '请输入...':
                properties['placeholder'] = self._generate_input_placeholder(description)
        
        elif component_type == 'Text':
            # 智能生成文本内容
            if not properties.get('content') or properties['content'] == '文本内容':
                properties['content'] = self._generate_text_content(description)
        
        elif component_type == 'Chart':
            # 智能生成图表配置
            self._fill_chart_defaults(properties, description)
    
    def _fill_chart_defaults(self, properties: Dict, description: str):
        """智能填充图表默认配置"""
        desc_lower = description.lower()
        
        # 根据描述确定图表类型
        if any(keyword in desc_lower for keyword in ['饼图', 'pie', '饼状', '圆形图']):
            properties['type'] = 'pie'
        elif any(keyword in desc_lower for keyword in ['折线图', 'line', '线图', '曲线', '趋势']):
            properties['type'] = 'line'
        elif any(keyword in desc_lower for keyword in ['面积图', 'area', '填充图']):
            properties['type'] = 'area'
        elif any(keyword in desc_lower for keyword in ['环形图', 'doughnut', '甜甜圈']):
            properties['type'] = 'doughnut'
        else:
            properties['type'] = 'bar'  # 默认柱状图
        
        # 智能生成图表标题
        title = self._extract_chart_title(description)
        if title:
            properties['title'] = title
        
        # 根据描述生成示例数据
        chart_data = self._generate_chart_data(description)
        if chart_data:
            properties['data'] = chart_data
    
    def _extract_chart_title(self, description: str) -> str:
        """提取图表标题"""
        # 提取引号内的标题
        quoted_matches = re.findall(r'["""]([^"""]+)["""]', description)
        if quoted_matches:
            return quoted_matches[0]
        
        # 提取"标题是"、"名称是"等模式
        title_patterns = [
            r'标题是(.+?)(?:[，。,.]|$)',
            r'名称是(.+?)(?:[，。,.]|$)',
            r'叫做(.+?)(?:[，。,.]|$)',
            r'显示(.+?)数据',
            r'(.+?)图表',
            r'(.+?)统计'
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, description)
            if matches:
                return matches[0].strip()
        
        return ''
    
    def _generate_chart_data(self, description: str) -> List[Dict]:
        """根据描述生成图表数据"""
        # 基础多色数据
        default_data = [
            {'name': 'A', 'value': 30, 'color': '#4F46E5'},
            {'name': 'B', 'value': 80, 'color': '#10B981'},
            {'name': 'C', 'value': 45, 'color': '#F59E0B'},
            {'name': 'D', 'value': 60, 'color': '#EF4444'}
        ]
        
        # 根据描述关键词生成相应的数据
        if any(keyword in description for keyword in ['销售', '业绩', '营收']):
            return [
                {'name': '第一季度', 'value': 45, 'color': '#4F46E5'},
                {'name': '第二季度', 'value': 78, 'color': '#10B981'},
                {'name': '第三季度', 'value': 62, 'color': '#F59E0B'},
                {'name': '第四季度', 'value': 85, 'color': '#EF4444'}
            ]
        elif any(keyword in description for keyword in ['用户', '访问', '流量']):
            return [
                {'name': '周一', 'value': 120, 'color': '#4F46E5'},
                {'name': '周二', 'value': 180, 'color': '#10B981'},
                {'name': '周三', 'value': 150, 'color': '#F59E0B'},
                {'name': '周四', 'value': 220, 'color': '#EF4444'},
                {'name': '周五', 'value': 280, 'color': '#8B5CF6'}
            ]
        elif any(keyword in description for keyword in ['分类', '类型', '占比']):
            return [
                {'name': '类型A', 'value': 35, 'color': '#4F46E5'},
                {'name': '类型B', 'value': 25, 'color': '#10B981'},
                {'name': '类型C', 'value': 20, 'color': '#F59E0B'},
                {'name': '类型D', 'value': 20, 'color': '#EF4444'}
            ]
        
        return default_data
    
    def _generate_button_text(self, description: str) -> str:
        """生成按钮文字"""
        # 常见按钮文字映射
        button_texts = {
            '提交': ['提交', '保存', '确认', '发送'],
            '取消': ['取消', '关闭', '返回'],
            '删除': ['删除', '移除'],
            '编辑': ['编辑', '修改'],
            '查看': ['查看', '详情', '查看详情'],
            '搜索': ['搜索', '查询', '查找'],
            '登录': ['登录', '登录系统'],
            '注册': ['注册', '注册账号']
        }
        
        for text, keywords in button_texts.items():
            if any(keyword in description for keyword in keywords):
                return text
        
        # 默认返回
        return '确定'
    
    def _generate_input_placeholder(self, description: str) -> str:
        """生成输入框占位符"""
        placeholder_maps = {
            '姓名': '请输入姓名',
            '邮箱': '请输入邮箱地址',
            '密码': '请输入密码',
            '电话': '请输入电话号码',
            '地址': '请输入地址',
            '备注': '请输入备注信息',
            '标题': '请输入标题',
            '内容': '请输入内容'
        }
        
        for keyword, placeholder in placeholder_maps.items():
            if keyword in description:
                return placeholder
        
        return '请输入内容'
    
    def _generate_text_content(self, description: str) -> str:
        """生成文本内容"""
        # 提取描述中的关键信息
        if '标题' in description:
            return '页面标题'
        elif '描述' in description:
            return '这里是描述信息'
        elif '说明' in description:
            return '使用说明'
        elif '提示' in description:
            return '提示信息'
        
        return '文本内容'
    
    def _calculate_confidence(self, description: str, component_type: str, 
                             properties: Dict) -> float:
        """计算生成结果的置信度"""
        confidence = 0.0
        
        # 基础分数
        confidence += 0.3
        
        # 组件类型匹配度
        keywords = self.component_keywords.get(component_type, [])
        keyword_matches = sum(1 for keyword in keywords if keyword in description)
        confidence += min(keyword_matches * 0.1, 0.3)
        
        # 属性提取质量
        confidence += len(properties) * 0.05
        
        # 描述长度合理性
        if 5 <= len(description) <= 50:
            confidence += 0.2
        elif len(description) > 50:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _generate_suggestions(self, description: str) -> List[str]:
        """生成改进建议"""
        suggestions = [
            "尝试使用更具体的描述，例如：'创建一个红色的提交按钮'",
            "指定组件类型，例如：'输入框'、'按钮'、'表格'等",
            "添加颜色、大小等属性描述"
        ]
        
        if len(description) < 5:
            suggestions.insert(0, "描述太简短，请提供更多详细信息")
        
        return suggestions
    
    def _generate_cache_key(self, description: str) -> str:
        """生成缓存键"""
        return hashlib.md5(description.encode('utf-8')).hexdigest()
    
    def _get_cached_result(self, cache_key: str, cache_type: str) -> Optional[Dict]:
        """获取缓存结果"""
        try:
            cache_entry = AICache.objects.get(
                cache_type=cache_type,
                input_hash=cache_key
            )
            cache_entry.hit_count += 1
            cache_entry.last_used = timezone.now()
            cache_entry.save()
            return cache_entry.result_data
        except AICache.DoesNotExist:
            return None
    
    def _cache_result(self, cache_key: str, cache_type: str, result: Dict):
        """缓存结果"""
        try:
            AICache.objects.create(
                cache_type=cache_type,
                input_hash=cache_key,
                result_data=result
            )
        except Exception as e:
            print(f"Cache save failed: {e}")
    
    def _save_training_data(self, description: str, component: Dict, user_id: int):
        """保存训练数据"""
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            
            NLPTrainingData.objects.create(
                description=description,
                generated_component=component,
                created_by=user
            )
        except Exception as e:
            print(f"Training data save failed: {e}")


class SmartRecommendationEngine:
    """智能推荐引擎"""
    
    def __init__(self):
        self.nlp_processor = ChineseNLPProcessor()
    
    def recommend_components(self, context: Dict, existing_components: List[Dict] = None) -> List[Dict]:
        """基于上下文推荐组件"""
        recommendations = []
        
        if existing_components is None:
            existing_components = []
        
        # 分析现有组件
        existing_types = [comp.get('type') for comp in existing_components]
        
        # 基于页面类型推荐
        page_type = context.get('page_type', '')
        recommendations.extend(self._recommend_by_page_type(page_type, existing_types))
        
        # 基于用户行为推荐
        user_behavior = context.get('user_behavior', {})
        recommendations.extend(self._recommend_by_behavior(user_behavior, existing_types))
        
        # 基于布局分析推荐
        layout_analysis = self._analyze_layout(existing_components)
        recommendations.extend(self._recommend_by_layout(layout_analysis, existing_types))
        
        # 去重和排序
        recommendations = self._deduplicate_and_rank(recommendations)
        
        return recommendations[:5]  # 返回前5个推荐
    
    def _recommend_by_page_type(self, page_type: str, existing_types: List[str]) -> List[Dict]:
        """基于页面类型推荐"""
        page_recommendations = {
            'login': [
                {'type': 'Input', 'reason': '登录页面通常需要用户名输入框', 'priority': 10},
                {'type': 'Input', 'reason': '登录页面通常需要密码输入框', 'priority': 10},
                {'type': 'Button', 'reason': '登录页面需要登录按钮', 'priority': 9},
                {'type': 'Checkbox', 'reason': '记住密码选项', 'priority': 5}
            ],
            'form': [
                {'type': 'Input', 'reason': '表单页面需要输入字段', 'priority': 10},
                {'type': 'Select', 'reason': '表单通常有选择项', 'priority': 8},
                {'type': 'Button', 'reason': '表单需要提交按钮', 'priority': 9},
                {'type': 'Text', 'reason': '表单需要标签和说明', 'priority': 7}
            ],
            'dashboard': [
                {'type': 'Chart', 'reason': '仪表板需要数据可视化', 'priority': 10},
                {'type': 'Table', 'reason': '仪表板通常展示数据表格', 'priority': 9},
                {'type': 'Text', 'reason': '仪表板需要统计数字展示', 'priority': 8}
            ],
            'list': [
                {'type': 'Table', 'reason': '列表页面需要数据表格', 'priority': 10},
                {'type': 'Button', 'reason': '列表需要操作按钮', 'priority': 8},
                {'type': 'Input', 'reason': '列表通常有搜索功能', 'priority': 7}
            ]
        }
        
        recommendations = page_recommendations.get(page_type.lower(), [])
        
        # 过滤已存在的组件类型
        filtered = []
        for rec in recommendations:
            if existing_types.count(rec['type']) < 3:  # 允许少量重复
                filtered.append(rec)
        
        return filtered
    
    def _recommend_by_behavior(self, user_behavior: Dict, existing_types: List[str]) -> List[Dict]:
        """基于用户行为推荐"""
        recommendations = []
        
        # 最近使用的组件类型
        recent_components = user_behavior.get('recent_components', [])
        for comp_type in recent_components[:3]:  # 取最近3个
            if existing_types.count(comp_type) < 2:
                recommendations.append({
                    'type': comp_type,
                    'reason': f'您最近经常使用{comp_type}组件',
                    'priority': 6
                })
        
        # 基于项目类型的偏好
        project_preferences = user_behavior.get('project_preferences', {})
        for comp_type, usage_count in project_preferences.items():
            if usage_count > 5 and existing_types.count(comp_type) < 2:
                recommendations.append({
                    'type': comp_type,
                    'reason': f'根据您的使用习惯推荐{comp_type}',
                    'priority': 5
                })
        
        return recommendations
    
    def _analyze_layout(self, existing_components: List[Dict]) -> Dict:
        """分析现有布局"""
        analysis = {
            'component_count': len(existing_components),
            'has_form_elements': False,
            'has_display_elements': False,
            'has_navigation': False,
            'layout_density': 'low'
        }
        
        form_components = ['Input', 'Select', 'Checkbox', 'RadioGroup', 'Button']
        display_components = ['Text', 'Image', 'Chart', 'Table']
        navigation_components = ['Button', 'Tabs', 'Modal']
        
        for comp in existing_components:
            comp_type = comp.get('type', '')
            if comp_type in form_components:
                analysis['has_form_elements'] = True
            if comp_type in display_components:
                analysis['has_display_elements'] = True
            if comp_type in navigation_components:
                analysis['has_navigation'] = True
        
        # 计算布局密度
        if len(existing_components) > 10:
            analysis['layout_density'] = 'high'
        elif len(existing_components) > 5:
            analysis['layout_density'] = 'medium'
        
        return analysis
    
    def _recommend_by_layout(self, layout_analysis: Dict, existing_types: List[str]) -> List[Dict]:
        """基于布局分析推荐"""
        recommendations = []
        
        # 如果有表单元素但没有提交按钮
        if layout_analysis['has_form_elements'] and 'Button' not in existing_types:
            recommendations.append({
                'type': 'Button',
                'reason': '表单需要提交按钮',
                'priority': 9
            })
        
        # 如果组件很少，推荐基础组件
        if layout_analysis['component_count'] < 3:
            basic_components = [
                {'type': 'Text', 'reason': '页面需要文字说明', 'priority': 7},
                {'type': 'Button', 'reason': '交互需要按钮', 'priority': 8}
            ]
            recommendations.extend(basic_components)
        
        # 如果缺少显示元素
        if not layout_analysis['has_display_elements'] and layout_analysis['component_count'] > 3:
            recommendations.append({
                'type': 'Text',
                'reason': '页面需要信息展示组件',
                'priority': 6
            })
        
        return recommendations
    
    def _deduplicate_and_rank(self, recommendations: List[Dict]) -> List[Dict]:
        """去重和排序推荐结果"""
        # 去重（按类型）
        seen_types = set()
        unique_recommendations = []
        
        for rec in recommendations:
            if rec['type'] not in seen_types:
                seen_types.add(rec['type'])
                unique_recommendations.append(rec)
        
        # 按优先级排序
        unique_recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return unique_recommendations


class TranslationService:
    """多语言翻译服务"""
    
    def __init__(self):
        # 简化的翻译映射
        self.translations = {
            'en': {
                '按钮': 'Button',
                '输入框': 'Input',
                '文本': 'Text',
                '表格': 'Table',
                '确定': 'OK',
                '取消': 'Cancel',
                '提交': 'Submit',
                '保存': 'Save',
                '删除': 'Delete',
                '编辑': 'Edit',
                '查看': 'View',
                '搜索': 'Search',
                '请输入': 'Please enter'
            },
            'zh': {
                'Button': '按钮',
                'Input': '输入框',
                'Text': '文本',
                'Table': '表格',
                'OK': '确定',
                'Cancel': '取消',
                'Submit': '提交',
                'Save': '保存',
                'Delete': '删除',
                'Edit': '编辑',
                'View': '查看',
                'Search': '搜索',
                'Please enter': '请输入'
            }
        }
    
    def translate_component(self, component: Dict, target_language: str) -> Dict:
        """翻译组件内容"""
        if target_language not in self.translations:
            return component
        
        translation_map = self.translations[target_language]
        translated_component = component.copy()
        
        # 翻译组件属性
        properties = translated_component.get('properties', {})
        
        for key, value in properties.items():
            if isinstance(value, str) and value in translation_map:
                properties[key] = translation_map[value]
        
        return translated_component
    
    def auto_translate_interface(self, components: List[Dict], 
                                source_lang: str, target_lang: str) -> List[Dict]:
        """自动翻译界面"""
        translated_components = []
        
        for component in components:
            translated = self.translate_component(component, target_lang)
            translated_components.append(translated)
        
        return translated_components 