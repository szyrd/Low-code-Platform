# LCDP (Low-Code Development Platform) 项目索引

## 🏗️ 项目概述
这是一个现代化的低代码开发平台，支持用户通过可视化界面创建和管理多个项目，每个项目可以包含多个页面，通过拖拽组件来构建用户界面。项目采用前后端分离的微服务架构，支持设备类型固定（Web/Tablet/Phone）、用户权限管理、JWT认证和PostgreSQL数据库。

## 🆕 最新版本特性 (v1.0.0)
- ✅ **企业级Dashboard**: 项目管理、用户profile、现代化UI设计
- ✅ **分层架构**: 用户 → 项目 → 页面 → 组件的层次结构
- ✅ **设备类型固定**: 项目创建时选择并固定设备类型(Web/Tablet/Phone)
- ✅ **React Router**: 完整的单页应用路由系统
- ✅ **美观Properties面板**: Material Design风格的属性编辑器
- ✅ **40+组件库**: 支持10个分类的丰富组件
- ✅ **Docker一键部署**: 完整的容器化解决方案

## 📁 项目结构

```
LCDP/
├── docker-compose.yml           # Docker Compose配置文件 (1.3KB, 57行)
├── README.md                    # 项目主说明文档 (4.3KB, 153行)
├── PROJECT_INDEX.md             # 项目索引文档 (本文件)
├── src/                         # 早期版本源码 (已废弃)
├── LCDPFront/                   # 前端项目主目录
│   └── lcdp-front/             # React应用
│       ├── Dockerfile           # 前端Docker配置
│       ├── package.json         # 前端依赖配置 (v0.1.0)
│       ├── tsconfig.json        # TypeScript配置
│       ├── public/              # 静态资源
│       └── src/                 # 前端源码 (26个TS/TSX文件)
│           ├── App.tsx          # 主应用路由配置 (2.0KB, 93行)
│           ├── index.tsx        # 应用入口
│           ├── components/      # 组件库
│           │   ├── Dashboard.tsx        # 项目管理面板 (13KB, 363行) ⭐新增
│           │   ├── Dashboard.css        # Dashboard样式 (11KB, 678行) ⭐新增
│           │   ├── ProjectEditor.tsx    # 项目编辑器 (23KB, 678行) ⭐重构
│           │   ├── ProjectEditor.css    # 编辑器样式 (8.5KB, 538行) ⭐新增
│           │   ├── ComponentInspector.tsx # 属性检查器 (12KB, 392行)
│           │   ├── ComponentInspector.css # 属性面板样式 (7.6KB, 394行) ⭐新增
│           │   ├── ComponentRenderer.tsx  # 组件渲染器 (4.5KB, 152行)
│           │   ├── DraggableComponents.tsx # 拖拽组件库 (19KB, 808行)
│           │   ├── PageManager.tsx      # 页面管理器 (3.7KB, 138行)
│           │   ├── auth/               # 认证组件 ⭐新增
│           │   │   ├── AuthPage.tsx    # 认证页面 (707B, 28行)
│           │   │   ├── LoginForm.tsx   # 登录表单 (2.8KB, 113行)
│           │   │   ├── RegisterForm.tsx # 注册表单 (4.3KB, 171行)
│           │   │   └── AuthForms.css   # 认证样式 (3.8KB, 230行)
│           │   ├── editor/             # 编辑器组件
│           │   ├── navigation/         # 导航组件
│           │   ├── pages/              # 页面组件
│           │   └── layout/             # 布局组件
│           ├── contexts/        # React上下文 ⭐新增
│           │   └── AuthContext.tsx     # 认证上下文 (3.5KB, 126行)
│           ├── services/        # 服务层
│           │   ├── api.ts              # API通信服务 (6.2KB, 251行)
│           │   └── pageService.ts      # 页面服务 (2.2KB, 95行)
│           ├── hooks/           # React Hooks
│           └── types/           # TypeScript类型定义
└── LCDPBackend/                 # 后端项目目录 (20个Python文件)
    ├── Dockerfile               # 后端Docker配置
    ├── manage.py                # Django管理脚本
    ├── requirements.txt         # Python依赖 (6个包)
    ├── lcdp_backend/           # Django项目配置
    │   ├── settings.py         # Django设置 (支持PostgreSQL)
    │   ├── urls.py             # URL路由配置
    │   ├── wsgi.py             # WSGI配置
    │   └── asgi.py             # ASGI配置
    └── api/                    # API应用
        ├── models.py           # 数据模型 (2.2KB, 66行) ⭐支持Project模型
        ├── urls.py             # API路由 (1.0KB, 28行)
        ├── admin.py            # 管理后台
        ├── auth/               # 认证模块
        │   ├── __init__.py     # 认证模块初始化
        │   ├── serializers.py  # 认证序列化器
        │   ├── views.py        # 认证视图
        │   └── urls.py         # 认证路由
        ├── views/              # 视图目录
        │   ├── __init__.py     # 视图模块初始化
        │   ├── auth_views.py   # 认证视图 (1.2KB, 37行)
        │   ├── project_views.py # 项目视图 (851B, 21行) ⭐新增
        │   ├── page_views.py   # 页面视图 (4.8KB, 129行)
        │   └── component_views.py # 组件视图 (5.5KB, 156行)
        ├── serializers/        # 序列化器目录
        │   ├── __init__.py     # 序列化器模块初始化
        │   ├── auth_serializers.py # 认证序列化器 (1.3KB, 43行)
        │   ├── project_serializers.py # 项目序列化器 (1.9KB, 53行) ⭐新增
        │   ├── page_serializers.py # 页面序列化器 (5.0KB, 118行)
        │   └── component_serializers.py # 组件序列化器 (3.2KB, 101行)
        └── migrations/         # 数据库迁移文件
            └── 0006_project_device_type.py # 设备类型迁移 ⭐新增
```

