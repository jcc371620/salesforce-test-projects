# BDD 场景描述

Feature: Salesforce Contact Management

  Scenario: Create a contact via API and verify in UI
    Given a new contact is created via Salesforce API
    When I login to Salesforce and navigate to Contacts
    Then I should see the newly created contact in the list