# LCDP 低代码开发平台 - 完整项目文档
# LCDP Low-Code Development Platform - Comprehensive Documentation

## 📋 项目概述 | Project Overview

**LCDP (Low-Code Development Platform)** 是一个基于现代技术栈构建的企业级低代码开发平台，支持通过可视化拖拽界面快速创建应用程序。该平台集成了人工智能技术，包括粒子群优化(PSO)算法和自然语言处理(NLP)功能，为用户提供智能化的开发体验。

**LCDP** is an enterprise-grade low-code development platform built with modern technology stack, enabling rapid application development through visual drag-and-drop interface. The platform integrates AI technologies including Particle Swarm Optimization (PSO) and Natural Language Processing (NLP) for intelligent development experience.

---

## 🏗️ 系统架构 | System Architecture

### 技术栈 | Technology Stack

#### Frontend (前端)
- **React 19.1.0** + **TypeScript 5.3.3** - 现代化前端框架
- **React Router DOM 6.30.1** - 单页应用路由
- **React Grid Layout 1.5.1** - 拖拽网格布局
- **React DnD 16.0.1** - 拖拽功能实现
- **Framer Motion 11.0.0** - 动画效果
- **Axios 1.8.4** - HTTP客户端 (JWT支持)
- **i18next** - 国际化支持 (中英文)
- **Zustand 4.4.7** - 状态管理

#### Backend (后端)
- **Django 5.0+** - Web框架
- **Django REST Framework 3.14+** - API框架
- **PostgreSQL 15** - 主数据库
- **JWT认证** - 用户认证系统
- **Redis** (可选) - 缓存系统

#### AI & ML Libraries (AI/机器学习库)
- **NumPy 1.21+** - 数值计算
- **SciPy 1.7+** - 科学计算
- **scikit-learn 1.0+** - 机器学习
- **PyTorch 1.12+** - 深度学习
- **Transformers 4.21+** - NLP模型
- **SpaCy 3.4+** - NLP工具包
- **Jieba 0.42+** - 中文分词

#### Infrastructure (基础设施)
- **Docker + Docker Compose** - 容器化部署
- **Nginx** (生产环境) - 反向代理
- **PostgreSQL** - 数据持久化

---

## 📁 项目结构 | Project Structure

