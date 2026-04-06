// ==========================================
// 脚本名称: delete-test-data.apex
// 用途: 清理名称包含 "AutoTest" 的测试数据
// ==========================================

// 查找要删除的巡店记录
List<Visit__c> testVisits = [
    SELECT Id FROM Visit__c
    WHERE Name LIKE 'AutoTest_%'
    AND CreatedDate = TODAY
];

if (!testVisits.isEmpty()) {
    delete testVisits;
    System.debug('✅ 删除了 ' + testVisits.size() + ' 条测试巡店记录');
} else {
    System.debug('📋 没有找到需要删除的测试数据');
}