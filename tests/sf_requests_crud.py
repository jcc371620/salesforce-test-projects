# 1. 使用 requests 库直接调用 Salesforce REST API 来实现 CRUD 操作
# 2. 通过手动构造 HTTP 请求，来更底层地理解 Salesforce API 的工作原理
# 3. 业务场景：模拟一个零售门店的客户信息管理系统，展示如何通过 REST API 来创建、查询、更新和删除客户数据
# 4. 每一步操作后都进行结果验证，确保数据正确性和 API 调用的成功与否
# 5. 最后清理测试数据，保持环境整洁

# 1. post_url = f"{instance_url}/services/data/v60.0/sobjects/Account/"  # 创建新客户的 API 端点
# 2. get_url = f"{instance_url}/services/data/v60.0/sobjects/Account/{new_id}"  # 获取客户信息的 API 端点
# 3. patch_url = f"{instance_url}/services/data/v60.0/sobjects/Account/{new_id}"  # 更新客户信息的 API 端点
# 4. delete_url = f"{instance_url}/services/data/v60.0/sobjects/Account/{new_id}"  # 删除客户的 API 端点

import requests
import json
from tests.test_connection import SalesforceClient  

def run_requests_demo():
    # --- 1. 获取认证信息 (这是所有请求的“通行证”) ---
    client = SalesforceClient()
    sf = client.connect()
    
    access_token = sf.session_id
    # 这里的 base_url 通常是 https://xxx.my.salesforce.com
    instance_url = sf.base_url.split('/services')[0] 
    
    # 公用请求头
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print(f"🚀 开始执行 Requests 核心四部曲...")

    #  第一步：POST (增) - 新建一个测试门店，并获取它的 ID 以供后续操作使用
    # 业务描述：模拟业务员在系统中录入一家新的零售门店
    post_url = f"{instance_url}/services/data/v60.0/sobjects/Account/"
    new_store_data = {
        "Name": "Requests测试门店_001",
        "Type": "Retail Store",
        "Phone": "13800000000",
        "Description": "由 Requests 脚本创建的测试数据"
    }
    
    res_post = requests.post(post_url, headers=headers, json=new_store_data)
    if res_post.status_code == 201:
        new_id = res_post.json()['id']
        print(f"✅ [POST] 新建成功! 门店 ID: {new_id}")
    else:
        print(f"❌ [POST] 新建失败: {res_post.text}")
        return

    #  第二步：GET (查) - 确认刚才创建的门店数据，并获取它的详细信息
    # 业务描述：通过 ID 获取该门店的详细信息进行审计
    get_url = f"{instance_url}/services/data/v60.0/sobjects/Account/{new_id}"
    
    res_get = requests.get(get_url, headers=headers)
    if res_get.status_code == 200:
        store_info = res_get.json()
        print(f"✅ [GET] 查询成功! 门店名称: {store_info['Name']}, 状态码: {res_get.status_code}")
    else:
        print(f"❌ [GET] 查询失败: {res_get.text}")

    #  第三步：PATCH (改) - 修改门店的电话号码，模拟门店信息变更后的数据维护
    # 业务描述：模拟门店信息变更后的数据维护
    patch_url = f"{instance_url}/services/data/v60.0/sobjects/Account/{new_id}"
    update_data = {"Phone": "400-888-9999"}
    
    res_patch = requests.patch(patch_url, headers=headers, json=update_data)
    
    # 注意：Salesforce 更新成功通常返回 204 (No Content)
    if res_patch.status_code == 204:
        print(f"✅ [PATCH] 更新成功! 状态码: {res_patch.status_code}")
    else:
        print(f"❌ [PATCH] 更新失败: {res_patch.text}")

    #  第四步：DELETE (删) - 清理测试数据，保持环境整洁
    # 业务描述：测试完成后，删除产生的脏数据，保持环境整洁
    delete_url = f"{instance_url}/services/data/v60.0/sobjects/Account/{new_id}"
    
    res_delete = requests.delete(delete_url, headers=headers)
    if res_delete.status_code == 204:
        print(f"✅ [DELETE] 删除成功! 状态码: {res_delete.status_code}")
        print(f"🧹 测试记录 {new_id} 已从系统中移除。")
    else:
        print(f"❌ [DELETE] 删除失败: {res_delete.text}")

if __name__ == "__main__":
    run_requests_demo()