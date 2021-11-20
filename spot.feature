Feature: Spot
    Platform where u can convert, hold ur crypto

    Scenario: Make a swap

        Given  User logIn to account
        And Some crypto on balance
        When User gets 1 step swap quote
        And User execute quote
        Then User has new record in operation history
        # And User has new record in balance history
        And User`s balance is changed

        