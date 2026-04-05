# 1. 读取目前系统中所有account数量并print
# 2. 导入csv表格
# 3. 再次读取accout数量并print
# 4. 删除刚才导入的数据
# 5. 再次读取account的数量并print

import pandas as pd
from tests.test_connection import SalesforceClient

def run_csv_integration_demo():
    # 0. 初始化连接
    client = SalesforceClient()
    sf = client.connect()
    if not sf: return

    # 步骤 1. 读取目前系统中所有 Account 数量，并打印出来。这是为了在导入数据之前先了解一下当前系统中有多少条 Account 记录，以便后续对比导入后的数量变化。
    print("\n" + "="*60)
    count_res_initial = sf.query("SELECT COUNT(Id) total FROM Account")
    total_before = count_res_initial['records'][0]['total']
    print(f"📊 [步骤 1] 初始审计：当前系统中共有 {total_before} 条 Account 记录。")


    # 步骤 2. 导入 CSV 表格，从一个指定路径的 CSV 文件中读取数据，并尝试导入到 Salesforce 中。我们会自动探测文件的编码，以确保能够正确读取包含中文字符的 CSV 文件。然后将 CSV 数据转换成适合 Salesforce API 的格式，并逐行创建 Account 记录。同时统计成功和失败的导入数量，并打印出每一行的导入结果。
    print("\n🚀 [步骤 2] 正在从 CSV 导入数据...")
    csv_file = '/Users/jc/git/salesforce/salesforce-test-projects/import_csv_data/import_accounts2.csv'
    df_import = None
    
    # 自动探测编码
    for enc in ['gbk', 'gb18030', 'utf-8', 'utf-8-sig']:
        try:
            df_import = pd.read_csv(csv_file, encoding=enc)
            print(f"📖 读取成功！探测到文件编码为: {enc}")
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if df_import is None:
        print(f"❌ 错误：无法读取 {csv_file}")
        return

    records_to_import = df_import.to_dict('records')
    
    #  ⭐ 修改点：用字典来存储 {ID: Name} 的对应关系
    newly_created_records = {}

    success_count = 0 # 成功计数器
    fail_count = 0    # 失败计数器
    for i, row in enumerate(records_to_import, 1): # 遍历每一行数据，i 是行号（从 1 开始），row 是一个字典，包含了这一行的字段和值。
        # 清理 NaN 值：过滤掉所有空字段，只发有内容的。这是因为 Salesforce API 不喜欢接收值为 NaN 的字段。我们使用 pandas 的 notnull() 方法来检查每个字段的值，如果值不是 NaN，我们就保留这个字段，否则就过滤掉。这样我们就得到了一个只包含有效字段的 clean_row 字典。
        clean_row = {k: v for k, v in row.items() if pd.notnull(v)}
        
        if 'Name' in clean_row:
            try:
                # 创建并获取返回的 ID
                result = sf.Account.create(clean_row)
                new_id = result['id']
                newly_created_records[new_id] = clean_row['Name']

                success_count += 1
                print(f"  ✅ 第 {i} 行导入成功: Name: {clean_row['Name']} | ID: {new_id}")
            except Exception as e:
                print(f"  ❌ 第 {i} 行导入失败: {e}")
        else:
            print(f"  ⚠️ 第 {i} 行跳过：缺少 'Name'")

    print(f"🎊 导入尝试结束。成功创建了 {success_count} 条数据。")


    # 步骤 3. 再次读取 Account 数量并验证 
    count_res_after = sf.query("SELECT COUNT(Id) total FROM Account")
    total_after = count_res_after['records'][0]['total']
    print(f"\n📊 [步骤 3] 导入后审计：当前系统中共有 {total_after} 条 Account 记录。")
    print(f"📈 净增长：{total_after - total_before} 条。")


    # 步骤 4. 删除刚才导入的数据 
    print(f"\n🧹 [步骤 4] 正在清理数据：准备删除刚才导入的 {len(newly_created_records)} 条记录...")
    
    delete_count = 0
    for acc_id, acc_name in newly_created_records.items():
        try:
            sf.Account.delete(acc_id) # 使用 simple-salesforce 提供的 delete 方法，传入记录的 ID 来删除对应的 Account 记录。如果删除成功，我们就增加删除计数器，并打印一条成功信息；如果删除失败，我们就捕获异常，并打印一条错误信息。遍历这个列表，只删除我们亲手创建的那几条。这比根据“名字”删除要安全得多，因为这样不会误删系统中原本就存在的重名数据
            delete_count += 1
            print(f"  🗑️ 已删除 ID: {acc_id} ｜ Name: {acc_name:<20}")
        except Exception as e:
            print(f"  ❌ 删除失败 ID {acc_id}: {e}")

    print(f"✅ 清理完成，共成功删除 {delete_count} 条数据。")


    # 步骤 5. 再次读取 Account 的数量并 print 
    print("\n" + "="*60)
    count_res_final = sf.query("SELECT COUNT(Id) total FROM Account")
    total_final = count_res_final['records'][0]['total']
    print(f"📊 [步骤 5] 最终审计：数据清理后，系统中剩余 {total_final} 条 Account 记录。")
    
    # 验证最终数量是否与初始数量一致，以确认数据已经成功清理。如果最终数量与初始数量相同，说明我们成功地恢复了系统到测试前的状态；如果不一致，我们就打印一个警告信息，提示用户检查是否有其他操作影响了数据。
    if total_final == total_before:
        print("✨ 完美！系统已恢复到测试前的原始状态。")
    else:
        print("⚠️ 警告：最终数量与初始数量不一致，请检查是否有其他操作。")
    print("="*60)

if __name__ == "__main__":
    run_csv_integration_demo()



