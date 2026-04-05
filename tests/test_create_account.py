# 1.查询原始数据
# 2.创建五条数据
# 3.修改第一条数据
# 4.删除第三条数据
# 5.再次查询数据，验证前面操作的结果
# 一个简单的 Salesforce API 操作示例，展示了如何使用 simple-salesforce 库来创建、查询、更新和删除 Account 对象。它首先连接到 Salesforce，然后执行一系列操作来验证连接和 API 功能是否正常工作。
# sf.Account.create()	POST    创建一个新的 Account 记录。 
# sf.Account.update()	PATCH   更新一个已有的 Account 记录。
# sf.Account.delete()	DELETE  删除一个已有的 Account 记录。
# sf.query()	        GET     执行一个 SOQL 查询，获取数据。
from tests.test_connection import SalesforceClient


def run_simple_demo():
    # 0. 初始化连接
    client = SalesforceClient()
    sf = client.connect()
    if not sf: return

    # 步骤 0: [SOQL] 先查询原始数据，看看当前系统中有哪些 Account 记录。这是为了在测试前了解一下现有数据的情况。
    print("\n" + "="*60)
    print("🔍 [步骤 0] 初始状态查询 (SOQL)")
    soql_init = "SELECT id, Name, Industry FROM Account ORDER BY CreatedDate DESC"
    init_res = sf.query(soql_init)
    print(f"执行语句: {soql_init}")
    print(f"📊 当前系统中共有 {init_res['totalSize']} 条 Account 记录：")
    print(f"📊 当前系统中所有的Account:")
    if init_res['totalSize'] == 0:
        print("   (当前数据库为空)")
    for r in init_res['records']:
        print(f"   🔹 ID: {r['Id']} | Name: {r['Name']} | Industry: {r['Industry']}")
    print("="*60) # 分割线，清晰区分步骤

    # 步骤 1: [CRUD] 创建五条 Account 数据
    print("\n🚀 [步骤 1] POST: 开始创建 5 条测试数据...")
    # 手动创建 5 条，并记录各自的 ID
    id1 = sf.Account.create({'Name': 'Jessy_Owner_001', 'Industry': 'Banking'})['id']
    id2 = sf.Account.create({'Name': 'Jessy_Owner_002', 'Industry': 'Shipping'})['id']
    id3 = sf.Account.create({'Name': 'Jessy_Owner_003', 'Industry': 'Technology'})['id']
    id4 = sf.Account.create({'Name': 'Jessy_Owner_004', 'Industry': 'Manufacturing'})['id']
    id5 = sf.Account.create({'Name': 'Jessy_Owner_005', 'Industry': 'Education'})['id']
    
    # 拼接 ID 字符串，用于后续的 SOQL 过滤
    all_test_ids = f"'{id1}','{id2}','{id3}','{id4}','{id5}'"
    print(f"✅ 5 条新数据已创建成功。")

    # 验证步骤1创建的五条Account
    print("\n🔍 [SOQL 验证]: 查询刚才创建的这 5 条记录")
    soql_verify = f"SELECT id, Name, Industry FROM Account WHERE Id IN ({all_test_ids}) order by CreatedDate DESC"
    results = sf.query(soql_verify) # 这里的 sf.query() 是 simple-salesforce 库提供的方法，它会把你写的 SOQL 语句翻译成一个 REST API 请求，发送给 Salesforce，然后把返回的 JSON 数据转换成 Python 字典。
    for r in results['records']:
        print(f"   🏢 ID: {r['Id']} | Name: {r['Name']} | Industry: {r['Industry']}")
    print("="*60) # 分割线，清晰区分步骤


    # 步骤 2: [CRUD] 修改第一条Account的信息
    print(f"\n📝 [步骤 2] PATCH: 修改第 1 条数据 (ID: {id1})")
    sf.Account.update(id1, {'Name': 'Jessy_Owner_020', 'Industry': 'Consulting'})
    
    # 验证步骤2的修改结果，查询刚才修改的这条记录，看看名字和行业是否已经更新成功。
    soql_check_patch = f"SELECT id, Name, Industry FROM Account WHERE Id = '{id1}'"
    updated_data = sf.query(soql_check_patch)['records'][0]
    print(f"📊 修改结果 -> ID: {updated_data['Id']} | Name: {updated_data['Name']} | Industry: {updated_data['Industry']}")
    print("="*60) # 分割线，清晰区分步骤


    # 步骤 3: [CRUD] 删除第三条Account
    print(f"\n🗑️ [步骤 3] DELETE: 删除第 3 条数据 (ID: {id3})")
    sf.Account.delete(id3)
    
    # 验证步骤3的删除结果，用 SOQL 的 Count 函数统计这组测试数据还剩几条
    soql_count = f"SELECT Count(Id) total FROM Account WHERE Id IN ({all_test_ids})"
    count_res = sf.query(soql_count)
    remaining = count_res['records'][0]['total']
    print(f"📊 验证删除 -> 初始 5 条，当前这组测试数据剩余: {remaining} 条")
    print("="*60) # 分割线，清晰区分步骤


    # 最后再查询一次，看看最终剩下哪些数据，确认一下删除和修改的结果。
    print("\n🏁 [最终清单]: 剩余有效测试数据")
    final_res = sf.query(soql_verify)
    for r in final_res['records']:
        print(f"   ✅ 存留: {r['Name']}")


    # 步骤 4: 再次打印目前所有的 Account 数据
    print("\n" + "="*60)
    print("🌎 [最终步骤] 打印当前系统中所有的 Account 数据")
    # 不加 WHERE 过滤，查询所有
    soql_all = "SELECT Id, Name, Industry FROM Account ORDER BY Name ASC"
    final_res = sf.query(soql_all)
    
    print(f"执行语句: {soql_all}")
    print(f"📋 当前 Salesforce 组织内共有 {final_res['totalSize']} 条记录:")
    for i, r in enumerate(final_res['records'], 1):
        # 打印序号、ID后五位、名称和行业
        name = r['Name']
        industry = r.get('Industry') or "未填写"
        print(f"   {i:02d}. [ID: {r['Id']} | Name: {r['Name']} | Industry: {r['Industry']}")
    print("="*60)

if __name__ == "__main__":
    run_simple_demo()