```
LCDP/
├── 📄 README.md                          # 项目说明文档
├── 📄 docker-compose.yml                 # Docker编排配置
├── 📄 PROJECT_INDEX.md                   # 项目索引文档
├── 📄 AI_INTEGRATION_COMPLETE.md         # AI集成文档
├── 📄 GRADUATION_THESIS_PRESENTATION.md  # 毕业论文演示
├── 📄 PSOandNLP.md                      # PSO和NLP技术文档
│
├── 📁 LCDPBackend/                       # Django后端服务
│   ├── 📄 manage.py                      # Django管理脚本
│   ├── 📄 requirements.txt               # Python依赖包
│   ├── 📄 Dockerfile                     # 后端Docker配置
│   ├── 🗄️ db.sqlite3                    # 开发数据库
│   │
│   ├── 📁 lcdp_backend/                  # Django项目配置
│   │   ├── 📄 settings.py               # Django设置
│   │   ├── 📄 urls.py                   # 主URL路由
│   │   ├── 📄 wsgi.py                   # WSGI配置
│   │   └── 📄 asgi.py                   # ASGI配置
│   │
│   └── 📁 api/                          # REST API应用
│       ├── 📄 models.py                 # 数据模型 (7.4KB, 204行)
│       ├── 📄 urls.py                   # API路由配置
│       ├── 📄 admin.py                  # 管理后台
│       ├── 🤖 ai_optimizer.py           # PSO优化算法 (23KB, 664行)
│       ├── 🤖 nlp_generator.py          # NLP处理引擎 (31KB, 795行)
│       │
│       ├── 📁 views/                    # API视图
│       │   ├── 📄 auth_views.py         # 认证视图
│       │   ├── 📄 project_views.py      # 项目管理视图
│       │   ├── 📄 page_views.py         # 页面管理视图
│       │   └── 📄 component_views.py    # 组件管理视图
│       │
│       ├── 📁 serializers/              # 数据序列化器
│       │   ├── 📄 auth_serializers.py   # 认证序列化器
│       │   ├── 📄 project_serializers.py # 项目序列化器
│       │   ├── 📄 page_serializers.py   # 页面序列化器
│       │   └── 📄 component_serializers.py # 组件序列化器
│       │
│       ├── 📁 auth/                     # 认证模块
│       └── 📁 migrations/               # 数据库迁移文件
│
├── 📁 LCDPFront/                        # React前端应用
│   └── 📁 lcdp-front/                   # 主前端项目
│       ├── 📄 package.json              # Node.js依赖配置
│       ├── 📄 tsconfig.json             # TypeScript配置
│       ├── 📄 Dockerfile                # 前端Docker配置
│       │
│       ├── 📁 public/                   # 静态资源
│       │   ├── 📄 index.html            # HTML模板
│       │   └── 🎨 favicon.ico           # 网站图标
│       │
│       └── 📁 src/                      # 源代码目录
│           ├── 📄 App.tsx               # 主应用组件 (3.9KB, 162行)
│           ├── 📄 index.tsx             # 应用入口
│           ├── 🎨 App.css               # 全局样式
│           ├── 🎨 index.css             # 基础样式
│           │
│           ├── 📁 components/           # React组件库
│           │   ├── ⭐ Dashboard.tsx      # 项目仪表板 (18KB, 484行)
│           │   ├── 🎨 Dashboard.css     # 仪表板样式 (14KB, 809行)
│           │   ├── ⭐ ProjectEditor.tsx  # 项目编辑器 (52KB, 1467行)
│           │   ├── 🎨 ProjectEditor.css # 编辑器样式 (20KB, 1126行)
│           │   ├── 🔧 ComponentInspector.tsx # 属性检查器 (53KB, 1548行)
│           │   ├── 🎨 ComponentInspector.css # 检查器样式 (7.6KB, 394行)
│           │   ├── 🎭 ComponentRenderer.tsx # 组件渲染器 (8.6KB, 317行)
│           │   ├── 🧩 DraggableComponents.tsx # 拖拽组件库 (20KB, 813行)
│           │   ├── 📑 PageManager.tsx   # 页面管理器 (3.7KB, 138行)
│           │   ├── 🔗 AdditionalComponents.tsx # 额外组件 (37KB, 1379行)
│           │   ├── 🌐 LanguageSwitcher.tsx # 语言切换器 (2.8KB, 97行)
│           │   ├── 💾 DataSourceManager.tsx # 数据源管理 (19KB, 522行)
│           │   ├── 🔍 QueryBuilder.tsx  # 查询构建器 (16KB, 483行)
│           │   ├── 📝 CodeEditor.tsx    # 代码编辑器 (9.6KB, 313行)
│           │   ├── ⚠️ ErrorBoundary.tsx # 错误边界 (3.7KB, 135行)
│           │   │
│           │   ├── 📁 ai/               # AI功能组件
│           │   │   ├── 🤖 PSO.tsx       # PSO优化组件
│           │   │   ├── 🎨 PSO.css       # PSO样式
│           │   │   ├── 🧠 NLPGenerator.tsx # NLP生成组件
│           │   │   └── 🎨 NLPGenerator.css # NLP样式
│           │   │
│           │   ├── 📁 auth/             # 认证组件
│           │   │   ├── 📄 AuthPage.tsx  # 认证页面
│           │   │   ├── 🔐 LoginForm.tsx # 登录表单
│           │   │   ├── 📝 RegisterForm.tsx # 注册表单
│           │   │   └── 🎨 AuthForms.css # 认证样式
│           │   │
│           │   ├── 📁 editor/           # 编辑器相关组件
│           │   ├── 📁 navigation/       # 导航组件
│           │   ├── 📁 pages/            # 页面组件
│           │   ├── 📁 layout/           # 布局组件
│           │   └── 📁 FlowDesigner/     # 流程设计器
│           │
│           ├── 📁 contexts/             # React上下文
│           │   └── 🔐 AuthContext.tsx   # 认证上下文 (3.5KB, 126行)
│           │
│           ├── 📁 services/             # 服务层
│           │   ├── 🌐 api.ts            # API通信服务 (6.2KB, 251行)
│           │   └── 📑 pageService.ts    # 页面服务 (2.2KB, 95行)
│           │
│           ├── 📁 hooks/                # React Hooks
│           ├── 📁 types/                # TypeScript类型定义
│           ├── 📁 store/                # 状态管理
│           ├── 📁 i18n/                 # 国际化配置
│           └── 📁 locales/              # 语言包
│
└── 📁 src/                             # 早期版本源码 (已废弃)
    ├── 📄 App.tsx                      # 遗留应用组件
    └── 📁 components/                  # 遗留组件

---

## 🎯 核心功能 | Core Features

### 1. 用户认证系统 | Authentication System
- **JWT令牌认证** - JSON Web Token based authentication
- **用户注册/登录** - User registration and login
- **权限管理** - Role-based access control
- **会话管理** - Session management with auto-refresh
- **路由保护** - Protected routes for authenticated users

### 2. 项目管理仪表板 | Project Management Dashboard
- **项目CRUD操作** - Create, Read, Update, Delete projects
- **设备类型选择** - Device type selection (Web/Tablet/Phone)
- **现代化卡片布局** - Modern card-based layout
- **用户资料管理** - User profile management
- **响应式设计** - Responsive design for all screen sizes

### 3. 可视化项目编辑器 | Visual Project Editor
- **拖拽界面** - Drag-and-drop interface
- **实时预览** - Real-time component preview
- **分层结构** - Hierarchical structure: Project → Page → Components
- **设备适配** - Device-specific layouts
- **三栏布局** - Three-column layout (Components | Canvas | Properties)

### 4. 丰富的组件库 | Rich Component Library

#### 🧩 组件分类 | Component Categories (40+ Components)

**基础组件 | Basic Components**
- Button - 按钮组件
- Input - 输入框组件
- Text - 文本组件
- Table - 表格组件

**表单组件 | Form Components**
- Form - 表单容器
- Select - 选择器

**输入组件 | Input Components**
- CurrencyInput - 货币输入
- DatePicker - 日期选择器
- FilePicker - 文件选择器
- PhoneInput - 电话输入
- RichTextEditor - 富文本编辑器

**按钮组件 | Button Components**
- ButtonGroup - 按钮组
- IconButton - 图标按钮
- MenuButton - 菜单按钮

**展示组件 | Display Components**
- Chart - 图表组件
- Custom - 自定义组件
- Iframe - 内嵌框架
- List - 列表组件
- MapChart - 地图图表
- StatsBox - 统计框

**布局组件 | Layout Components**
- Container - 容器
- Divider - 分割线
- JSONForm - JSON表单
- Modal - 模态框
- Tabs - 标签页

**媒体组件 | Media Components**
- Audio - 音频播放器
- DocumentViewer - 文档查看器
- Image - 图片组件
- Video - 视频播放器

**开关组件 | Toggle Components**
- Checkbox - 复选框
- CheckboxGroup - 复选框组
- RadioGroup - 单选框组
- Switch - 开关
- SwitchGroup - 开关组

**滑块组件 | Slider Components**
- CategorySlider - 分类滑块
- NumberSlider - 数字滑块
- RangeSlider - 范围滑块

**内容组件 | Content Components**
- Map - 地图
- Progress - 进度条
- Rating - 评分组件

### 5. 🤖 AI 智能功能 | AI Intelligence Features

#### PSO 粒子群优化 | Particle Swarm Optimization
- **智能布局优化** - Automatic layout optimization
- **避免组件重叠** - Prevent component overlapping
- **视觉美学优化** - Visual aesthetics enhancement
- **多目标优化** - Multi-objective optimization
- **实时进度显示** - Real-time progress indication
- **结果缓存** - Result caching for performance

**PSO算法特性 | PSO Algorithm Features:**
- 粒子群规模: 30个粒子 | Swarm size: 30 particles
- 最大迭代次数: 100次 | Max iterations: 100
- 适应度函数考虑因素 | Fitness function considers:
  - 重叠惩罚 | Overlap penalty
  - 边界违规惩罚 | Boundary violation penalty
  - 对齐奖励 | Alignment bonus
  - 间距均匀性 | Spacing uniformity
  - 视觉平衡 | Visual balance

#### NLP 自然语言处理 | Natural Language Processing
- **中文智能识别** - Chinese language intelligent recognition
- **组件智能生成** - Intelligent component generation
- **智能推荐引擎** - Smart recommendation engine
- **多语言翻译** - Multi-language translation
- **用户反馈学习** - User feedback learning

**NLP功能特性 | NLP Features:**
- 支持中文分词 (Jieba) | Chinese word segmentation support
- 40+组件类型识别 | 40+ component type recognition
- 智能属性提取 | Intelligent property extraction
- 上下文理解 | Context understanding
- 模板缓存系统 | Template caching system

### 6. 页面管理系统 | Page Management System
- **多页面支持** - Multiple pages per project
- **页面切换** - Page navigation
- **页面模板** - Page templates
- **布局配置保存** - Layout configuration persistence

### 7. 属性检查器 | Property Inspector
- **Material Design风格** - Material Design style
- **实时属性编辑** - Real-time property editing
- **颜色选择器** - Color picker
- **响应式属性面板** - Responsive property panel
- **批量编辑** - Batch editing support

### 8. 国际化支持 | Internationalization (i18n)
- **中英文切换** - Chinese/English language switching
- **动态语言加载** - Dynamic language loading
- **组件文本翻译** - Component text translation
- **界面本地化** - Interface localization 

---

## 🗄️ 数据库设计 | Database Design

### 核心数据模型 | Core Data Models

#### User (用户模型)
```python
# Django内置用户模型扩展
User {
    id: Integer (Primary Key)
    username: String (Unique, 最大150字符)
    email: String
    password: String (Hashed)
    first_name: String
    last_name: String
    is_active: Boolean
    date_joined: DateTime
}
```

#### Project (项目模型)
```python
Project {
    id: Integer (Primary Key)
    name: String (最大255字符)
    description: Text (可选)
    device_type: String (web/tablet/phone)
    owner: ForeignKey(User)
    created_at: DateTime
    updated_at: DateTime
    
    # 约束条件
    unique_together: ['name', 'owner']
}
```

#### Page (页面模型)
```python
Page {
    id: Integer (Primary Key)
    name: String (最大255字符)
    layout_config: JSONField (布局配置)
    project: ForeignKey(Project)
    owner: ForeignKey(User)
    created_at: DateTime
    updated_at: DateTime
}
```

#### Component (组件模型)
```python
Component {
    id: Integer (Primary Key)
    page: ForeignKey(Page)
    type: String (组件类型，最大50字符)
    properties: JSONField (组件属性)
    created_at: DateTime
    updated_at: DateTime
}
```

### AI相关数据模型 | AI-Related Data Models

#### OptimizationHistory (优化历史)
```python
OptimizationHistory {
    id: Integer (Primary Key)
    project: ForeignKey(Project)
    page: ForeignKey(Page, optional)
    optimization_type: String (PSO/NLP/LAYOUT/COLOR)
    input_data: JSONField
    output_data: JSONField
    performance_metrics: JSONField
    user: ForeignKey(User)
    created_at: DateTime
}
```

#### ComponentTemplate (组件模板)
```python
ComponentTemplate {
    id: Integer (Primary Key)
    name: String (最大100字符)
    description: Text
    nlp_keywords: JSONField (关键词数组)
    template_config: JSONField (模板配置)
    usage_count: Integer (使用次数)
    created_by: ForeignKey(User)
    is_public: Boolean (是否公开)
    created_at: DateTime
    updated_at: DateTime
}
```

#### AICache (AI缓存)
```python
AICache {
    id: Integer (Primary Key)
    cache_type: String (缓存类型)
    input_hash: String (输入哈希值, unique)
    result_data: JSONField (缓存结果)
    hit_count: Integer (命中次数)
    created_at: DateTime
    last_used: DateTime
}
```

#### NLPTrainingData (NLP训练数据)
```python
NLPTrainingData {
    id: Integer (Primary Key)
    description: Text (用户描述)
    generated_component: JSONField (生成的组件)
    user_feedback: Integer (1-5星评分)
    is_correct: Boolean (是否正确)
    corrected_component: JSONField (用户修正)
    created_by: ForeignKey(User)
    created_at: DateTime
}
```

---

## 🌐 API接口文档 | API Documentation

### 基础URL | Base URL
- **开发环境**: `http://localhost:8000/api/`
- **生产环境**: `https://yourdomain.com/api/`

