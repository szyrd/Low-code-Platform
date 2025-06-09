#!/usr/bin/env python3
"""
LCDP Django REST Framework API 测试脚本
测试所有主要的 API 端点功能
"""

import requests
import json
import sys
from time import sleep
import time

# API 配置
BASE_URL = "http://localhost:8000/api"
TEST_USER = {
    "username": "testuser123",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
}

class LCDPAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name, success, message=""):
        """记录测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} {test_name}"
        if message:
            result += f": {message}"
        print(result)
        self.test_results.append((test_name, success, message))
    
    def test_api_connection(self):
        """测试 API 基础连接"""
        try:
            response = requests.get(f"{self.base_url.replace('/api', '')}/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("API基础连接", True, f"API版本: {data.get('version', '未知')}")
                return True
            else:
                self.log_test("API基础连接", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API基础连接", False, f"连接错误: {str(e)}")
            return False
    
    def test_user_registration(self):
        """测试用户注册"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/register/",
                json=TEST_USER,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                self.log_test("用户注册", True, f"用户 {TEST_USER['username']} 注册成功")
                return True
            elif response.status_code == 400:
                # 用户可能已存在
                error_data = response.json()
                if "already exists" in str(error_data).lower() or "username" in str(error_data):
                    self.log_test("用户注册", True, "用户已存在 (正常)")
                    return True
                else:
                    self.log_test("用户注册", False, f"注册失败: {error_data}")
                    return False
            else:
                self.log_test("用户注册", False, f"状态码: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("用户注册", False, f"错误: {str(e)}")
            return False
    
    def test_user_login(self):
        """测试用户登录"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/token/",
                json={
                    "username": TEST_USER["username"],
                    "password": TEST_USER["password"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access" in data and "refresh" in data:
                    self.token = data["access"]
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.token}"
                    })
                    self.log_test("用户登录", True, "获取到访问令牌")
                    return True
                else:
                    self.log_test("用户登录", False, "响应中缺少令牌")
                    return False
            else:
                self.log_test("用户登录", False, f"状态码: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("用户登录", False, f"错误: {str(e)}")
            return False
    
    def test_user_profile(self):
        """测试获取用户资料"""
        if not self.token:
            self.log_test("获取用户资料", False, "未登录")
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/auth/profile/")
            
            if response.status_code == 200:
                data = response.json()
                username = data.get("username", "未知")
                self.log_test("获取用户资料", True, f"用户名: {username}")
                return True
            else:
                self.log_test("获取用户资料", False, f"状态码: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("获取用户资料", False, f"错误: {str(e)}")
            return False
    
    def test_project_operations(self):
        """测试项目相关操作"""
        if not self.token:
            self.log_test("项目操作", False, "未登录")
            return False
        
        project_id = None
        
        # 创建项目
        try:
            project_data = {
                "name": "API测试项目" + str(time.time()),
                "description": "通过API创建的测试项目",
                "device_type": "web"
            }
            
            response = self.session.post(
                f"{self.base_url}/projects/",
                json=project_data
            )
            
            if response.status_code == 201:
                data = response.json()
                project_id = data.get("id")
                self.log_test("创建项目", True, f"项目ID: {project_id}")
            else:
                self.log_test("创建项目", False, f"状态码: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("创建项目", False, f"错误: {str(e)}")
            return False
        
        # 获取项目列表
        try:
            response = self.session.get(f"{self.base_url}/projects/")
            
            if response.status_code == 200:
                data = response.json()
                projects_count = len(data.get("results", data))
                self.log_test("获取项目列表", True, f"项目数量: {projects_count}")
            else:
                self.log_test("获取项目列表", False, f"状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("获取项目列表", False, f"错误: {str(e)}")
        
        return project_id is not None
    
    def test_page_operations(self, project_id=None):
        """测试页面相关操作"""
        if not self.token:
            self.log_test("页面操作", False, "未登录")
            return False
        
        page_id = None
        
        # 创建页面
        try:
            page_data = {
                "name": "API测试页面" + str(time.time()),
                "layout_config": {
                    "components": []
                }
            }
            
            # 不强制关联项目，允许独立页面
            # if project_id:
            #     page_data["project"] = project_id
            
            response = self.session.post(
                f"{self.base_url}/pages/",
                json=page_data
            )
            
            if response.status_code == 201:
                data = response.json()
                page_id = data.get("id")
                self.log_test("创建页面", True, f"页面ID: {page_id}")
            else:
                self.log_test("创建页面", False, f"状态码: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("创建页面", False, f"错误: {str(e)}")
            return False
        
        # 获取页面列表
        try:
            response = self.session.get(f"{self.base_url}/pages/")
            
            if response.status_code == 200:
                data = response.json()
                pages_count = len(data.get("results", data))
                self.log_test("获取页面列表", True, f"页面数量: {pages_count}")
            else:
                self.log_test("获取页面列表", False, f"状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("获取页面列表", False, f"错误: {str(e)}")
        
        return page_id
    
    def test_component_operations(self, page_id=None):
        """测试组件相关操作"""
        if not self.token or not page_id:
            self.log_test("组件操作", False, "未登录或无页面ID")
            return False
        
        component_id = None
        
        # 创建组件
        try:
            component_data = {
                "page_id": page_id,
                "type": "Button",
                "properties": {
                    "label": "API测试按钮",
                    "color": "#4F46E5",
                    "variant": "filled",
                    "x": 100,
                    "y": 100,
                    "w": 120,
                    "h": 40,
                    "customCSS": "border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/components/",
                json=component_data
            )
            
            if response.status_code == 201:
                data = response.json()
                component_id = data.get("id")
                self.log_test("创建组件", True, f"组件ID: {component_id}")
            else:
                self.log_test("创建组件", False, f"状态码: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("创建组件", False, f"错误: {str(e)}")
            return False
        
        # 获取组件列表
        try:
            response = self.session.get(f"{self.base_url}/components/?page_id={page_id}")
            
            if response.status_code == 200:
                data = response.json()
                components_count = len(data.get("results", data))
                self.log_test("获取组件列表", True, f"组件数量: {components_count}")
            else:
                self.log_test("获取组件列表", False, f"状态码: {response.status_code}")
                
        except Exception as e:
            self.log_test("获取组件列表", False, f"错误: {str(e)}")
        
        # 更新组件
        if component_id:
            try:
                update_data = {
                    "type": "Button",
                    "properties": {
                        "label": "更新的API测试按钮",
                        "color": "#EF4444",
                        "customCSS": "border-radius: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
                    }
                }
                
                response = self.session.put(
                    f"{self.base_url}/components/{component_id}/",
                    json=update_data
                )
                
                if response.status_code == 200:
                    self.log_test("更新组件", True, "组件属性更新成功")
                else:
                    self.log_test("更新组件", False, f"状态码: {response.status_code}")
                    
            except Exception as e:
                self.log_test("更新组件", False, f"错误: {str(e)}")
        
        return component_id is not None
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始 LCDP Django REST Framework API 测试")
        print("=" * 50)
        
        # 基础连接测试
        if not self.test_api_connection():
            print("\n❌ API服务器连接失败，请检查Docker服务是否正常运行")
            return False
        
        # 认证测试
        self.test_user_registration()
        if not self.test_user_login():
            print("\n❌ 用户登录失败，无法继续测试")
            return False
        
        self.test_user_profile()
        
        # 业务功能测试
        project_id = self.test_project_operations()
        page_id = self.test_page_operations(project_id if project_id else None)
        self.test_component_operations(page_id)
        
        # 统计测试结果
        print("\n" + "=" * 50)
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, success, _ in self.test_results if success)
        failed_tests = total_tests - passed_tests
        
        print(f"📊 测试总结:")
        print(f"   总测试数: {total_tests}")
        print(f"   通过: {passed_tests} ✅")
        print(f"   失败: {failed_tests} ❌")
        print(f"   成功率: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 所有API测试通过！Django REST Framework 配置完美！")
        else:
            print("\n⚠️  有部分测试失败，请检查API配置")
        
        return failed_tests == 0

def main():
    """主函数"""
    tester = LCDPAPITester()
    success = tester.run_all_tests()
    
    print("\n🔗 有用的链接:")
    print(f"   API 根地址: {BASE_URL}")
    print(f"   DRF 可浏览 API: {BASE_URL}/")
    print(f"   Django Admin: http://localhost:8000/admin/")
    print(f"   前端应用: http://localhost:3000/")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 