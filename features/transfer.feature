Feature: Transfer
    Send some crypto from one wallet to anouther

    Scenario Outline: Make a transfer by phone
        Given Some crypto on balance
        When User send <asset> to phone number
        Then User has new record in operation history
        And User`s balance is changed
        And Receive user has new record in operation history
        And Receive user`s balance is changed
        Examples:
            | asset |
            | LTC   |
            | BTC   |
            | ETH   |