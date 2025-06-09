# 🚀 Django REST Framework API 完整文档

## 📋 概览

您的 LCDP (Low-Code Development Platform) 已经配置了完整的 Django REST Framework API，提供强大的后端服务支持。

## 🌐 API 服务器信息

- **基础 URL**: `http://localhost:8000/api/`
- **认证方式**: JWT Token 认证
- **API 版本**: v1.0.0
- **文档格式**: DRF 可浏览 API

## 🔐 认证端点

### 用户注册
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_secure_password"
}
```

**响应示例**：
```json
{
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
  },
  "message": "User created successfully"
}
```

### 用户登录 (获取 Token)
```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**响应示例**：
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 刷新 Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

### 用户资料
```http
GET /api/auth/profile/
Authorization: Bearer your_access_token
```

## 📁 项目管理 API

### 获取所有项目
```http
GET /api/projects/
Authorization: Bearer your_access_token
```

### 创建新项目
```http
POST /api/projects/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "name": "我的新项目",
  "description": "项目描述",
  "device_type": "web"
}
```

### 获取特定项目
```http
GET /api/projects/{project_id}/
Authorization: Bearer your_access_token
```

### 更新项目
```http
PUT /api/projects/{project_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "name": "更新的项目名称",
  "description": "更新的描述",
  "device_type": "tablet"
}
```

### 删除项目
```http
DELETE /api/projects/{project_id}/
Authorization: Bearer your_access_token
```

## 📄 页面管理 API

### 获取所有页面
```http
GET /api/pages/
Authorization: Bearer your_access_token
```

### 创建新页面
```http
POST /api/pages/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "name": "主页",
  "layout_config": {
    "components": [],
    "layout": "grid"
  },
  "project": 1
}
```

### 获取特定页面
```http
GET /api/pages/{page_id}/
Authorization: Bearer your_access_token
```

### 更新页面
```http
PUT /api/pages/{page_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "name": "更新的页面名称",
  "layout_config": {
    "components": [
      {
        "id": "comp1",
        "type": "Button",
        "props": {"label": "点击我"}
      }
    ]
  }
}
```

### 删除页面
```http
DELETE /api/pages/{page_id}/
Authorization: Bearer your_access_token
```

## 🧩 组件管理 API

### 获取页面中的所有组件
```http
GET /api/components/?page={page_id}
Authorization: Bearer your_access_token
```

### 创建新组件
```http
POST /api/components/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "page": 1,
  "type": "Button",
  "properties": {
    "label": "我的按钮",
    "color": "#4F46E5",
    "variant": "filled",
    "x": 100,
    "y": 100,
    "w": 120,
    "h": 40
  }
}
```

### 获取特定组件
```http
GET /api/components/{component_id}/
Authorization: Bearer your_access_token
```

### 更新组件
```http
PUT /api/components/{component_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "type": "Button",
  "properties": {
    "label": "更新的按钮",
    "color": "#EF4444",
    "customCSS": "border-radius: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
  }
}
```

### 删除组件
```http
DELETE /api/components/{component_id}/
Authorization: Bearer your_access_token
```

## 📊 支持的组件类型

### 基础组件
- `Button` - 按钮组件
- `Input` - 输入框组件
- `Text` - 文本组件
- `Table` - 表格组件
- `Select` - 选择框组件

### 表单组件
- `Form` - 表单容器
- `RichTextEditor` - 富文本编辑器
- `MenuButton` - 菜单按钮
- `Checkbox` - 复选框
- `RadioGroup` - 单选按钮组
- `CheckboxGroup` - 复选框组

### 显示组件
- `Chart` - 图表组件
- `StatsBox` - 统计框
- `List` - 列表组件
- `Image` - 图像组件
- `Video` - 视频组件
- `Audio` - 音频组件

### 布局组件
- `Container` - 容器组件
- `Modal` - 模态框
- `Tabs` - 标签页
- `Divider` - 分割线

### 交互组件
- `NumberSlider` - 数值滑块
- `CategorySlider` - 分类滑块
- `RangeSlider` - 范围滑块
- `Rating` - 评分组件

## 💻 JavaScript 客户端示例