## 🛠️ 技术栈

### 前端技术栈
- **核心框架**: React 19.1.0 + TypeScript 4.9.5
- **路由**: React Router DOM 6.30.1 ⭐新增
- **UI组件**: 
  - react-grid-layout 1.5.1: 拖拽网格布局
  - react-dnd 16.0.1: 拖拽功能
  - react-icons 5.5.0: 图标库
- **HTTP客户端**: Axios 1.8.4 (JWT拦截器支持)
- **工具库**: 
  - uuid 11.1.0: 生成唯一ID
  - TypeScript类型支持全覆盖
- **测试**: Jest + React Testing Library
- **样式**: 现代化CSS3 + Material Design风格

### 后端技术栈
- **框架**: Django 5.0+ 
- **API**: Django REST Framework 3.14+
- **认证**: djangorestframework-simplejwt 5.3+ (JWT)
- **数据库**: PostgreSQL 15 (生产) / SQLite (开发)
- **跨域**: django-cors-headers 4.3+
- **环境配置**: python-decouple 3.8+
- **数据库驱动**: psycopg2-binary 2.9+

### 基础设施
- **容器化**: Docker + Docker Compose
- **数据库**: PostgreSQL 15
- **网络**: 自定义Docker网络 (lcdp_network)
- **存储**: Docker卷持久化 (postgres_data)

## 🎯 核心功能

### 1. 用户认证系统 (JWT) ⭐升级
- **组件**: `AuthPage.tsx`, `LoginForm.tsx`, `RegisterForm.tsx`
- **上下文**: `AuthContext.tsx` - 全局认证状态管理
- **端点**: 
  - POST `/api/auth/register/` - 用户注册
  - POST `/api/auth/token/` - 获取JWT令牌
  - POST `/api/auth/token/refresh/` - 刷新令牌
- **特性**: 
  - 自动Token刷新
  - 路由保护
  - 用户状态持久化

### 2. 项目管理Dashboard ⭐全新
- **组件**: `Dashboard.tsx` (13KB, 363行)
- **样式**: `Dashboard.css` (11KB, 678行)
- **功能**: 
  - 项目CRUD操作 (创建、编辑、删除)
  - 设备类型选择 (Web/Tablet/Phone)
  - 现代化卡片布局
  - 用户Profile下拉菜单
  - 响应式设计
- **特色UI**:
  - 渐变背景和Material Design
  - 动画过渡效果
  - 设备类型选择器卡片

### 3. 项目编辑器 ⭐重大重构
- **组件**: `ProjectEditor.tsx` (23KB, 678行)
- **样式**: `ProjectEditor.css` (8.5KB, 538行)
- **功能**: 
  - 分层结构: 项目 → 页面 → 组件
  - 设备类型固定显示
  - 页面管理面板
  - 40+组件库，10个分类
  - 三栏布局 (组件库 | 画布 | 属性面板)
