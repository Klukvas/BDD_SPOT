Feature: Circle
    Actions with card

    Scenario Outline: Make a deposit by card
        Given User get encryption key
        And User encrypt data of his card
        When User add new card
        Then User gets his card
        And User create payment via card
        And Users`s balance are changed
        And User delete his card