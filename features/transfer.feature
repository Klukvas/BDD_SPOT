Feature: Transfer
    Send some crypto from one wallet to anouther
    
    Background: Check crypto balance
        Given Some crypto on balance

    Scenario Outline: Make a transfer by phone
        When User send <asset> to phone number
        Then User has new record in operation history
        And User`s balance is changed
        And Receive user has new record in operation history
        And Balance of receive user are correct
        Examples:
            | asset |
            | LTC   |
            | BTC   |
            | ETH   |
    
    Scenario Outline: Make a internalWithdrawal
        When User send <assetId> to <address>
        Then User has new record(withdrawal) in operation history
        And User`s balance is changed after withdrawal
        And Receive user has new record(deposit) in operation history
        And Balance of deposited user are correct
        Examples:
            | assetId | address                                     |
            | LTC   | QfLN5dHi3NLsYJrGqLJUrhkGUXnQKVju35          |
            | BTC   | 2N15SuQSqCu2vuN8LeGQm7rsjES2QGXn24b         |
            | ETH   | 0xbed6f295026de344c1e80b1cfdaf545d00cd6900  |