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

  Scenario Outline: Transfer(waiting for user)
    Given User send transfer with asset: <asset>, to phone <phone>
    When User has new email with appove link
    Then User approve transfer by link
    Examples:
      | asset | phone         |
      | LTC   | +111111123123 |

  Scenario Outline: Internal withdrawal
    Given User send withdrawal request wiht asset: <asset>, to address: <address>
    When User has new email with appove withdwal link
    Then User approve withdrawal by link
    Examples:
        | asset |  address                             |
        | LTC   |  QVTCAaqX8UUk8kf3VY6FRdicFkBuoDQ78P  |


  Scenario: Password Recovery
    Given User passed registration
    When User send request to forgot password endpoint
    Then User get new email with token
    And User change password using token from email
    And User can not auth with old password
    And User can auth with new password