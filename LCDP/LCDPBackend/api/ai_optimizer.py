"""
AI优化器模块 - PSO (粒子群优化) 实现
用于LCDP平台的组件布局优化和智能排版
"""

import numpy as np
import random
import math
import json
import hashlib
from typing import List, Dict, Tuple, Optional
from django.utils import timezone
from .models import OptimizationHistory, AICache


class Particle:
    """粒子类 - PSO算法的基本单元"""
    
    def __init__(self, dimensions: int, bounds: List[Tuple[float, float]]):
        self.dimensions = dimensions
        self.bounds = bounds
        
        # 初始化位置和速度
        self.position = np.array([
            random.uniform(bound[0], bound[1]) 
            for bound in bounds
        ])
        self.velocity = np.array([
            random.uniform(-1, 1) for _ in range(dimensions)
        ])
        
        # 历史最佳位置和适应度
        self.best_position = self.position.copy()
        self.best_fitness = float('inf')
        self.current_fitness = float('inf')
    
    def update_velocity(self, global_best_position: np.ndarray, 
                       w: float = 0.5, c1: float = 1.5, c2: float = 1.5):
        """更新粒子速度"""
        r1, r2 = random.random(), random.random()
        
        # PSO速度更新公式
        cognitive = c1 * r1 * (self.best_position - self.position)
        social = c2 * r2 * (global_best_position - self.position)
        
        self.velocity = w * self.velocity + cognitive + social
        
        # 限制速度范围
        self.velocity = np.clip(self.velocity, -2, 2)
    
    def update_position(self):
        """更新粒子位置"""
        self.position += self.velocity
        
        # 确保位置在边界内
        for i, (min_val, max_val) in enumerate(self.bounds):
            if self.position[i] < min_val:
                self.position[i] = min_val
                self.velocity[i] *= -0.5  # 反弹
            elif self.position[i] > max_val:
                self.position[i] = max_val
                self.velocity[i] *= -0.5  # 反弹


