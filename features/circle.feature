Feature: Circle
    @smoke
    @circle_all
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
    @circle_all
    @circle_bank_accounts
        Scenario Outline: Add bank accounts
            Given bank_country is <bank_country>
            And billing_country is <billing_country>
            And account_number is <account_number>
            And iban is <iban>
            And routing_number is <routing_number>
            And guid is <guid>
            When user add bank account
            Then response status code has to be equals to <status_code>
            And response must contains created bank account info
        Examples:
        | bank_country | billing_country | account_number | iban | routing_number | guid   | status_code |
        | US           | US              | 123400120      | null | 121000248      | unique | 200         |