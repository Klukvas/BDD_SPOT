Feature: Circle
#    @smoke
#    @circle_all
#    @circle_cards
#        Scenario: Make a deposit by card
#            Given User get encryption key
#            And User encrypt data of his card
#            When User add new card
#            Then User create deposit via card
#            And User has new record in operation history
#            And User`s balance is changed
#            And User delete his card
#
#####################################################################################################################

#    @smoke
#    @circle_all
#    @circle_bank_accounts
#        Scenario Outline: Add bank account
#            Given bank_country is <bank_country>; billing_country is <billing_country>; account_number is <account_number>; iban is <iban>; routing_number is <routing_number>; guid is <guid>
#            When user add bank account
#            Then response status code has to be equals to <status_code>
#            And response must contains bank account info
#        Examples:
#        | bank_country | billing_country | account_number | iban                              | routing_number | guid   | status_code |
#        | US           | US              | 123400120      | null                              | 121000248      | unique | 200         |
#        | IT           | IT              | null           | IT60 X054 2811 1010 0000 0123 456 | null           | unique | 200         |
#        | CL           | CL              | 98765432       | null                              | AFPPCLR2       | unique | 200         |
#
#    @smoke
#    @circle_all
#    @circle_bank_accounts
#        Scenario: Get all bank accounts if count(bank_accounts) >= 1
#            When user send request to get all bank accounts (>=1)
#            Then response status code has to be equals to 200
#            And response must contains info about all bank accounts
#
#    @smoke
#    @circle_all
#    @circle_bank_accounts
#        Scenario: Get all bank accounts if count(bank_accounts) == 0
#            When user send request to get all bank accounts (0)
#            Then response status code has to be equals to 200
#            And response must return empty list
#
    @smoke
    @circle_all
    @circle_bank_accounts
        Scenario: Get bank account if it exist
            When user send request to get bank account if it exist
            Then response status code has to be equals to 200
            And response must contains info about bank account

    @smoke
    @circle_all
    @circle_bank_accounts
        Scenario: Get bank account if bank_account_id is not user's
            When user send request to get bank account if bank_account_id is not my
            Then response status code has to be equals to 200
            And response must returns BankAccountNotFound

    @smoke
    @circle_all
    @circle_bank_accounts
        Scenario: Get bank account with no auth token
            When user send request to get bank account with no auth token
            Then response status code has to be equals to 401

    @smoke
    @circle_all
    @circle_bank_accounts
        Scenario: Get bank account if bank_account_id was deleted
            When user send request to get bank account if bank_account_id was deleted
            Then response status code has to be equals to 200
            And response must returns BankAccountNotFound

    @smoke
    @circle_all
    @circle_bank_accounts
        Scenario: Get bank account if bank_account_id is invalid
            When user send request to get bank account if bank_account_id is invalid
            Then response status code has to be equals to 200
            And response must returns BankAccountNotFound