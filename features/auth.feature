# Created by andrey.p s
@auth
Feature: Authentification
    # Enter feature description here
    auth service
    Scenario: Refresh token
        Given User logIn to account
        And User can interact with endpoints
        When User make Refresh of token
        Then User can interact with endpoint with new token
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
    @new_scenario
    Scenario Outline: Negative registration
        Given User try to registration with <email> and <password>. User get <response> with <status_code>
        Examples:
            | email             | password                                  | status_code | response                                             |
            | asd               | password1                                 | 400         | {"message":"'Email' is not a valid email address."} | #inc email
            | email@email       | password1                                 | 400         | {"message":"'Email' is not a valid email address."} | #inc email
            | empty             | password1                                 | 400         | {"message":"'Email' must not be empty. 'Email' is not a valid email address."} |
            | null              | password1                                 | 400         | {"message":"'Email' must not be empty."}            |
            | email@email.email | password                                  | 400         | {"message":"'Password' is not in the correct format."} |
            | email@email.email | 123123123                                 | 400         | {"message":"'Password' is not in the correct format."} |
            | email@email.email | 1a                                        | 400         | {"message":"'Password' must be between 8 and 31 characters. You entered 2 characters."} |
            | email@email.email | empty                                     | 400         | {"message":"'Password' must not be empty. 'Password' is not in the correct format. 'Password' must be between 8 and 31 characters. You entered 0 characters."} |
            | email@email.email | null                                      | 400         | {"message":"'Password' must not be empty."} |
            | email@email.email | $%^&*&^%                                  | 400         | {"message":"'Password' is not in the correct format."}     |
            | empty             | empty                                     | 400         | {"message":"'Email' must not be empty. 'Email' is not a valid email address. 'Password' must not be empty. 'Password' is not in the correct format. 'Password' must be between 8 and 31 characters. You entered 0 characters."} |
            | null              | null                                      | 400         | {"message":"'Email' must not be empty. 'Password' must not be empty."} |
            | email@email.email | asddddddddddddddddddddddddddfffd321       | 400         | {"message":"'Password' must be between 8 and 31 characters. You entered 35 characters."} |
    Scenario Outline: Negative authentification
        Given User try to authentification with <email> and <password>. User get <response> with <status_code>
        Examples:
            | email             | password   | status_code | response   |
            | asd281471@asdf.asd| password12 | 401         | {"message":"InvalidUserNameOrPassword"}   | #non existing user
            | email@email       | password1  | 400         | {"message":"'Email' is not a valid email address."} | #inc email
            | empty             | password1  | 400         | {"message":"'Email' must not be empty. 'Email' is not a valid email address."} |
            | null              | password1  | 400         | {"message":"'Email' must not be empty."}            |
            | email@email.email | password   | 401         | {"message":"InvalidUserNameOrPassword"} |
            | email@email.email | 123123123  | 401         | {"message":"InvalidUserNameOrPassword"} |
            | email@email.email | 1a         | 401         | {"message":"InvalidUserNameOrPassword"} |
            | email@email.email | empty      | 400         | {"message":"'Password' must not be empty."} |
            | email@email.email | null       | 400         | {"message":"'Password' must not be empty."} |
            | email@email.email | $%^&*&^%   | 401         | {"message":"InvalidUserNameOrPassword"}     |
            | empty             | empty      | 400         | {"message":"'Email' must not be empty. 'Email' is not a valid email address. 'Password' must not be empty."} |
            | null              | null       | 400         | {"message":"'Email' must not be empty. 'Password' must not be empty."} |