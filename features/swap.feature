Feature: Swap
    Convert one crypto to anouther

    Scenario Outline: Make a swap with fixed True
        Given Some crypto on balance
        When User gets swap quote from <fromAsset> to <toAsset>
        And User execute quote
        Then User has new record in operation history
        And User`s balance is changed
        Examples:
            | fromAsset | toAsset   |
            | LTC       | USD       |
            # | BTC       | USD       |
            # | BTC       | EUR       |
            # | ETH       | EUR       |
            # | BCH       | USD       |
            # | BTC       | ETH       |
            # | LTC       | BCH       |
            # | ETH       | LTC       |
            # | BCH       | BTC       |
    
    Scenario Outline: Make a swap with fixed False
        Given Some crypto on balance
        When User gets swap quote from <fromAsset> to <toAsset>
        And User execute quote
        Then User has new record in operation history
        And User`s balance is changed
        Examples:
            | fromAsset | toAsset   |
            | LTC       | USD       |
            # | BTC       | USD       |
            # | BTC       | EUR       |
            # | ETH       | EUR       |
            # | BCH       | USD       |
            # | BTC       | ETH       |
            # | LTC       | BCH       |
            # | ETH       | LTC       |
            # | BCH       | BTC       |


            