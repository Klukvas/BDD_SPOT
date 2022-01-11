Feature: Circle
    Actions with card
    @smoke
    @circle
    Scenario Outline: Make a deposit by card
        Given User get encryption key
        And User encrypt data of his card
        When User add new card
        Then User create deposit via card
        And User has new record in operation history
        And User`s balance is changed
        And User delete his card