### 认证方式 | Authentication
所有需要认证的API都使用JWT Bearer Token：
```http
Authorization: Bearer {jwt_access_token}
```

### 认证接口 | Authentication APIs

#### 用户注册 | User Registration
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
}

Response: 201 Created
{
    "user": {
        "id": 1,
        "username": "string",
        "email": "string"
    },
    "message": "User created successfully"
}
```

#### 用户登录 | User Login
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}

Response: 200 OK
{
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
}
```

#### 令牌刷新 | Token Refresh
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "jwt_refresh_token"
}

Response: 200 OK
{
    "access": "new_jwt_access_token"
}
```

### 项目管理接口 | Project Management APIs

#### 获取项目列表 | Get Projects
```http
GET /api/projects/
Authorization: Bearer {jwt_token}

Response: 200 OK
[
    {
        "id": 1,
        "name": "项目名称",
        "description": "项目描述",
        "device_type": "web",
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
    }
]
```

#### 创建项目 | Create Project
```http
POST /api/projects/
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
    "name": "新项目",
    "description": "项目描述",
    "device_type": "web"
}

Response: 201 Created
{
    "id": 1,
    "name": "新项目",
    "description": "项目描述",
    "device_type": "web",
    "owner": 1,
    "created_at": "2024-01-01T12:00:00Z"
}
```

#### 更新项目 | Update Project
```http
PUT /api/projects/{id}/
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
    "name": "更新的项目名",
    "description": "更新的描述"
}
```

#### 删除项目 | Delete Project
```http
DELETE /api/projects/{id}/
Authorization: Bearer {jwt_token}

