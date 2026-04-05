import pandas as pd
from test_connection import SalesforceClient

def run_retail_audit_suite():
    client = SalesforceClient()
    sf = client.connect()
    if not sf: return

    print("🚀 开始执行零售业务全链路审计...")

    # Scenario 1: 【门店全景】 查门店及其关联的巡店记录
    # 业务：总部需要确认每个门店是否按计划被访问。
    query1 = """
        SELECT Name, BillingCity, (SELECT Visit_Date__c, Status__c FROM Visits__r) 
        FROM Account WHERE Type = 'Retail Store' LIMIT 3
    """

    # Scenario 2: 【促销订单】 查本月订单及关联的产品活动
    # 业务：检查促销活动（Promotion）是否真正带动了订单项（OrderItems）的产生。
    query2 = """
        SELECT OrderNumber, TotalAmount, 
               (SELECT PricebookEntry.Product2.Name, Promotion__r.Name FROM OrderItems)
        FROM Order WHERE EffectiveDate = THIS_MONTH LIMIT 3
    """

    # Scenario 3: 【库存预警】 查低库存产品清单
    # 业务：自动筛选库存低于重订货点（Reorder Level）的门店。
    query3 = """
        SELECT Name, (SELECT Product__r.Name, On_Hand_Quantity__c FROM Store_Inventories__r 
                      WHERE On_Hand_Quantity__c < 10)
        FROM Account WHERE Type = 'Retail Store' LIMIT 3
    """

    # Scenario 4: 【陈列合规】 查巡店中的合规性检查结果，以及相关的门店和检查类型。
    # 业务：审计业务员在店内的货架排面（Facing）检查是否合格。
    query4 = """
        SELECT Name, Store__r.Name, (SELECT Check_Type__c, Result__c FROM Store_Checks__r)
        FROM Visit__c ORDER BY CreatedDate DESC LIMIT 3
    """

    # Scenario 5: 【团队业绩】 查销售代表管辖的客户合同，以及这些合同的签署状态。
    # 业务：验证销售人员名下的合同签署状态。
    query5 = """
        SELECT Name, (SELECT Name, (SELECT ContractNumber FROM Contracts) FROM Managed_Accounts__r)
        FROM User WHERE IsActive = true AND Profile.Name = 'Sales Representative' LIMIT 3
    """

    
    # Scenario 6: 获取关键巡店任务的 ID，并基于这个 ID 进行后续的依赖查询，形成一个查询链。
    # 业务描述：首先找到一个正在进行中的“重点品牌检查任务”。
    # 我们需要获取这个任务的 ID 才能进行下一步。
    print(f"\n{'='*20} 🔗 执行依赖链查询 {'='*20}")
    query6 = """
        SELECT Id, Name, Store__r.Name, Planned_Start_Time__c 
        FROM Visit__c 
        WHERE Status__c = 'In Progress' LIMIT 1
    """
    
    try:
        res6 = sf.query(query6)
        if res6['records']:
            visit_record = res6['records'][0]
            visit_id = visit_record['Id']
            store_name = visit_record['Store__r']['Name']
            print(f"✅ Query 6 成功: 捕获到正在进行的巡店任务 ID: {visit_id} (门店: {store_name})")

            # Scenario 7: 【深度审计该任务下的库存盘点明细
            # 业务描述：拿到 Query 6 的 ID 后，专门去查该次巡店中，业务员具体盘点了哪些产品。
            # 这是为了防止业务员“只签到不干活”，必须确认有具体的盘点记录（Inventory Check）。
            query7 = f"""
                SELECT Product__r.Name, Expected_Quantity__c, Actual_Quantity__c, Discrepancy__c
                FROM Inventory_Check__c 
                WHERE Visit__c = '{visit_id}'
            """
            
            res7 = sf.query(query7)
            print(f"📊 Query 7 结果 (基于 ID {visit_id} 的盘点明细):")
            if res7['records']:
                for check in res7['records']:
                    print(f"   ▫️ 产品: {check['Product__r']['Name']} | 预期: {check['Expected_Quantity__c']} | 实盘: {check['Actual_Quantity__c']}")
            else:
                print("   ⚠️ 警告：该巡店记录下尚未上传具体的盘点明细。")
        else:
            print("📝 Query 6 未发现进行中的巡店任务，跳过 Query 7。")
    except Exception as e:
        print(f"❌ 依赖查询链执行失败: {e}")

    # =================================================================
    # 🖨️ 打印前 5 个Scenario的结果
    all_queries = [
        ("1. 门店巡店历史", query1),
        ("2. 订单促销关联", query2),
        ("3. 门店缺货预警", query3),
        ("4. 货架陈列审计", query4),
        ("5. 业务员管辖链路", query5)
    ]

    for title, soql in all_queries:
        print(f"\n{'='*40}\n🏪 零售Scenario: {title}\n{'='*40}")
        try:
            res = sf.query(soql)
            if not res['records']:
                print("📝 暂无数据")
                continue
            for record in res['records']:
                print(f"📍 主记录: {record.get('Name') or record.get('OrderNumber')}")
                for k, v in record.items():
                    if isinstance(v, dict) and 'records' in v:
                        print(f"  └─ 子项 [{k}]: {len(v['records'])} 条记录")
        except Exception as e:
            print(f"❌ 查询执行失败: {e}")

if __name__ == "__main__":
    run_retail_audit_suite()