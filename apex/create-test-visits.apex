// ==========================================
// 脚本名称: create-test-visits.apex
// 用途: 批量创建巡店记录测试数据
// ==========================================

// 获取门店ID（先查出来）
List<Retail_Store__c> stores = [SELECT Id FROM Retail_Store__c LIMIT 10];

if (stores.isEmpty()) {
    System.debug('❌ 没有找到门店，请先创建门店数据');
} else {
    List<Visit__c> visits = new List<Visit__c>();
    
    for (Integer i = 0; i < 50; i++) {
        visits.add(new Visit__c(
            Name = 'AutoTest_Visit_' + i,
            Store__c = stores[Math.mod(i, stores.size())].Id,
            Shortage_Quantity__c = Math.random() * 10,
            Visit_Date__c = Date.today()
        ));
    }
    
    insert visits;
    System.debug('✅ 创建了 ' + visits.size() + ' 条巡店记录');
}