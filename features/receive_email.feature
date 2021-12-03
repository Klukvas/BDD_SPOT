# Created by andrey.p at 30.11.2021
Feature: Emails receive
  # Enter feature description here

  Scenario: Email confirmation
    Given User registration
    And User has new email with code
    When User can verify email by code from mail
    Then User`s email is veryfied
  
  Scenario: Success login
    Given  User has new Success login email after login

  Scenario: Transfer
    Given User send transfer
    When User has new email with appove link
    Then User approve transfer by link