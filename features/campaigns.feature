# Created by andrey.p s
@campaign
Feature: Campaigns

    Scenario Outline: Check campaign
        Given User gets campaign with id: <cmp_id>
        When User passed all criteria in campaign
        Then User has campaign in the context
        When User passed conditions
        Then User gets some reward
    Examples:
        | cmp_id                           |
        | 2637afecbaa344dda8b1b1491b752f88 |

