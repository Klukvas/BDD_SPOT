Feature: Swap
    Convert one crypto to anouther
    Background: Check balance
        Given Some crypto on balance
    Scenario Outline: Make a swap with fixed True
        When User gets swap quote with fixed True from <fromAsset> to <toAsset>
        And User execute quote (fixed True)
        Then User has new record in operation history (fixed True)
        And User`s balance is changed (fixed True)
        Examples:
            | fromAsset | toAsset   |
            | LTC       | USD       |
            | BTC       | USD       |
            | BTC       | EUR       |
            | ETH       | EUR       |
            | BCH       | USD       |
            | BTC       | ETH       |
            | LTC       | BCH       |
            | ETH       | LTC       |
            | USD       | LTC       |
            | USD       | ETH       |
            | EUR       | BTC       |
    
    Scenario Outline: Make a swap with fixed False
        When User gets swap quote from <fromAsset> to <toAsset>
        And User execute quote
        Then User has new record in operation history
        And User`s balance is changed
        Examples:
            | fromAsset | toAsset   |
            | LTC       | USD       |
            | BTC       | USD       |
            | BTC       | EUR       |
            | ETH       | EUR       |
            | BCH       | USD       |
            | BTC       | ETH       |
            | LTC       | BCH       |
            | ETH       | LTC       |
            | BCH       | BTC       |


            