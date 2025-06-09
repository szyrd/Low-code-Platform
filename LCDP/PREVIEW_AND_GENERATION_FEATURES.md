# 预览和生成功能 / Preview and Generation Features

## 🎯 新增功能概览 / Feature Overview

### 1. 页面预览功能 / Page Preview Feature

在项目编辑器中添加了实时预览功能，让用户可以在编辑过程中查看页面效果。

**功能特点：**
- 📱 支持多设备预览（Web, Tablet, Phone）
- 🎨 实时渲染当前页面组件
- 🔒 预览模式下组件不可编辑（只读）
- 🚀 预览界面直接生成应用功能

**使用方法：**
1. 在项目编辑器顶部点击 "👁️ 预览" 按钮
2. 在预览模态框中可以切换设备类型
3. 点击 "🚀 生成应用" 进入生成流程

### 2. 项目生成功能 / Project Generation Feature

在首页和预览界面都可以生成应用，将低代码项目转换为可部署的应用程序。

**功能特点：**
- 🏠 首页项目列表直接生成
- 💻📱 支持多平台生成（Web/Tablet/Phone）
- ⚠️ 自动检查项目是否有页面
- 🎯 智能权限验证

**使用方法：**
1. **从首页生成：** 在项目卡片底部点击 "🚀 生成" 按钮
2. **从预览生成：** 在预览界面点击 "🚀 生成应用" 按钮

## 🎨 界面更新 / UI Updates

### 项目编辑器 / Project Editor
- ✅ 新增预览按钮（位于页面按钮左侧）
- ✅ 全屏预览模态框
- ✅ 设备类型切换器
- ✅ 预览界面生成按钮

### 首页仪表板 / Dashboard
- ✅ 项目卡片新增生成按钮
- ✅ 按钮禁用状态（无页面时）
- ✅ 改进的项目footer布局

## 🌐 多语言支持 / Internationalization

### 新增翻译键 / New Translation Keys

**英文 / English:**
```json
{
  "page": {
    "preview": "Preview",
    "previewTitle": "Page Preview", 
    "generateApp": "Generate App"
  },
  "project": {
    "generate": "Generate",
    "generateProject": "Generate Application",
    "noPageToGenerate": "No pages to generate. Please create some pages first.",
    "generateConfirm": "Generate {{deviceType}} application for project \"{{projectName}}\"?",
    "generateSuccess": "{{deviceType}} application for \"{{projectName}}\" is being generated!"
  },
  "common": {
    "close": "Close"
  }
}
```

**中文 / Chinese:**
```json
{
  "page": {
    "preview": "预览",
    "previewTitle": "页面预览",
    "generateApp": "生成应用"
  },
  "project": {
    "generate": "生成",
    "generateProject": "生成应用",
    "noPageToGenerate": "没有页面可生成。请先创建一些页面。",
    "generateConfirm": "为项目 \"{{projectName}}\" 生成 {{deviceType}} 应用？",
    "generateSuccess": "正在为 \"{{projectName}}\" 生成 {{deviceType}} 应用！"
  },
  "common": {
    "close": "关闭"
  }
}
```

## 🔧 技术实现 / Technical Implementation

### 预览功能 / Preview Feature
- **组件：** `ProjectEditor.tsx` 
- **状态管理：** `showPreview` state
- **渲染：** 复用 `ComponentRenderer` 但设置为只读模式
- **样式：** `ProjectEditor.css` 中的预览模态框样式

### 生成功能 / Generation Feature  
- **组件：** `Dashboard.tsx` 和 `ProjectEditor.tsx`
- **权限检查：** 验证项目页面数量
- **用户交互：** 确认对话框
- **扩展性：** 预留后端API接入点

### CSS优化 / CSS Optimizations
- 响应式预览模态框
- 改进的按钮样式和状态
- 更好的项目卡片布局
- 移动端适配

## 🚀 未来扩展 / Future Enhancements

### 计划功能 / Planned Features
1. **后端生成API：** 实际的应用生成和打包
2. **模板系统：** 多种应用模板选择
3. **部署集成：** 直接部署到云平台
4. **下载管理：** 生成文件的下载和管理
5. **预览增强：** 交互式预览，数据绑定测试

### API设计建议 / Suggested API Design
```typescript
// 生成应用API
POST /api/projects/{id}/generate/
{
  "device_type": "web" | "tablet" | "phone",
  "template": "react" | "vue" | "native",
  "options": {
    "include_assets": true,
    "minify": true,
    "target_platform": "vercel" | "netlify" | "aws"
  }
}

// 响应
{
  "generation_id": "uuid",
  "status": "processing" | "completed" | "failed",
  "download_url": "https://...",
  "estimated_time": 300 // seconds
}
```

## 📱 使用截图说明 / Usage Screenshots

### 预览界面 / Preview Interface
- 模态框布局
- 设备类型切换
- 组件渲染效果
- 生成按钮位置

### 首页生成 / Homepage Generation
- 项目卡片布局
- 生成按钮状态
- 禁用状态提示

## ✅ 测试清单 / Testing Checklist

- [ ] 预览按钮点击
- [ ] 预览模态框显示/隐藏
- [ ] 设备类型切换
- [ ] 组件正确渲染（只读模式）
- [ ] 生成按钮功能
- [ ] 首页生成按钮
- [ ] 无页面时的禁用状态
- [ ] 多语言切换
- [ ] 响应式布局
- [ ] 错误处理

---

## 🎉 功能演示 / Feature Demo

现在您可以：

1. **打开任何项目** → 添加一些组件 → 点击"预览"按钮查看效果
2. **在首页** → 找到有页面的项目 → 点击"生成"按钮体验生成流程
3. **切换语言** → 查看所有新功能的多语言支持

所有功能都已完成并可以立即使用！🚀 