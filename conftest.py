# Pytest 配置与 Fixtures

# 示例：使用 SOQL 验证数据或清理数据
def cleanup_contact(contact_id):
    # SELECT Id FROM Contact WHERE LastName = 'Automation_User_01'
    # 使用 Requests DELETE 方法删除
    pass