class ComponentLayoutOptimizer:
    """组件布局PSO优化器"""
    
    def __init__(self, swarm_size: int = 30, max_iterations: int = 100):
        self.swarm_size = swarm_size
        self.max_iterations = max_iterations
        self.particles = []
        self.global_best_position = None
        self.global_best_fitness = float('inf')
        self.fitness_history = []
    
    def optimize_layout(self, components: List[Dict], constraints: Dict) -> Dict:
        """使用PSO优化组件布局"""
        
        # 检查缓存
        cache_key = self._generate_cache_key(components, constraints)
        cached_result = self._get_cached_result(cache_key, 'PSO_LAYOUT')
        if cached_result:
            return cached_result
        
        # 初始化粒子群
        self._initialize_particles(components, constraints)
        
        best_fitness_history = []
        
        # PSO主循环
        for iteration in range(self.max_iterations):
            # 评估每个粒子的适应度
            for particle in self.particles:
                fitness = self._evaluate_layout_fitness(
                    particle.position, components, constraints
                )
                particle.current_fitness = fitness
                
                # 更新个体最佳
                if fitness < particle.best_fitness:
                    particle.best_fitness = fitness
                    particle.best_position = particle.position.copy()
                
                # 更新全局最佳
                if fitness < self.global_best_fitness:
                    self.global_best_fitness = fitness
                    self.global_best_position = particle.position.copy()
            
            # 更新粒子速度和位置
            w = 0.9 - (0.5 * iteration / self.max_iterations)  # 递减惯性权重
            for particle in self.particles:
                particle.update_velocity(self.global_best_position, w)
                particle.update_position()
            
            best_fitness_history.append(self.global_best_fitness)
            
            # 早停条件
            if len(best_fitness_history) > 10:
                recent_improvement = best_fitness_history[-10] - best_fitness_history[-1]
                if recent_improvement < 0.01:  # 改进很小时提前停止
                    break
        
        # 生成优化结果
        optimized_positions = self._positions_to_layout(
            self.global_best_position, components, constraints
        )
        
        result = {
            'optimized_layout': optimized_positions,
            'fitness_score': self.global_best_fitness,
            'iterations': iteration + 1,
            'improvement': best_fitness_history[0] - self.global_best_fitness if best_fitness_history else 0,
            'fitness_history': best_fitness_history
        }
        
        # 缓存结果
        self._cache_result(cache_key, 'PSO_LAYOUT', result)
        
        return result
    
    def _initialize_particles(self, components: List[Dict], constraints: Dict):
        """初始化粒子群"""
        canvas_width = constraints.get('canvas_width', 1200)
        canvas_height = constraints.get('canvas_height', 800)
        
        # 每个组件需要2个维度 (x, y)
        dimensions = len(components) * 2
        
        # 设置边界
        bounds = []
        for comp in components:
            comp_width = comp.get('width', 100)
            comp_height = comp.get('height', 50)
            
            # x坐标边界
            bounds.append((0, max(0, canvas_width - comp_width)))
            # y坐标边界  
            bounds.append((0, max(0, canvas_height - comp_height)))
        
        # 创建粒子
        self.particles = [
            Particle(dimensions, bounds) 
            for _ in range(self.swarm_size)
        ]
    
    def _evaluate_layout_fitness(self, position: np.ndarray, 
                                components: List[Dict], constraints: Dict) -> float:
        """评估布局质量的适应度函数"""
        fitness = 0.0
        
        # 将位置向量转换为组件坐标
        positions = []
        for i in range(0, len(position), 2):
            positions.append({
                'x': position[i],
                'y': position[i + 1]
            })
        
        # 1. 重叠惩罚 (最重要)
        overlap_penalty = self._calculate_overlap_penalty(positions, components)
        fitness += overlap_penalty * 1000
        
        # 2. 边界违反惩罚
        boundary_penalty = self._calculate_boundary_penalty(
            positions, components, constraints
        )
        fitness += boundary_penalty * 500
        
        # 3. 对齐奖励 (降低fitness值)
        alignment_bonus = self._calculate_alignment_bonus(positions)
        fitness -= alignment_bonus * 10
        
        # 4. 间距均匀性奖励
        spacing_bonus = self._calculate_spacing_bonus(positions, components)
        fitness -= spacing_bonus * 5
        
        # 5. 视觉平衡奖励
        balance_bonus = self._calculate_visual_balance(positions, constraints)
        fitness -= balance_bonus * 20
        
        return max(0, fitness)  # 确保fitness非负
    
    def _calculate_overlap_penalty(self, positions: List[Dict], 
                                  components: List[Dict]) -> float:
        """计算组件重叠惩罚"""
        penalty = 0.0
        
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                comp1 = components[i]
                comp2 = components[j]
                pos1 = positions[i]
                pos2 = positions[j]
                
                # 计算重叠面积
                overlap_area = self._calculate_overlap_area(
                    pos1['x'], pos1['y'], comp1.get('width', 100), comp1.get('height', 50),
                    pos2['x'], pos2['y'], comp2.get('width', 100), comp2.get('height', 50)
                )
                
                penalty += overlap_area
        
        return penalty
    
    def _calculate_overlap_area(self, x1: float, y1: float, w1: float, h1: float,
                               x2: float, y2: float, w2: float, h2: float) -> float:
        """计算两个矩形的重叠面积"""
        # 计算重叠区域的边界
        left = max(x1, x2)
        right = min(x1 + w1, x2 + w2)
        top = max(y1, y2)
        bottom = min(y1 + h1, y2 + h2)
        
        # 如果有重叠
        if left < right and top < bottom:
            return (right - left) * (bottom - top)
        
        return 0.0
    
    def _calculate_boundary_penalty(self, positions: List[Dict], 
                                   components: List[Dict], constraints: Dict) -> float:
        """计算边界违反惩罚"""
        penalty = 0.0
        canvas_width = constraints.get('canvas_width', 1200)
        canvas_height = constraints.get('canvas_height', 800)
        
        for i, pos in enumerate(positions):
            comp = components[i]
            comp_width = comp.get('width', 100)
            comp_height = comp.get('height', 50)
            
            # 检查是否超出边界
            if pos['x'] < 0:
                penalty += abs(pos['x'])
            if pos['y'] < 0:
                penalty += abs(pos['y'])
            if pos['x'] + comp_width > canvas_width:
                penalty += pos['x'] + comp_width - canvas_width
            if pos['y'] + comp_height > canvas_height:
                penalty += pos['y'] + comp_height - canvas_height
        
        return penalty
    
    def _calculate_alignment_bonus(self, positions: List[Dict]) -> float:
        """计算对齐度奖励"""
        if len(positions) < 2:
            return 0.0
        
        bonus = 0.0
        threshold = 5  # 对齐阈值
        
        # 水平对齐检查
        y_coords = [pos['y'] for pos in positions]
        for i in range(len(y_coords)):
            for j in range(i + 1, len(y_coords)):
                if abs(y_coords[i] - y_coords[j]) <= threshold:
                    bonus += 1.0
        
        # 垂直对齐检查
        x_coords = [pos['x'] for pos in positions]
        for i in range(len(x_coords)):
            for j in range(i + 1, len(x_coords)):
                if abs(x_coords[i] - x_coords[j]) <= threshold:
                    bonus += 1.0
        
        return bonus
    
    def _calculate_spacing_bonus(self, positions: List[Dict], 
                                components: List[Dict]) -> float:
        """计算间距均匀性奖励"""
        if len(positions) < 2:
            return 0.0
        
        distances = []
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                pos1, pos2 = positions[i], positions[j]
                comp1, comp2 = components[i], components[j]
                
                # 计算组件边缘之间的最小距离
                dist = self._min_distance_between_components(
                    pos1, comp1, pos2, comp2
                )
                distances.append(dist)
        
        if not distances:
            return 0.0
        
        # 计算距离的方差，方差越小奖励越高
        mean_dist = np.mean(distances)
        variance = np.var(distances)
        
        # 距离越均匀，方差越小，奖励越高
        return max(0, 100 - variance)
    
    def _calculate_visual_balance(self, positions: List[Dict], 
                                 constraints: Dict) -> float:
        """计算视觉平衡奖励"""
        if not positions:
            return 0.0
        
        canvas_width = constraints.get('canvas_width', 1200)
        canvas_height = constraints.get('canvas_height', 800)
        
        # 计算重心
        center_x = np.mean([pos['x'] for pos in positions])
        center_y = np.mean([pos['y'] for pos in positions])
        
        # 理想重心位置（画布中心）
        ideal_center_x = canvas_width / 2
        ideal_center_y = canvas_height / 2
        
        # 计算偏移
        offset = np.sqrt(
            (center_x - ideal_center_x) ** 2 + 
            (center_y - ideal_center_y) ** 2
        )
        
        # 偏移越小，奖励越高
        max_offset = np.sqrt(canvas_width ** 2 + canvas_height ** 2) / 2
        balance_score = max(0, (max_offset - offset) / max_offset * 100)
        
        return balance_score
    
    def _min_distance_between_components(self, pos1: Dict, comp1: Dict, 
                                        pos2: Dict, comp2: Dict) -> float:
        """计算两个组件之间的最小距离"""
        x1, y1 = pos1['x'], pos1['y']
        w1, h1 = comp1.get('width', 100), comp1.get('height', 50)
        x2, y2 = pos2['x'], pos2['y']
        w2, h2 = comp2.get('width', 100), comp2.get('height', 50)
        
        # 计算矩形边缘之间的最小距离
        dx = max(0, max(x1 - (x2 + w2), x2 - (x1 + w1)))
        dy = max(0, max(y1 - (y2 + h2), y2 - (y1 + h1)))
        
        return np.sqrt(dx ** 2 + dy ** 2)
    
    def _positions_to_layout(self, position: np.ndarray, 
                            components: List[Dict], constraints: Dict) -> List[Dict]:
        """将PSO位置向量转换为布局配置"""
        layout = []
        
        for i, comp in enumerate(components):
            x = position[i * 2]
            y = position[i * 2 + 1]
            
            layout.append({
                'id': comp.get('id', f'comp_{i}'),
                'type': comp.get('type', 'Button'),
                'x': round(x, 2),
                'y': round(y, 2),
                'width': comp.get('width', 100),
                'height': comp.get('height', 50),
                'properties': comp.get('properties', {})
            })
        
        return layout
    
    def _generate_cache_key(self, components: List[Dict], constraints: Dict) -> str:
        """生成缓存键"""
        data = {
            'components': components,
            'constraints': constraints,
            'version': '1.0'
        }
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    def _get_cached_result(self, cache_key: str, cache_type: str) -> Optional[Dict]:
        """获取缓存结果"""
        try:
            cache_entry = AICache.objects.get(
                cache_type=cache_type,
                input_hash=cache_key
            )
            # 更新命中次数和最后使用时间
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
            # 缓存失败不影响主要功能
            print(f"Cache save failed: {e}")


