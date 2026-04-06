// ==========================================
// 脚本名称: check-sharing-rule.apex
// 用途: 验证天津业务员是否能看到北京业务员的记录
// ==========================================

// 1. 获取测试用户
User tianjinUser = [SELECT Id FROM User WHERE Name LIKE '%天津%' LIMIT 1];
User beijingUser = [SELECT Id FROM User WHERE Name LIKE '%北京%' LIMIT 1];

if (tianjinUser == null || beijingUser == null) {
    System.debug('❌ 请确保存在天津和北京业务员用户');
} else {
    // 2. 用北京业务员身份创建一条记录
    Visit__c beijingVisit;
    System.runAs(beijingUser) {
        beijingVisit = new Visit__c(
            Name = 'Sharing_Test_Visit',
            Store__c = [SELECT Id FROM Store__c LIMIT 1].Id
        );
        insert beijingVisit;
        System.debug('✅ 北京业务员创建了记录: ' + beijingVisit.Id);
    }
    
    // 3. 验证天津业务员是否能访问
    System.runAs(tianjinUser) {
        List<Visit__c> accessible = [
            SELECT Id FROM Visit__c WHERE Id = :beijingVisit.Id
        ];
        
        if (!accessible.isEmpty()) {
            System.debug('✅ Sharing Rule 生效：天津业务员可以看到北京业务员的记录');
        } else {
            System.debug('❌ Sharing Rule 未生效：天津业务员看不到北京业务员的记录');
        }
    }
}