Response: 204 No Content
```

### AI功能接口 | AI Feature APIs

#### PSO布局优化 | PSO Layout Optimization
```http
POST /api/ai/pso/optimize-layout/
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
    "components": [
        {
            "id": "comp1",
            "type": "Button",
            "width": 100,
            "height": 40,
            "x": 10,
            "y": 10
        }
    ],
    "constraints": {
        "canvas_width": 1200,
        "canvas_height": 800
    }
}

Response: 200 OK
{
    "optimized_layout": [
        {
            "id": "comp1",
            "x": 50,
            "y": 100
        }
    ],
    "fitness_score": 15.5,
    "iterations": 45,
    "improvement": 25.3
}
```

#### NLP组件生成 | NLP Component Generation
```http
POST /api/ai/nlp/generate-component/
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
    "description": "创建一个红色的提交按钮，大小中等"
}

Response: 200 OK
{
    "component": {
        "type": "Button",
        "properties": {
            "text": "提交",
            "color": "red",
            "size": "medium"
        }
    },
    "confidence": 0.85,
    "suggestions": ["修改文本", "调整颜色"]
}
```

---

## 🚀 部署指南 | Deployment Guide

### Docker 容器化部署 | Docker Containerized Deployment

#### 前置要求 | Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 至少 4GB 内存
- 至少 10GB 可用磁盘空间

#### 快速部署 | Quick Deployment
```bash
# 1. 克隆项目
git clone <repository-url>
cd LCDP

