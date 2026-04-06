// ==========================================
// 脚本名称: verify-trigger.apex
// 用途: 验证缺货时是否自动创建补货任务
// ==========================================

// 1. 准备数据
Store__c testStore = [SELECT Id FROM Store__c LIMIT 1];

// 2. 创建缺货巡店记录
Visit__c visit = new Visit__c(
    Name = 'Trigger_Test_Visit',
    Store__c = testStore.Id,
    Shortage_Quantity__c = 5
);
insert visit;
System.debug('✅ 创建巡店记录: ' + visit.Id);

// 3. 验证是否自动创建了 Task
List<Task__c> tasks = [
    SELECT Id, Status__c 
    FROM Task__c 
    WHERE Visit__c = :visit.Id
];

if (!tasks.isEmpty()) {
    System.debug('✅ Trigger 生效，自动创建了 ' + tasks.size() + ' 个任务');
    System.debug('   任务状态: ' + tasks[0].Status__c);
} else {
    System.debug('❌ Trigger 未生效，没有自动创建任务');
}