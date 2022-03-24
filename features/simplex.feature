Feature: Simplex

    @test
    Scenario Outline: Make a deposit by simplex
        Given User try to make a deposit from <from_asset> to <to_asset> with amount <amount>
        Examples:
            | from_asset | to_asset   | amount |
            | USD        | ETH        | 110    |
            | USD        | XLM        | 110    |