class ColorSchemeOptimizer:
    """颜色方案PSO优化器"""
    
    def __init__(self, swarm_size: int = 20, max_iterations: int = 50):
        self.swarm_size = swarm_size
        self.max_iterations = max_iterations
    
    def optimize_color_scheme(self, base_color: str, 
                             requirements: Dict) -> Dict:
        """使用PSO优化颜色方案"""
        
        # 将基础颜色转换为HSL
        base_hsl = self._hex_to_hsl(base_color)
        
        # 初始化粒子群 (H, S, L for each color in palette)
        num_colors = requirements.get('num_colors', 5)
        dimensions = num_colors * 3  # HSL for each color
        
        # 设置边界
        bounds = []
        for _ in range(num_colors):
            bounds.extend([
                (0, 360),    # Hue
                (0, 100),    # Saturation  
                (0, 100)     # Lightness
            ])
        
        particles = [Particle(dimensions, bounds) for _ in range(self.swarm_size)]
        global_best_position = None
        global_best_fitness = float('inf')
        
        # PSO主循环
        for iteration in range(self.max_iterations):
            for particle in particles:
                fitness = self._evaluate_color_fitness(
                    particle.position, base_hsl, requirements
                )
                particle.current_fitness = fitness
                
                if fitness < particle.best_fitness:
                    particle.best_fitness = fitness
                    particle.best_position = particle.position.copy()
                
                if fitness < global_best_fitness:
                    global_best_fitness = fitness
                    global_best_position = particle.position.copy()
            
            # 更新粒子
            w = 0.9 - (0.5 * iteration / self.max_iterations)
            for particle in particles:
                particle.update_velocity(global_best_position, w)
                particle.update_position()
        
        # 生成最终配色方案
        color_scheme = self._position_to_colors(global_best_position, num_colors)
        
        return {
            'colors': color_scheme,
            'fitness_score': global_best_fitness,
            'base_color': base_color,
            'accessibility_score': self._calculate_accessibility_score(color_scheme)
        }
    
    def _hex_to_hsl(self, hex_color: str) -> Tuple[float, float, float]:
        """将十六进制颜色转换为HSL"""
        # 简化实现，实际项目中可以使用专业的颜色库
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return (0, 0, 50)  # 默认值
        
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0  
        b = int(hex_color[4:6], 16) / 255.0
        
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Lightness
        l = (max_val + min_val) / 2
        
        if diff == 0:
            h = s = 0
        else:
            # Saturation
            s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)
            
            # Hue
            if max_val == r:
                h = (g - b) / diff + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / diff + 2
            else:
                h = (r - g) / diff + 4
            h /= 6
        
        return (h * 360, s * 100, l * 100)
    
    def _evaluate_color_fitness(self, position: np.ndarray, 
                               base_hsl: Tuple[float, float, float], 
                               requirements: Dict) -> float:
        """评估配色方案质量"""
        fitness = 0.0
        num_colors = len(position) // 3
        
        colors_hsl = []
        for i in range(num_colors):
            h = position[i * 3]
            s = position[i * 3 + 1]
            l = position[i * 3 + 2]
            colors_hsl.append((h, s, l))
        
        # 1. 与基础颜色的和谐度
        harmony_penalty = self._calculate_harmony_penalty(colors_hsl, base_hsl)
        fitness += harmony_penalty * 100
        
        # 2. 对比度要求
        contrast_penalty = self._calculate_contrast_penalty(colors_hsl, requirements)
        fitness += contrast_penalty * 200
        
        # 3. 颜色多样性
        diversity_bonus = self._calculate_diversity_bonus(colors_hsl)
        fitness -= diversity_bonus * 50
        
        return max(0, fitness)
    
    def _calculate_harmony_penalty(self, colors: List[Tuple], 
                                  base_hsl: Tuple[float, float, float]) -> float:
        """计算颜色和谐度惩罚"""
        penalty = 0.0
        base_hue = base_hsl[0]
        
        for h, s, l in colors:
            # 计算色相差异
            hue_diff = min(abs(h - base_hue), 360 - abs(h - base_hue))
            
            # 理想的色相关系：互补色(180°)、三角色(120°)、邻近色(30°以内)
            ideal_diffs = [0, 30, 60, 120, 180]
            min_ideal_diff = min(abs(hue_diff - ideal) for ideal in ideal_diffs)
            
            penalty += min_ideal_diff / 30  # 归一化惩罚
        
        return penalty
    
    def _calculate_contrast_penalty(self, colors: List[Tuple], 
                                   requirements: Dict) -> float:
        """计算对比度惩罚"""
        penalty = 0.0
        min_contrast = requirements.get('min_contrast_ratio', 4.5)
        
        # 简化的对比度计算
        for i, (h1, s1, l1) in enumerate(colors):
            for j, (h2, s2, l2) in enumerate(colors[i+1:], i+1):
                lightness_diff = abs(l1 - l2)
                contrast_ratio = (max(l1, l2) + 5) / (min(l1, l2) + 5)
                
                if contrast_ratio < min_contrast:
                    penalty += (min_contrast - contrast_ratio)
        
        return penalty
    
    def _calculate_diversity_bonus(self, colors: List[Tuple]) -> float:
        """计算颜色多样性奖励"""
        if len(colors) < 2:
            return 0.0
        
        # 计算色相分布的标准差
        hues = [h for h, s, l in colors]
        hue_std = np.std(hues)
        
        # 计算饱和度分布
        saturations = [s for h, s, l in colors]
        sat_std = np.std(saturations)
        
        # 计算亮度分布
        lightnesses = [l for h, s, l in colors]
        light_std = np.std(lightnesses)
        
        # 多样性奖励
        diversity_score = (hue_std + sat_std + light_std) / 3
        return min(diversity_score, 100)  # 限制最大奖励
    
    def _position_to_colors(self, position: np.ndarray, num_colors: int) -> List[str]:
        """将PSO位置转换为颜色列表"""
        colors = []
        
        for i in range(num_colors):
            h = position[i * 3]
            s = position[i * 3 + 1] 
            l = position[i * 3 + 2]
            
            # 将HSL转换为十六进制
            hex_color = self._hsl_to_hex(h, s, l)
            colors.append(hex_color)
        
        return colors
    
    def _hsl_to_hex(self, h: float, s: float, l: float) -> str:
        """将HSL转换为十六进制颜色"""
        # 简化实现
        h = h / 360.0
        s = s / 100.0
        l = l / 100.0
        
        def hue_to_rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q - p) * 6 * t
            if t < 1/2: return q
            if t < 2/3: return p + (q - p) * (2/3 - t) * 6
            return p
        
        if s == 0:
            r = g = b = l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)
        
        # 转换为十六进制
        r_hex = format(int(r * 255), '02x')
        g_hex = format(int(g * 255), '02x')
        b_hex = format(int(b * 255), '02x')
        
        return f"#{r_hex}{g_hex}{b_hex}"
    
    def _calculate_accessibility_score(self, colors: List[str]) -> float:
        """计算配色方案的可访问性评分"""
        # 简化的可访问性评分
        score = 100.0
        
        for color in colors:
            hsl = self._hex_to_hsl(color)
            lightness = hsl[2]
            
            # 避免过暗或过亮的颜色
            if lightness < 20 or lightness > 90:
                score -= 10
            
            # 理想亮度范围
            if 30 <= lightness <= 70:
                score += 5
        
        return max(0, min(100, score)) 