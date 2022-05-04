@circle_all
Feature: Circle
    @smoke
    @circle_cards
        Scenario: Make a deposit by card
            Given User get encryption key
            And User encrypt data of his card
            When User add new card
            Then User create deposit via card
            And User has new record in operation history
            And User`s balance is changed
            And User delete his card
    @smoke
    @circle_bank_accounts
        Scenario Outline: Add bank account
            Given bank_country is <bank_country>; billing_country is <billing_country>; account_number is <account_number>; iban is <iban>; routing_number is <routing_number>; guid is <guid>
            When user add bank account
            Then response must contains bank account info
        Examples:
        | bank_country | billing_country | account_number | iban                              | routing_number | guid   |
        | US           | US              | 123400120      | null                              | 121000248      | unique |
        | IT           | IT              | null           | IT60 X054 2811 1010 0000 0123 456 | null           | unique |
        | CL           | CL              | 98765432       | null                              | AFPPCLR2       | unique |
#
    @smoke
    @circle_bank_accounts
        Scenario: Get all bank accounts if count(bank_accounts) >= 1
            When user send request to get all bank accounts (>=1)
            Then response must contains info about all bank accounts
#
    @smoke
    @circle_bank_accounts
        Scenario: Get all bank accounts if count(bank_accounts) == 0
            When user send request to get all bank accounts (0)
            Then response must return empty list

    @smoke
    @circle_bank_accounts
        Scenario: Get bank account if it exist
            When user send request to get bank account if it exist
            Then response must contains info about bank account

    @circle_bank_accounts
        Scenario: Get bank account if bank_account_id is not user's
            When user send request to get bank account if bank_account_id is not my
            Then response must returns BankAccountNotFound

    @circle_bank_accounts
        Scenario: Get bank account with no auth token
            When user send request to get bank account with no auth token
            Then response status code has to be equals to 401

    @circle_bank_accounts
        Scenario: Get bank account if bank_account_id was deleted
            When user send request to get bank account if bank_account_id was deleted
            Then response must returns BankAccountNotFound
#
    @circle_bank_accounts
        Scenario: Get bank account if bank_account_id is invalid
            When user send request to get bank account if bank_account_id is invalid
            Then response must returns BankAccountNotFound
#
    @smoke
    @circle_bank_accounts
        Scenario: Delete bank account of user
            Given user send request to parse existed bank_account_id (>=1)
            When user send request to delete bank account
            Then response must contains deleted true
            And get-bank-accounts-all haven't to return deleted bank account

    @circle_bank_accounts
        Scenario: Delete bank account of user that was deleted already
            Given user send request to parse existed bank_account_id (>=1)
            And user get deleted bank_account_id
            When user send request to delete bank account
            Then response must contains deleted true
            And count of bank accounts at get-bank-accounts-all hasn't change

    @circle_bank_accounts
        Scenario: Delete bank account of another user
            Given user send request to parse existed bank_account_id (>=1)
            When user2 send request to delete bank account
            Then response must contains deleted true
            And count of bank accounts at get-bank-accounts-all hasn't change

    @circle_bank_accounts
        Scenario: Delete bank account without token
            Given user send request to parse existed bank_account_id (>=1)
            When user send request to delete bank account without token
            Then response status code has to be equals to 401
            And count of bank accounts at get-bank-accounts-all hasn't change