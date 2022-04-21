Feature: Autoinvest

    Scenario Outline: create instruction (method №1) - execute it
        Given scheduleType is <scheduleType>; isFromFixed is <isFromFixed>; volume is <volume>; fromAsset is <fromAsset>; toAsset is <toAsset>
        # method 1 - /get-quote with recurringBuy - /execute quote
        When user create instruction (method 1)
        And instruction appears in DB
#        And instruction has to appear at signalR hub
        Then change execution time at DB
        And wait till instruction executes
        And order appears in DB
        And balance has to be changed
        And new log has to be in backoffice
        And new log has to be in operation history
    Examples:
        | scheduleType | isFromFixed | volume | fromAsset | toAsset |
        | 1            | true        | 0.01   | BTC       | ETH     |
        | 2            | false       | 0.01   | BTC       | ETH     |
        | 3            | true        | 0.01   | BTC       | ETH     |
        | 4            | false       | 0.01   | BTC       | ETH     |

#    Scenario: create method №2 -execute
#        When user create instruction (method 2)
#
#    Scenario: create-switch-execute
#        Given
#
#    Scenario: create-delete-execute
#        Given
#