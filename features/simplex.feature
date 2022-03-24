Feature: Simplex

    Scenario Outline: Make a deposit by simplex
        Given User try to make a deposit from <from_asset> to <to_asset> with amount <amount>
        Examples:
            | from_asset | to_asset   | amount |
            | USD        | ETH        | 110    |
            | USD        | XLM        | 110    |
    
    Scenario Outline: Make a deposit by simplex with non exists asset from
        Given User try to make a deposit by simplex with asset to <to_asset>, amount <amount>,  non exists asset from
        Examples:
            | to_asset   | amount |
            | ETH        | 110    |
    
    Scenario Outline: Make a deposit by simplex with non exists asset to
        Given User try to make a deposit by simplex with asset from <from_asset>, amount <amount>,  non exists asset to
        Examples:
            | from_asset | amount |
            | USD        | 110    |
    
    Scenario Outline: Make a deposit by simplex with amount less than minimum
        Given User try to make a deposit by simplex with asset to <to_asset>, asset from <from_asset> and amount <amount>
        Examples:
            | from_asset | to_asset | amount |
            | USD        | XLM      |    1   |
       
    Scenario Outline: Make a deposit by simplex with amount more than maximum
        Given User try to make a deposit by simplex with asset to <to_asset>, asset from <from_asset> and amount more than maximum <amount>
        Examples:
            | from_asset | to_asset | amount   |
            | USD        | XLM      | 10100101 |