# 2. 启动所有服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f
```

#### 服务访问 | Service Access
- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000/api/
- **数据库**: localhost:5432 (仅本地访问)

#### 环境配置 | Environment Configuration
创建 `.env` 文件：
```bash
# 数据库配置
POSTGRES_DB=lcdp_db
POSTGRES_USER=lcdp_user
POSTGRES_PASSWORD=your_secure_password

# Django配置
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# 前端配置
REACT_APP_API_URL=http://localhost:8000/api
```

### 手动部署 | Manual Deployment

#### 后端部署 | Backend Deployment
```bash
# 1. 进入后端目录
cd LCDPBackend

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 数据库迁移
python manage.py migrate

# 5. 创建超级用户
python manage.py createsuperuser

# 6. 启动服务
python manage.py runserver 0.0.0.0:8000
```

#### 前端部署 | Frontend Deployment
```bash
# 1. 进入前端目录
cd LCDPFront/lcdp-front

# 2. 安装依赖
npm install

# 3. 开发模式启动
npm start

# 4. 生产构建
npm run build

# 5. 部署构建文件 (例如使用 nginx)
sudo cp -r build/* /var/www/html/
```

#### 生产环境配置 | Production Configuration

**Nginx 配置示例**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**PostgreSQL 生产配置**:
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
```

---

## 📱 使用指南 | Usage Guide

### 快速开始 | Quick Start

#### 1. 用户注册和登录 | User Registration and Login
1. 访问应用首页: `http://localhost:3000`
2. 点击"注册"创建新账户
3. 填写用户信息：用户名、邮箱、密码
4. 注册成功后自动跳转到登录页面
5. 使用注册的账户信息登录

#### 2. 项目管理 | Project Management
1. **创建项目**:
   - 在主页点击"+ 新建项目"按钮
   - 填写项目名称和描述
   - 选择设备类型 (Web/Tablet/Phone)
   - 点击"创建"按钮

2. **编辑项目**:
   - 在项目卡片上点击"编辑"按钮
   - 修改项目信息
   - 保存更改

3. **删除项目**:
   - 在项目卡片上点击"删除"按钮
   - 确认删除操作

#### 3. 页面编辑 | Page Editing

##### 进入编辑器 | Enter Editor
1. 在项目卡片上点击"打开项目"按钮
2. 进入可视化项目编辑器
3. 界面分为三个区域：
   - **左侧**: 组件库面板
   - **中间**: 画布区域
   - **右侧**: 属性检查器

##### 添加组件 | Add Components
1. 从左侧组件库选择所需组件
2. 拖拽到中间画布区域
3. 组件自动生成唯一ID
4. 在右侧属性面板编辑组件属性

##### 编辑组件属性 | Edit Component Properties
1. 点击画布中的组件进行选择
2. 在右侧属性面板中编辑:
   - **基础属性**: 文本、颜色、尺寸
   - **布局属性**: 位置、大小、边距
   - **样式属性**: 字体、边框、阴影
   - **交互属性**: 事件、动画

##### 页面管理 | Page Management
1. 点击顶部"页面"按钮
2. 查看当前项目的所有页面
3. 创建新页面:
   - 点击"+ 新页面"
   - 输入页面名称
   - 选择页面模板 (可选)
4. 切换页面:
   - 在页面列表中点击目标页面
5. 删除页面:
   - 点击页面旁的删除按钮

##### 保存和加载 | Save and Load
1. **保存页面**:
   - 点击顶部"💾 保存"按钮
   - 页面布局自动保存到数据库
2. **加载页面**:
   - 页面切换时自动加载
   - 支持历史版本恢复

#### 4. AI 智能功能使用 | AI Features Usage

##### PSO 布局优化 | PSO Layout Optimization
1. 在编辑器中添加多个组件
2. 点击"🤖 AI助手"按钮
3. 切换到"布局优化"标签页
4. 选择要优化的组件 (默认选择全部)
5. 点击"开始优化"按钮
6. 观察实时优化进度
7. 优化完成后应用结果

##### NLP 组件生成 | NLP Component Generation
1. 点击"🤖 AI助手"按钮
2. 切换到"智能生成"标签页
3. 在输入框中用自然语言描述组件:
   - 例如："创建一个红色的提交按钮"
   - 例如："添加一个用户名输入框"
   - 例如："生成一个销售数据图表"
4. 点击"生成组件"按钮
5. 查看生成结果和置信度
6. 应用生成的组件到画布

### 高级功能 | Advanced Features

#### 设备适配 | Device Adaptation
1. **Web模式**: 全屏显示，适合桌面应用
2. **Tablet模式**: 768×1024px，适合平板应用
3. **Phone模式**: 375×667px，适合手机应用

#### 国际化 | Internationalization
1. 点击右上角语言切换器
2. 选择中文或英文
3. 界面自动切换语言
4. 组件文本支持翻译

#### 导入导出 | Import/Export
1. **导出项目**:
   - 点击"导出"按钮
   - 下载JSON格式的项目文件
2. **导入项目**:
   - 点击"导入"按钮
   - 选择JSON项目文件
   - 确认导入

#### 预览和发布 | Preview and Publish
1. **预览模式**:
   - 点击"👁️ 预览"按钮
   - 查看实际运行效果
2. **代码生成**:
   - 点击"代码"按钮
   - 查看生成的React代码
3. **发布项目**:
   - 配置发布设置
   - 生成生产版本

---

## 🔧 开发指南 | Development Guide

### 开发环境设置 | Development Environment Setup

#### 前端开发 | Frontend Development
```bash
cd LCDPFront/lcdp-front
npm install
npm start
```

#### 后端开发 | Backend Development
```bash
cd LCDPBackend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

### 代码规范 | Code Standards

#### TypeScript/React 规范
- 使用 TypeScript 严格模式
- 函数组件 + Hooks
- ESLint + Prettier 代码格式化
- 组件和 Hook 命名使用 PascalCase
- 文件名使用 PascalCase (.tsx) 或 camelCase (.ts)

#### Python/Django 规范  
- 遵循 PEP 8 代码规范
- 使用类型提示 (Type Hints)
- 文档字符串格式 (Docstrings)
- 函数和变量命名使用 snake_case
- 类命名使用 PascalCase

### 测试指南 | Testing Guide

#### 前端测试
```bash
# 运行测试
npm test

# 测试覆盖率
npm run test:coverage

# E2E 测试
npm run test:e2e
```

#### 后端测试
```bash
# 运行测试
python manage.py test

# 测试覆盖率
coverage run --source='.' manage.py test
coverage report
```

---

## 🛠️ 故障排除 | Troubleshooting

### 常见问题 | Common Issues

#### 1. Docker 容器启动失败
**问题**: 容器无法启动或端口冲突
**解决方案**:
```bash
# 检查端口占用
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# 停止冲突服务
docker-compose down
sudo service nginx stop

# 重新启动
docker-compose up -d
```

#### 2. 数据库连接错误
**问题**: Django 无法连接到 PostgreSQL
**解决方案**:
```bash
# 检查数据库容器状态
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 重置数据库
docker-compose down -v
docker-compose up -d
```

#### 3. 前端 API 调用失败
**问题**: 前端无法访问后端 API
**解决方案**:
1. 检查 CORS 设置
2. 验证 API URL 配置
3. 检查 JWT 令牌是否有效

#### 4. AI 功能报错
**问题**: PSO 或 NLP 功能异常
**解决方案**:
1. 检查 Python AI 库安装
2. 验证内存使用情况
3. 查看后端错误日志

### 性能优化 | Performance Optimization

#### 前端优化
- 启用 React 生产构建
- 使用代码分割 (Code Splitting)
- 优化组件渲染
- 压缩静态资源

#### 后端优化
- 启用数据库查询优化
- 使用 Redis 缓存
- 配置 Gunicorn + Nginx
- 启用 gzip 压缩

---

## 📊 项目统计 | Project Statistics

### 代码统计 | Code Statistics
- **总文件数**: 200+ 文件
- **前端代码**: ~150,000 行 TypeScript/JavaScript
- **后端代码**: ~50,000 行 Python
- **样式文件**: ~20,000 行 CSS
- **文档**: ~30,000 行 Markdown

### 功能统计 | Feature Statistics
- **组件数量**: 40+ 个组件
- **API接口**: 50+ 个端点
- **页面数量**: 10+ 个页面
- **AI算法**: 2 个 (PSO + NLP)
- **语言支持**: 2 种 (中文/英文)

---

## 🤝 贡献指南 | Contributing Guide

### 如何贡献 | How to Contribute
1. Fork 项目仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 报告问题 | Report Issues
- 使用 GitHub Issues 报告 Bug
- 提供详细的复现步骤
- 包含系统环境信息
- 附上相关日志和截图

---

## 📄 许可证 | License

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

---

## 📞 联系方式 | Contact

- **项目维护者**: LCDP Team
- **邮箱**: support@lcdp.com
- **官网**: https://lcdp.com
- **文档**: https://docs.lcdp.com

---

## 🙏 致谢 | Acknowledgments

感谢以下开源项目和技术支持:
- React.js 社区
- Django 社区
- PyTorch 团队
- All Contributors

---

*最后更新时间: 2024年1月*
*Last Updated: January 2024* 