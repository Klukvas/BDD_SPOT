@swap
Feature: Swap
    Convert one crypto to another
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
    Scenario: Swap with amount more than balance
        Given User try to get quote with amount more than has on balance. User get an lowBalance error
    Scenario: Swap with nonexisting asset from
        Given User try to get quote with nonexisting asset from. User get an Asset do not found error
    @new_scenario
    Scenario: Swap with nonexisting asset to
        Given User try to get quote with nonexisting asset to. User get an Asset do not found error
