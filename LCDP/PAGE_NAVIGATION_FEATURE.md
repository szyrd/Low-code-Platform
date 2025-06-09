# 页面导航功能 / Page Navigation Feature

## 🎯 功能概览 / Feature Overview

为LCDP平台添加了强大的页面间导航功能，允许用户在组件中配置页面跳转，实现真正的多页面应用体验。

### ✨ 主要特性 / Key Features

- 🔗 **组件级导航配置** - 为Button等组件添加页面跳转功能
- 🎯 **可视化配置界面** - 在属性面板中直观配置目标页面
- 🚀 **实时导航预览** - 在预览模式下测试页面跳转
- 🌐 **多语言支持** - 完整的中英文界面支持
- ⚡ **智能触发机制** - 支持多种导航触发方式

## 🔧 技术实现 / Technical Implementation

### 1. 类型系统扩展

更新了`ComponentProps`接口，添加导航相关属性：

```typescript
export interface ComponentProps {
  // 现有属性...
  
  // 页面导航属性
  navigateTo?: number; // 目标页面ID
  navigationAction?: 'click' | 'submit' | 'change'; // 导航触发方式
}
```

### 2. 导航上下文 / Navigation Context

创建了`NavigationContext`来管理页面导航状态：

```typescript
interface NavigationContextType {
  currentPageId: number | null;
  pages: Page[];
  navigateToPage: (pageId: number) => void;
  isPreviewMode: boolean;
}
```

### 3. 组件渲染器增强

`ComponentRenderer`现在支持：
- 接收导航回调函数
- 为组件添加导航事件处理
- 区分编辑模式和预览模式

### 4. 属性面板集成

`ComponentInspector`新增：
- 页面选择下拉菜单
- 导航触发方式配置
- 可视化导航状态指示

## 📖 使用指南 / Usage Guide

### 🚀 快速开始

1. **创建多个页面**
   ```
   项目编辑器 → 点击"新建"按钮 → 创建多个页面
   ```

2. **添加Button组件**
   ```
   组件面板 → 拖拽Button到画布
   ```

3. **配置页面导航**
   ```
   选中Button → 属性面板 → "页面导航"区域 → 选择目标页面
   ```

4. **测试导航功能**
   ```
   点击"预览"按钮 → 在预览模式下点击配置的Button
   ```

### 🎨 配置选项详解

#### 导航到页面 / Navigate to Page
- **无导航** - 按钮不执行页面跳转
- **页面列表** - 显示项目中所有可用页面

#### 导航触发方式 / Navigation Trigger
- **点击时 (On Click)** - 用户点击组件时触发导航
- **提交时 (On Submit)** - 表单提交时触发（未来扩展）
- **值改变时 (On Change)** - 值变化时触发（未来扩展）

### 🎯 支持导航的组件

当前支持页面导航的组件：

#### ✅ Button 按钮
- 点击导航到指定页面
- 显示导航箭头指示符 (→)
- 支持所有按钮样式和尺寸

#### 🔄 计划支持的组件
- **Form** - 表单提交后导航
- **IconButton** - 图标按钮导航
- **MenuButton** - 菜单项导航
- **Text** - 文本链接导航

## 🌟 用户体验特性

### 可视化反馈
- 配置导航的按钮显示箭头符号 (→)
- 鼠标悬停显示导航提示信息
- 属性面板显示导航状态说明

### 智能验证
- 自动检测可用页面列表
- 防止导航到不存在的页面
- 编辑模式下禁用导航功能

### 预览模式增强
- 在预览中完整测试导航功能
- 实时页面切换体验
- 保持设备类型和视图状态

## 🌍 国际化支持 / Internationalization

完整的中英文支持，包括：

### 英文界面
```json
{
  "page": {
    "navigation": "Page Navigation",
    "navigateTo": "Navigate to Page",
    "navigationTrigger": "Navigation Trigger",
    "noNavigation": "No navigation",
    "onClick": "On Click",
    "navigationInfo": "This component will navigate to the selected page when triggered"
  }
}
```

### 中文界面
```json
{
  "page": {
    "navigation": "页面导航",
    "navigateTo": "导航到页面",
    "navigationTrigger": "导航触发方式",
    "noNavigation": "无导航",
    "onClick": "点击时",
    "navigationInfo": "该组件将在触发时导航到选定的页面"
  }
}
```

## 💡 最佳实践 / Best Practices

### 1. 页面结构设计
```
首页 (Home)
├── 产品列表 (Product List)
│   └── 产品详情 (Product Detail)
├── 用户中心 (User Center)
│   ├── 个人资料 (Profile)
│   └── 设置 (Settings)
└── 关于我们 (About)
```

### 2. 导航按钮设计
- 使用清晰的按钮标签
- 选择合适的按钮样式和颜色
- 考虑用户的导航路径

### 3. 预览测试流程
1. 配置所有导航链接
2. 在预览模式下测试每个导航路径
3. 验证页面间的逻辑关系
4. 确保用户体验的连贯性

## 🔄 未来扩展计划

### 短期计划
- [ ] 支持更多组件类型的导航
- [ ] 添加导航历史和返回功能
- [ ] 支持外部链接导航

### 中期计划
- [ ] 条件导航（基于用户输入）
- [ ] 导航动画和过渡效果
- [ ] 导航路径可视化

### 长期计划
- [ ] 深度链接支持
- [ ] SEO友好的URL结构
- [ ] 浏览器历史管理

## 🎬 功能演示

### 演示场景：电商应用

1. **创建页面结构**
   - 商品列表页
   - 商品详情页
   - 购物车页
   - 结算页

2. **配置导航链接**
   - 商品卡片 → 商品详情
   - 加入购物车 → 购物车页
   - 立即购买 → 结算页
   - 返回首页 → 商品列表

3. **测试用户流程**
   - 浏览商品 → 查看详情 → 加入购物车 → 结算购买

## 🚨 注意事项 / Important Notes

### 编辑模式 vs 预览模式
- **编辑模式**：导航功能被禁用，专注于页面设计
- **预览模式**：导航功能完全激活，模拟真实用户体验

### 页面保存提醒
- 导航前会检查当前页面是否有未保存的更改
- 提示用户保存当前页面以免丢失数据

### 性能考虑
- 页面切换时会重新渲染组件
- 大型页面建议优化组件性能
- 避免过度复杂的页面结构

---

## 🎉 立即体验

现在您可以：

1. **打开任何项目** → 创建多个页面
2. **添加Button组件** → 配置页面导航
3. **预览模式测试** → 体验页面跳转效果
4. **构建完整应用** → 创建多页面用户流程

页面导航功能已完全集成到LCDP平台中，开始构建您的多页面应用吧！🚀 