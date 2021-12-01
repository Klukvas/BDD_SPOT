# Created by andrey.p at 30.11.2021
Feature: Emails receive
  # Enter feature description here

  Scenario: Email confirmation
    Given User registration
    Then User has new email with code
    And User can verify email by code from mail