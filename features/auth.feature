Feature: Auth
    @auth
    Scenario: Change password
        Given User pass the registration
        When User change his password
        Then User can not logIn by old password
        And User can logIn by new password

    Scenario: LogOut
        Given User logIn to account
        And User can interact with endpoints
        When User make LogOut
        Then User can not interact with endpoint with old token

    Scenario: Refresh token
        Given User logIn to account
        And User can interact with endpoints
        When User make Refresh of token
        Then User can not interact with endpoint with old token and can with new
