from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    DEVICE_CHOICES = [
        ('web', 'Web'),
        ('tablet', 'Tablet'),
        ('phone', 'Phone'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_CHOICES, default='web')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        unique_together = ['name', 'owner']  # Each user can have unique project names
    
    def __str__(self):
        return f"{self.name} (by {self.owner.username})"

class Page(models.Model):
    name = models.CharField(max_length=255)
    layout_config = models.JSONField(default=dict)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pages', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.project:
            return f"{self.name} in {self.project.name} (by {self.owner.username})"
        return f"{self.name} (by {self.owner.username})"

class Component(models.Model):
    COMPONENT_TYPES = [
        # Basic Components
        ('Button', 'Button'),
        ('Input', 'Input'),
        ('Text', 'Text'),
        ('Table', 'Table'),
        
        # Form Components
        ('Form', 'Form'),
        ('Select', 'Select'),
        
        # Input Components
        ('CurrencyInput', 'Currency Input'),
        ('DatePicker', 'Date Picker'),
        ('FilePicker', 'File Picker'),
        ('PhoneInput', 'Phone Input'),
        ('RichTextEditor', 'Rich Text Editor'),
        
        # Button Components
        ('ButtonGroup', 'Button Group'),
        ('IconButton', 'Icon Button'),
        ('MenuButton', 'Menu Button'),
        
        # Display Components
        ('Chart', 'Chart'),
        ('Custom', 'Custom'),
        ('Iframe', 'Iframe'),
        ('List', 'List'),
        ('MapChart', 'Map Chart'),
        ('StatsBox', 'Stats Box'),
        
        # Layout Components
        ('Container', 'Container'),
        ('Divider', 'Divider'),
        ('JSONForm', 'JSON Form'),
        ('Modal', 'Modal'),
        ('Tabs', 'Tabs'),
        
        # Media Components
        ('Audio', 'Audio'),
        ('DocumentViewer', 'Document Viewer'),
        ('Image', 'Image'),
        ('Video', 'Video'),
        
        # Toggle Components
        ('Checkbox', 'Checkbox'),
        ('CheckboxGroup', 'Checkbox Group'),
        ('RadioGroup', 'Radio Group'),
        ('Switch', 'Switch'),
        ('SwitchGroup', 'Switch Group'),
        
        # Slider Components
        ('CategorySlider', 'Category Slider'),
        ('NumberSlider', 'Number Slider'),
        ('RangeSlider', 'Range Slider'),
        
        # Content Components
        ('Map', 'Map'),
        ('Progress', 'Progress'),
        ('Rating', 'Rating'),
    ]
    
    page = models.ForeignKey(Page, related_name='components', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=COMPONENT_TYPES)
    properties = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.type} on {self.page.name}"

# AI功能相关模型
class OptimizationHistory(models.Model):
    """PSO和NLP优化历史记录"""
    OPTIMIZATION_TYPES = [
        ('PSO', 'Particle Swarm Optimization'),
        ('NLP', 'Natural Language Processing'),
        ('LAYOUT', 'Layout Optimization'),
        ('COLOR', 'Color Scheme Optimization'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='optimizations')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='optimizations', null=True, blank=True)
    optimization_type = models.CharField(max_length=50, choices=OPTIMIZATION_TYPES)
    input_data = models.JSONField()  # 输入参数
    output_data = models.JSONField()  # 优化结果
    performance_metrics = models.JSONField(default=dict)  # 性能指标
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_optimizations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.optimization_type} - {self.project.name} ({self.created_at.strftime('%Y-%m-%d')})"


class ComponentTemplate(models.Model):
    """NLP生成的组件模板"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    nlp_keywords = models.JSONField(default=list)  # 关键词映射
    template_config = models.JSONField(default=dict)  # 组件配置模板
    usage_count = models.IntegerField(default=0)  # 使用次数
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='component_templates')
    is_public = models.BooleanField(default=False)  # 是否公开模板
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-usage_count', '-created_at']
    
    def __str__(self):
        return f"{self.name} (used {self.usage_count} times)"


class AICache(models.Model):
    """AI结果缓存"""
    CACHE_TYPES = [
        ('PSO_LAYOUT', 'PSO Layout Optimization'),
        ('NLP_COMPONENT', 'NLP Component Generation'),
        ('NLP_TRANSLATE', 'NLP Translation'),
        ('COLOR_OPTIMIZE', 'Color Optimization'),
    ]
    
    cache_type = models.CharField(max_length=50, choices=CACHE_TYPES)
    input_hash = models.CharField(max_length=64, unique=True)  # 输入数据的哈希值
    result_data = models.JSONField()  # 缓存的结果
    hit_count = models.IntegerField(default=0)  # 命中次数
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_used']
        indexes = [
            models.Index(fields=['cache_type', 'input_hash']),
        ]
    
    def __str__(self):
        return f"{self.cache_type} - {self.input_hash[:8]}... (hits: {self.hit_count})"


class NLPTrainingData(models.Model):
    """NLP训练数据"""
    description = models.TextField()  # 用户描述
    generated_component = models.JSONField()  # 生成的组件配置
    user_feedback = models.IntegerField(choices=[(1, '差'), (2, '一般'), (3, '好'), (4, '很好'), (5, '完美')], null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)  # 是否生成正确
    corrected_component = models.JSONField(null=True, blank=True)  # 用户修正后的组件
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nlp_training_data')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Training: {self.description[:50]}... (feedback: {self.user_feedback or 'none'})"
