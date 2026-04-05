# 1. 读取目前系统中所有account数量并print
# 2. 导入csv表格 
# 3. 再次读取accout数量并print 
# 4. 导出目前所有accout到新的csv文件，包括所有字段

import pandas as pd
from tests.test_connection import SalesforceClient

def run_csv_integration_demo():
    # 0. 初始化连接
    client = SalesforceClient()
    sf = client.connect()
    if not sf: return

    # 步骤 1. 初始审计：读取目前系统中的 Account 数量 
    print("\n" + "="*60) # 分割线，清晰区分步骤
    count_res_initial = sf.query("SELECT COUNT(Id) total FROM Account") # 这里的 sf.query() 是 simple-salesforce 库提供的方法，它会把你写的 SOQL 语句翻译成一个 REST API 请求，发送给 Salesforce，然后把返回的 JSON 数据转换成 Python 字典。我们从这个字典中提取出 total 字段，这个字段告诉我们当前系统中有多少条 Account 记录。
    total_before = count_res_initial['records'][0]['total'] # 这里的 count_res_initial['records'] 是一个列表，里面有一个字典（因为我们只查询了总数，所以只有一条记录），我们从这个字典中提取出 total 字段的值，这就是当前系统中 Account 的总数量。
    print(f"📊 [步骤 1] 初始审计：当前系统中共有 {total_before} 条 Account 记录。")

    # 步骤 2. 导入 CSV 表格 
    print("\n🚀 [步骤 2] 正在从 CSV 导入数据...")
    csv_file = '/Users/jc/git/salesforce/salesforce-test-projects/import_csv_data/import_accounts.csv'
    df_import = None
    
    # 自动探测编码：GBK (Excel中文) -> GB18030 -> UTF-8，
    # 尝试用几种常见的编码来读取 CSV 文件，直到成功为止。这个方法可以帮助我们处理不同来源的 CSV 文件，尤其是那些包含中文字符的文件。
    for enc in ['gbk', 'gb18030', 'utf-8', 'utf-8-sig']:
        try:
            df_import = pd.read_csv(csv_file, encoding=enc) # 使用 pandas 的 read_csv 方法来读取 CSV 文件，并指定编码。
            print(f"📖 读取成功！探测到文件编码为: {enc}")
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if df_import is None: # 如果所有编码尝试都失败了，我们就打印一个错误信息，提示用户检查文件是否存在以及编码是否正确，然后退出函数。
        print(f"❌ 错误：无法读取 {csv_file}，请确保文件存在且编码正确。")
        return

    # 将 DataFrame 转换为字典列表，每一行数据都会被转换成一个字典，字典的键是列名，值是对应的单元格内容。这个格式更适合后续使用 simple-salesforce 库来创建 Salesforce 记录。
    records_to_import = df_import.to_dict('records')
    success_count = 0
    fail_count = 0

    for i, row in enumerate(records_to_import, 1):
        # 【关键】清理 NaN 值：过滤掉所有空字段，只发有内容的
        clean_row = {k: v for k, v in row.items() if pd.notnull(v)}
        
        # 调试：第一行打印一下字段名，确保匹配 Salesforce
        if i == 1:
            print(f"🔍 检查到 CSV 字段: {list(clean_row.keys())}")

        # 检查必填项 'Name' (注意大小写必须与 Salesforce 一致)，如果没有这个字段，我们就跳过这行数据，并打印一个警告信息，提示用户检查 CSV 表头是否正确。如果有 'Name' 字段，我们就尝试创建一个新的 Account 记录，使用 clean_row 这个字典作为字段值。如果创建成功，我们就增加成功计数器，并打印一条成功信息；如果创建失败，我们就捕获异常，增加失败计数器，并打印一条错误信息。
        if 'Name' in clean_row:
            try:
                sf.Account.create(clean_row)
                success_count += 1
                print(f"  ✅ 第 {i} 行导入成功: {clean_row['Name']}")
            except Exception as e:
                print(f"  ❌ 第 {i} 行导入失败: {e}")
                fail_count += 1
        else:
            print(f"  ⚠️ 第 {i} 行被跳过：未找到 'Name' 字段。请检查 CSV 表头是否为 Name。")
            fail_count += 1

    print(f"🎊 导入尝试结束。成功: {success_count}, 失败: {fail_count}")


    # 步骤 3. 再次读取 Account 数量并验证 
    count_res_after = sf.query("SELECT COUNT(Id) total FROM Account")
    total_after = count_res_after['records'][0]['total']
    print(f"\n📊 [步骤 3] 导入后审计：当前系统中共有 {total_after} 条 Account 记录。")
    print(f"📈 净增长：{total_after - total_before} 条。")


    # 步骤 4. 导出目前所有 Account 到新的 CSV 文件 
    print("\n📥 [步骤 4] 正在导出全量数据到 CSV...")
    
    # 动态获取 Account 的所有字段名
    desc = sf.Account.describe()
    all_fields = [f['name'] for f in desc['fields']]
    
    # 执行全量查询 (使用 query_all 处理大数据量)
    soql_all = f"SELECT {','.join(all_fields)} FROM Account"
    all_data = sf.query_all(soql_all)
    
    # 转换为 DataFrame 并去掉 attributes 冗余列
    df_export = pd.DataFrame(all_data['records']).drop(columns=['attributes'])
    
    # 导出文件，使用 utf-8-sig 确保 Excel 打开中文不乱码
    output_file = '/Users/jc/git/salesforce/salesforce-test-projects/export_csv_data/export_accounts.csv'
    df_export.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ 导出完成！文件已保存至: {output_file}")
    print(f"📄 最终表格行数: {len(df_export)}")
    print("="*60)

if __name__ == "__main__":
    run_csv_integration_demo()