```javascript
// API 客户端类
class LCDPApiClient {
  constructor(baseURL = 'http://localhost:8000/api') {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('access_token');
  }

  // 设置认证头
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  // 用户登录
  async login(username, password) {
    const response = await fetch(`${this.baseURL}/auth/token/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    if (data.access) {
      this.token = data.access;
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
    }
    return data;
  }

  // 获取项目列表
  async getProjects() {
    const response = await fetch(`${this.baseURL}/projects/`, {
      headers: this.getHeaders()
    });
    return response.json();
  }

  // 创建新项目
  async createProject(projectData) {
    const response = await fetch(`${this.baseURL}/projects/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(projectData)
    });
    return response.json();
  }

  // 获取页面列表
  async getPages() {
    const response = await fetch(`${this.baseURL}/pages/`, {
      headers: this.getHeaders()
    });
    return response.json();
  }

  // 保存页面布局
  async savePage(pageId, layoutConfig) {
    const response = await fetch(`${this.baseURL}/pages/${pageId}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify({ layout_config: layoutConfig })
    });
    return response.json();
  }

  // 创建组件
  async createComponent(componentData) {
    const response = await fetch(`${this.baseURL}/components/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(componentData)
    });
    return response.json();
  }

  // 更新组件
  async updateComponent(componentId, componentData) {
    const response = await fetch(`${this.baseURL}/components/${componentId}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(componentData)
    });
    return response.json();
  }
}

// 使用示例
const api = new LCDPApiClient();

// 登录
await api.login('your_username', 'your_password');

// 创建项目
const project = await api.createProject({
  name: '我的 Web 应用',
  description: '使用 LCDP 构建的应用',
  device_type: 'web'
});

// 创建页面
const page = await api.createPage({
  name: '主页',
  project: project.id,
  layout_config: { components: [] }
});

// 添加按钮组件
const button = await api.createComponent({
  page: page.id,
  type: 'Button',
  properties: {
    label: '点击我',
    color: '#4F46E5',
    x: 100,
    y: 100,
    w: 120,
    h: 40,
    customCSS: 'border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'
  }
});
```

## 🔒 安全配置

### JWT Token 配置
- **Access Token 有效期**: 60 分钟
- **Refresh Token 有效期**: 7 天
- **Token 自动轮换**: 启用
- **算法**: HS256

### CORS 配置
- **允许的域名**: `http://localhost:3000` (前端应用)
- **支持的方法**: GET, POST, PUT, DELETE, PATCH, OPTIONS

### 权限设置
- **默认权限**: 需要认证
- **用户隔离**: 每个用户只能访问自己创建的项目和页面

## 📈 性能优化

### 分页配置
- **默认页面大小**: 10 条记录
- **分页类**: PageNumberPagination

### 查询优化
- 使用 select_related 和 prefetch_related 优化数据库查询
- 适当的数据库索引

## 🧪 API 测试

### 使用 curl 测试
```bash
# 获取 Token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# 使用 Token 访问 API
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/projects/
```

### 使用 Postman 测试
1. 创建新的 Collection
2. 设置 Base URL: `http://localhost:8000/api`
3. 在 Authorization 中设置 Bearer Token
4. 测试各个端点

## 🔧 高级功能

### 批量操作
- 批量创建组件
- 批量更新组件属性
- 批量删除组件

### 搜索和过滤
- 按项目筛选页面
- 按类型筛选组件
- 全文搜索项目和页面

### 版本控制
- 页面版本历史
- 布局快照保存
- 回滚功能

## 📚 API 文档访问

访问 `http://localhost:8000/api/` 可以看到 DRF 的可浏览 API 界面，提供：
- 交互式 API 文档
- 在线测试功能
- 详细的字段说明
- 示例请求和响应

---

## 🎯 总结

您的 LCDP 平台现在拥有：
✅ **完整的 RESTful API**
✅ **JWT 认证系统**
✅ **用户权限管理**
✅ **CORS 跨域支持**
✅ **PostgreSQL 数据库**
✅ **Docker 容器化部署**

**API 状态**: 🟢 正常运行
**访问地址**: http://localhost:8000/api/
**文档地址**: http://localhost:8000/api/ (DRF 可浏览 API) 