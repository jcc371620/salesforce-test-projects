// ==========================================
// 脚本名称: get-shortage-stores.apex
// 用途: 查询缺货严重的门店，供手工测试参考
// ==========================================

List<AggregateResult> results = [
    SELECT Store__r.Name, SUM(Shortage_Quantity__c) totalShortage
    FROM Visit__c
    WHERE Visit_Date__c = THIS_WEEK
    GROUP BY Store__r.Name
    ORDER BY totalShortage DESC
    LIMIT 10
];

System.debug('========== 本周缺货 TOP 10 门店 ==========');
for (AggregateResult result : results) {
    System.debug('门店: ' + result.get('Store__r.Name') + 
                 ', 缺货总量: ' + result.get('totalShortage'));
}