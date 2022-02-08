@transfer
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
            | LTC   | tltc1qz3qgnmt9fyd77rv4f0jh3aer0yu6mlgje7jx0a          |
            | BTC   | tb1qkttnq44z65020l0vwxq98cnjcu38sv7cmsvs2k         |
            | ETH   | 0x3472b8126294D67b1586519425Ea3b98f32ABD05  |