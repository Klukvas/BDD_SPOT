Feature: Swap
    Convert one crypto to another
    @swap
    Scenario Outline: Make a swap
        Given Some crypto on balance
        When User gets swap quote with from fixed <isFromFixed> from asset <fromAsset> to  asset <toAsset>
        And User execute quote
        Then User has new record in operation history
        And User`s balance is changed
        Examples:
            | fromAsset | toAsset   | isFromFixed |
            | LTC       | USD       | True        |
            | BTC       | USD       | True        |
            | BTC       | EUR       | True        |
            | ETH       | EUR       | True        |
            | BCH       | USD       | True        |
            | BTC       | ETH       | True        |
            | LTC       | BCH       | True        |
            | ETH       | LTC       | True        |
            | USD       | LTC       | True        |
            | USD       | ETH       | True        |
            | EUR       | BTC       | True        |
            | LTC       | USD       | False       |
            | BTC       | USD       | False       |
            | BTC       | EUR       | False       |
            | ETH       | EUR       | False       |
            | BCH       | USD       | False       |
            | BTC       | ETH       | False       |
            | LTC       | BCH       | False       |
            | ETH       | LTC       | False       |
            | BCH       | BTC       | False       |