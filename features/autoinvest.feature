Feature: Autoinvest

    Scenario Outline: create instruction (method №1) - execute it
        Given scheduleType is <scheduleType>; isFromFixed is <isFromFixed>; volume is <volume>; fromAsset is <fromAsset>; toAsset is <toAsset>
#         method 1 - /get-quote with recurringBuy - /execute quote
        When user create instruction (method 1)
        And instruction appears in DB
#        And instruction has to appear at signalR hub
        Then change execution time at DB
        And wait till instruction executes (order appears at db)
        And new log has to be in the operation history
        And new log has to be in the balance history
#        And new log has to be in backoffice
    Examples:
        | scheduleType | isFromFixed | volume  | fromAsset | toAsset |
        | 1            | true        | 0.001   | BTC       | ETH     |
        | 1            | false       | 0.001   | BTC       | ETH     |
        | 2            | true        | 0.001   | BTC       | ETH     |
        | 2            | false       | 0.001   | BTC       | ETH     |
        | 3            | true        | 0.001   | BTC       | ETH     |
        | 3            | false       | 0.001   | BTC       | ETH     |
        | 4            | true        | 0.001   | BTC       | ETH     |
        | 4            | false       | 0.001   | BTC       | ETH     |
#
    Scenario Outline: create instruction (method №2) - execute it
        Given scheduleType is <scheduleType>; isFromFixed is <isFromFixed>; volume is <volume>; fromAsset is <fromAsset>; toAsset is <toAsset>
#         method 1 - /get-quote with recurringBuy - /execute quote
        When user create instruction (method 2)
        And instruction appears in DB
#        And instruction has to appear at signalR hub
        Then change execution time at DB
        And wait till instruction executes (order appears at db)
        And new log has to be in the operation history
        And new log has to be in the balance history
#        And new log has to be in backoffice
    Examples:
        | scheduleType | isFromFixed | volume  | fromAsset | toAsset |
        | 1            | true        | 0.001   | BTC       | ETH     |
        | 1            | false       | 0.001   | BTC       | ETH     |
        | 2            | true        | 0.001   | BTC       | ETH     |
        | 2            | false       | 0.001   | BTC       | ETH     |
        | 3            | true        | 0.001   | BTC       | ETH     |
        | 3            | false       | 0.001   | BTC       | ETH     |
        | 4            | true        | 0.001   | BTC       | ETH     |
        | 4            | false       | 0.001   | BTC       | ETH     |

    Scenario Outline: create-switch-execute
        Given scheduleType is <scheduleType>; isFromFixed is <isFromFixed>; volume is <volume>; fromAsset is <fromAsset>; toAsset is <toAsset>
        When user create instruction (method 1)
        And instruction appears in DB
#        And instruction has to appear at signalR hub
        Then switch off instruction
        And instruction status changes at DB (switch off)
        And change execution time at DB
        And wait 2 minutes and check that instruction did not execute
    Examples:
        | scheduleType | isFromFixed | volume  | fromAsset | toAsset |
        | 1            | true        | 0.001   | BTC       | ETH     |


    Scenario Outline: create-delete-execute
        Given scheduleType is <scheduleType>; isFromFixed is <isFromFixed>; volume is <volume>; fromAsset is <fromAsset>; toAsset is <toAsset>
        When user create instruction (method 1)
        And instruction appears in DB
#        And instruction has to appear at signalR hub
        Then delete instruction
        And instruction status changes at DB (delete)
        And change execution time at DB
        And wait 2 minutes and check that instruction did not execute
    Examples:
        | scheduleType | isFromFixed | volume  | fromAsset | toAsset |
        | 1            | true        | 0.001   | BTC       | ETH     |