- **设备支持**:
  - **Web**: 100% × 100% (全屏)
  - **Tablet**: 768px × 1024px (居中)
  - **Phone**: 375px × 667px (居中)

### 4. 组件库系统 ⭐扩展
- **文件**: `DraggableComponents.tsx` (19KB, 808行)
- **分类**: 10个组件分类
  - Basic: Button, Input, Text, Table
  - Form: Form, Select
  - Inputs: CurrencyInput, DatePicker, FilePicker, PhoneInput, RichTextEditor
  - Buttons: ButtonGroup, IconButton, MenuButton
  - Display: Chart, Custom, Iframe, List, MapChart, StatsBox
  - Layout: Container, Divider, JSONForm, Modal, Tabs
  - Media: Audio, DocumentViewer, Image, Video
  - Toggles: Checkbox, CheckboxGroup, RadioGroup, Switch, SwitchGroup
  - Sliders: CategorySlider, NumberSlider, RangeSlider
  - Content: Map, Progress, Rating
- **总计**: 40+组件类型

### 5. 属性编辑器 ⭐美化升级
- **文件**: `ComponentInspector.tsx` (12KB, 392行)
- **样式**: `ComponentInspector.css` (7.6KB, 394行)
- **功能**: 
  - Material Design风格界面
  - 卡片式属性分组
  - 颜色选择器增强
  - 动画和过渡效果
  - 渐变头部设计

### 6. 路由系统 ⭐新增
- **配置**: `App.tsx` (2.0KB, 93行)
- **路由**:
  - `/auth` - 认证页面
  - `/` - Dashboard首页
  - `/project/:projectId` - 项目编辑器
- **特性**:
  - 路由保护 (ProtectedRoute)
  - 自动重定向
  - 加载状态显示

## 📊 数据模型

### 前端类型定义 (`src/types/types.ts`)
```typescript
// 项目接口 ⭐新增
interface Project {
  id: number;
  name: string;
  description: string;
  device_type: 'web' | 'tablet' | 'phone'; // ⭐设备类型固定
  pages_count: number;
  created_at: string;
  updated_at: string;
}

// 页面接口
interface Page {
  id: number;
  name: string;
  project: number; // ⭐关联项目
  layout_config: any;
  created_at: string;
  updated_at: string;
}

// 组件数据接口 ⭐扩展支持40+类型
interface ComponentData {
  id: string;
  type: 'Button' | 'Input' | 'Text' | 'Table' | 'Chart' | /* ...40+类型... */;
  x: number; y: number; w: number; h: number;
  props: ComponentProps;
}
```

### 后端数据模型 (`LCDPBackend/api/models.py`)
```python
# 项目模型 ⭐新增
class Project(models.Model):
    DEVICE_CHOICES = [
        ('web', 'Web'),
        ('tablet', 'Tablet'),
        ('phone', 'Phone'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_CHOICES, default='web') # ⭐新增
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 页面模型 ⭐关联项目
class Page(models.Model):
    name = models.CharField(max_length=255)
    layout_config = models.JSONField(default=dict)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pages') # ⭐新增
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🔌 API接口

### 认证API (`/api/auth/`)
- **POST** `/token/` - 获取JWT令牌
- **POST** `/token/refresh/` - 刷新JWT令牌
- **POST** `/register/` - 用户注册
- **POST** `/logout/` - 用户登出

### 项目API (`/api/projects/`) ⭐新增
- **GET** `/` - 获取用户项目列表
- **POST** `/` - 创建新项目 (包含设备类型)
- **GET** `/{id}/` - 获取特定项目详情
- **PUT/PATCH** `/{id}/` - 更新项目
- **DELETE** `/{id}/` - 删除项目

### 页面API (`/api/pages/`)
- **GET** `/` - 获取页面列表
- **POST** `/` - 创建新页面 (关联项目)
- **GET** `/{id}/` - 获取特定页面详情
- **PUT/PATCH** `/{id}/` - 更新页面
- **DELETE** `/{id}/` - 删除页面
- **GET** `/by_project/?project_id={id}` - 按项目过滤页面

### 组件API (`/api/components/`)
- **GET** `/` - 获取组件列表
- **POST** `/` - 创建新组件
- **GET** `/{id}/` - 获取特定组件
- **PUT/PATCH** `/{id}/` - 更新组件
- **DELETE** `/{id}/` - 删除组件

## 🚀 开发环境

### Docker Compose启动 (推荐)
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启前端服务 (应用更改)
docker-compose restart frontend

# 停止服务
docker-compose down
```

