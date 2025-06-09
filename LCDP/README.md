# LCDP - 低代码开发平台 (Low-Code Development Platform)

LCDP是一个现代化的低代码开发平台，允许用户通过拖拽组件的方式快速构建应用程序界面。

## 🚀 功能特性

### 🏠 主页 (Dashboard)
- **项目管理**：查看、创建、编辑和删除项目
- **用户管理**：用户档案、设置和登出功能
- **现代化界面**：响应式设计，支持桌面和移动设备

### 🛠️ 项目编辑器 (Project Editor)
- **可视化拖拽**：超过40种预定义组件
- **实时编辑**：属性面板实时修改组件属性
- **页面管理**：在项目内创建、保存、加载和删除页面
- **多设备预览**：Web、平板和手机设备视图
- **响应式布局**：使用React Grid Layout实现

### 🔐 身份认证系统
- **JWT认证**：安全的用户认证机制
- **用户注册**：新用户注册功能
- **会话管理**：自动刷新token和登出

## 📁 项目结构

```
LCDP/
├── LCDPBackend/          # Django后端
│   ├── api/              # REST API应用
│   ├── users/            # 用户管理
│   └── lcdp_project/     # 项目设置
├── LCDPFront/            # React前端
│   └── lcdp-front/
│       ├── src/
│       │   ├── components/
│       │   │   ├── Dashboard.tsx        # 主页组件
│       │   │   ├── ProjectEditor.tsx    # 项目编辑器
│       │   │   ├── ComponentRenderer.tsx
│       │   │   ├── ComponentInspector.tsx
│       │   │   └── auth/                # 认证组件
│       │   ├── contexts/
│       │   │   └── AuthContext.tsx      # 认证上下文
│       │   ├── services/
│       │   │   └── api.ts               # API服务
│       │   └── types/
│       │       └── types.ts             # TypeScript类型
└── docker-compose.yml    # Docker容器编排
```

## 🛠️ 技术栈

### 后端
- **Django 4.x** - Web框架
- **Django REST Framework** - API框架
- **PostgreSQL** - 数据库
- **JWT认证** - 用户认证

### 前端
- **React 18** - UI库
- **TypeScript** - 类型安全
- **React Router** - 路由管理
- **React Grid Layout** - 拖拽布局
- **CSS3** - 现代化样式

## 🚀 快速开始

### 使用Docker (推荐)

1. **克隆项目**
```bash
git clone <repository-url>
cd LCDP
```

2. **启动服务**
```bash
docker-compose up -d
```

3. **访问应用**
- 前端: http://localhost:3000
- 后端API: http://localhost:8000/api/

### 手动安装

#### 后端设置
```bash
cd LCDPBackend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

#### 前端设置
```bash
cd LCDPFront/lcdp-front
npm install
npm start
```

## 📱 使用指南

### 1. 用户注册/登录
- 访问 http://localhost:3000
- 如果是新用户，点击"注册"创建账户
- 使用用户名和密码登录

### 2. 项目管理
- **创建项目**：在主页点击"新建项目"按钮
- **编辑项目**：点击项目卡片上的编辑按钮
- **删除项目**：点击项目卡片上的删除按钮

### 3. 页面编辑
- **进入编辑器**：点击"打开项目"按钮
- **添加组件**：从左侧组件面板拖拽组件到画布
- **编辑属性**：选中组件后在右侧属性面板修改
- **保存页面**：点击顶部"保存"按钮
- **页面管理**：点击"页面"按钮查看和切换页面

### 4. 组件类型
平台提供以下组件类别：
- **基础组件**：按钮、输入框、文本、表格
- **表单组件**：表单容器、选择框
- **输入组件**：货币输入、日期选择器、文件选择器等
- **显示组件**：图表、列表、统计框等
- **布局组件**：容器、分隔符、标签页等
- **媒体组件**：图片、视频、音频等
- **交互组件**：复选框、单选框、开关等

## 🔧 配置

### 环境变量
在 `LCDPFront/lcdp-front/.env` 中配置：
```
REACT_APP_API_URL=http://localhost:8000/api
```

### 数据库
默认使用PostgreSQL，配置在 `docker-compose.yml` 中。

## 🤝 贡献

欢迎提交问题和功能请求！

## 📄 许可证

MIT许可证 - 详见LICENSE文件

## 📞 支持

如有问题，请提交Issue或联系维护者。 