# Created by andrey.p at 30.11.2021
@emails
Feature: Emails receive
  # Enter feature description here
  @email_test
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
    When User has new email with appove withdwal link with <feeAmount> and <feeAsset>
    Then User approve withdrawal by link
    Examples:
        | asset |  address                             | feeAsset | feeAmount |
        | LTC   |  tltc1qz3qgnmt9fyd77rv4f0jh3aer0yu6mlgje7jx0a  | LTC      | 0         |


  Scenario: Password Recovery
    Given User send request to forgot password endpoint
    Then User get new email with code
    And User change password using code from email
    And User can not auth with old password
    And User can auth with new password
    And User comeback old password
  Scenario: ReRegistration
    Given  ReRegistration mail on inbox after existing user pass registration
  
  # Scenario: Success withdrawal or transfer && deposit
  #   #email must be with domen @mailforspam and existing in the system
  #   #address_phone field: if you fill the field with the phone number(+380, +4521 ...)
  #   #the scenario will make a transfer by phone, or if you fill  with  asset address 
  #   #scenario will make a withdrawal
  #   Given User send withdrawal/transfer with asset: <asset>, to address/phone <address_phone>
  #   When User approve withdrawal/transfer by restApi
  #   Then User has new success withdrawal email
  #   And Receive user with email <email> has new success deposit email
  #   Examples:
  #     | asset |  address_phone                                 | email          |
  #     | BTC   |  tb1q8gw6s94t43tz2rkpy4yerekkuuw6whrt5rhjar    | basereceiver1  |
  #     | ETH   |  0x316599B1fEe6b55CFd2c39FB85d3b9b4eED31567    | basereceiver1  |
  #     | LTC   |  +3803803803803801                             | basereceiver1  |
  #     | BCH   |  +3803803803803801                             | basereceiver1  |
      