### 服务端点
- **前端**: http://localhost:3000 (React开发服务器)
- **后端**: http://localhost:8000 (Django API)
- **数据库**: PostgreSQL (端口5432)

### 手动启动

#### 前端启动
```bash
cd LCDPFront/lcdp-front
npm install
npm start  # 开发服务器
```

#### 后端启动
```bash
cd LCDPBackend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🎨 UI/UX设计

### 设计系统
- **主题**: Material Design风格
- **色彩**: 渐变背景 (#667eea → #764ba2)
- **组件**: 现代化卡片布局
- **动画**: CSS3过渡效果
- **响应式**: 支持桌面端和移动端

### 关键样式文件
- `Dashboard.css` (11KB) - Dashboard界面样式
- `ProjectEditor.css` (8.5KB) - 编辑器布局样式
- `ComponentInspector.css` (7.6KB) - 属性面板样式
- `AuthForms.css` (3.8KB) - 认证表单样式

## 🔐 安全特性

1. **JWT认证**: 基于令牌的无状态认证
2. **路由保护**: React Router保护路由
3. **用户隔离**: 每个用户只能访问自己的项目/页面
4. **权限控制**: Django REST权限类
5. **输入验证**: 前后端双重验证
6. **CORS配置**: 跨域请求安全控制

## 📈 项目特点

1. **企业级架构**: 分层设计，用户→项目→页面→组件
2. **设备类型固定**: 项目级别设备类型固定，避免混乱
3. **现代化UI**: Material Design + 渐变主题
4. **容器化部署**: Docker一键部署，生产就绪
5. **类型安全**: 全面TypeScript支持
6. **可视化编辑**: 拖拽操作 + 实时预览
7. **组件丰富**: 40+组件，10个分类
8. **响应式设计**: 支持多种设备尺寸

## 🔍 关键文件分析

| 文件 | 大小 | 行数 | 功能描述 | 状态 |
|------|------|------|----------|------|
| `ProjectEditor.tsx` | 23KB | 678行 | 项目编辑器主组件 | ⭐重构 |
| `Dashboard.tsx` | 13KB | 363行 | 项目管理Dashboard | ⭐新增 |
| `DraggableComponents.tsx` | 19KB | 808行 | 40+组件库定义 | ⭐扩展 |
| `ComponentInspector.tsx` | 12KB | 392行 | 属性编辑器 | ⭐美化 |
| `Dashboard.css` | 11KB | 678行 | Dashboard样式 | ⭐新增 |
| `ProjectEditor.css` | 8.5KB | 538行 | 编辑器样式 | ⭐新增 |
| `ComponentInspector.css` | 7.6KB | 394行 | 属性面板样式 | ⭐新增 |
| `api.ts` | 6.2KB | 251行 | API通信服务 | ⭐升级 |
| `page_views.py` | 4.8KB | 129行 | 页面API视图 | ⭐更新 |
| `component_views.py` | 5.5KB | 156行 | 组件API视图 | ⭐更新 |
| `page_serializers.py` | 5.0KB | 118行 | 页面序列化器 | ⭐更新 |
| `AuthContext.tsx` | 3.5KB | 126行 | 认证上下文 | ⭐新增 |
| `docker-compose.yml` | 1.3KB | 57行 | Docker编排配置 | ⭐优化 |

## 🌐 环境变量

### Docker Compose环境变量
```bash
# 数据库配置
POSTGRES_DB=lcdp_db
POSTGRES_USER=lcdp_user
POSTGRES_PASSWORD=lcdp_password

# 后端配置
DEBUG=True
SECRET_KEY=your-secret-key-here

# 前端配置
REACT_APP_API_URL=http://localhost:8000/api
```

## 📊 项目统计

- **总源文件**: ~6181个文件
- **前端源文件**: 26个 TypeScript/TSX文件
- **后端源文件**: 20个 Python文件 (核心API)
- **总代码量**: ~100KB+ (核心业务逻辑)
- **组件数量**: 40+个可拖拽组件
- **API端点**: 15+个RESTful端点
- **Docker服务**: 3个服务 (前端、后端、数据库)

---

**最后更新时间**: 2024年12月  
**项目版本**: v1.0.0  
**架构升级**: Dashboard + ProjectEditor + 设备类型固定 + React Router + Material Design  
**开发状态**: 生产就绪，完整的企业级低代码平台 