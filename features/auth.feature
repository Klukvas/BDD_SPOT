# Created by andrey.p s
@auth
Feature: Authentification
    # Enter feature description here
    auth service

    Scenario: Blocker after password change
        Given User change password
        Then User can not make a transfer
        And  User can not make a withdrawal

    Scenario Outline: Blocker after incorrect password
        Given User input incorrect password for <repeat_count> times
        Then User has blocker for login
        Examples:
            | repeat_count |
            | 5            |

    Scenario: Refresh token
        Given User logIn to his account
        And User can interact with endpoints
        When User make Refresh of token
        Then User can interact with endpoint with new token
    @email_test
    Scenario: Change password
        Given User change his password
        When User can not logIn by old password
        Then User can logIn by new password

    Scenario: LogOut
        Given User logIn to account
        And User can interact with any endpoint
        When User make LogOut
        Then User can not interact with endpoint with old token
    Scenario Outline: Negative registration
        Given User try to registration with <email> and <password>. User get <response> with <status_code>
        Examples:
            | email             | password                                  | status_code | response                                             |
            | asd               | password1                                 | 400         | 'Email' is not a valid email address. | #inc email
            | email@email       | password1                                 | 400         | 'Email' is not a valid email address. | #inc email
            | empty             | password1                                 | 400         | 'Email' must not be empty. 'Email' is not a valid email address. |
            | null              | password1                                 | 400         | 'Email' must not be empty.            |
            | email@email.email | password                                  | 400         | 'Password' is not in the correct format. |
            | email@email.email | 123123123                                 | 400         | 'Password' is not in the correct format. |
            | email@email.email | 1a                                        | 400         | 'Password' must be between 8 and 31 characters. You entered 2 characters. |
            | email@email.email | empty                                     | 400         | 'Password' must not be empty. 'Password' is not in the correct format. 'Password' must be between 8 and 31 characters. You entered 0 characters. |
            | email@email.email | null                                      | 400         | 'Password' must not be empty. |
            | email@email.email | $%^&*&^%                                  | 400         | 'Password' is not in the correct format.     |
            | empty             | empty                                     | 400         | 'Email' must not be empty. 'Email' is not a valid email address. 'Password' must not be empty. 'Password' is not in the correct format. 'Password' must be between 8 and 31 characters. You entered 0 characters. |
            | null              | null                                      | 400         | 'Email' must not be empty. 'Password' must not be empty. |
            | email@email.email | asddddddddddddddddddddddddddfffd321       | 400         | 'Password' must be between 8 and 31 characters. You entered 35 characters. |
    Scenario Outline: Negative authentification
        Given User try to authentification with <email> and <password>. User get <response> with <status_code>
        Examples:
            | email             | password   | status_code | response   |
            | asd281471@asdf.asd| password12 | 401         | InvalidUserNameOrPassword   | #non existing user
            | email@email       | password1  | 400         | 'Email' is not a valid email address. | #inc email
            | empty             | password1  | 400         | 'Email' must not be empty. 'Email' is not a valid email address. |
            | null              | password1  | 400         | 'Email' must not be empty.            |
            | email@email.email | password   | 401         | InvalidUserNameOrPassword |
            | email@email.email | 123123123  | 401         | InvalidUserNameOrPassword |
            | email@email.email | 1a         | 401         | InvalidUserNameOrPassword |
            | email@email.email | empty      | 400         | 'Password' must not be empty. |
            | email@email.email | null       | 400         | 'Password' must not be empty. |
            | email@email.email | $%^&*&^%   | 401         | InvalidUserNameOrPassword     |
            | empty             | empty      | 400         | 'Email' must not be empty. 'Email' is not a valid email address. 'Password' must not be empty. |
            | null              | null       | 400         | 'Email' must not be empty. 'Password' must not be empty. |
    Scenario Outline: Negative change password
        Given User try to change password from <password_old> to <password_new>. User get <response> with <status_code>
        Examples:
            | password_old | password_new | status_code | response   |
            | default      | password     | 400         | 'New Password' is not in the correct format.   | #non existing user
            | default      | 23456789     | 400         | 'New Password' is not in the correct format.   | #non existing user
            | default      | #$%^&^%$     | 400         | 'New Password' is not in the correct format.   | #non existing user
            | default      | jk           | 400         | 'New Password' is not in the correct format. 'New Password' must be between 8 and 31 characters. You entered 2 characters.   | #non existing user
            | default      | 1232         | 400         | 'New Password' is not in the correct format. 'New Password' must be between 8 and 31 characters. You entered 4 characters.   | #non existing user
            | testpa1      | password1    | 400         | OldPasswordDoesntMatch   | #non existing user