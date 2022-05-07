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
        | 7d132d2ac7c34b7ca787db703c9b8ee2 |

