import uuid
from pytest_bdd import scenario, given, when, parsers, then
import settings
from GRPC.Kyc import kyc
from GRPC.PersonalData import personal_data
from API.CampaignsParser import CampaignWorker
from API.Auth import Auth
from API.Swap import Swap
from API.Verify import Verify
from API.Circle import Circle
from GRPC.Сampaigns import campaigns
import json
from GRPC.ChangeBalance import change_balance
from time import sleep
from random import randint
@scenario(f'../features/campaigns.feature', 'Check campaign')
def test_campaigns():
    pass


@given(parsers.parse("User gets campaign with id: {cmp_id}"), target_fixture='get_campaign')
def check_campaign(cmp_id):
    cmp_obj = CampaignWorker()
    cmp = cmp_obj.find_campaign_by_id(cmp_id)
    assert cmp['Status'] == 'Active', \
        f"Expected that status of campaign with id: {cmp_id} will be 'Active'. But returned: {cmp}"
    assert cmp['IsEnabled'], f"Expected that campaign with id: {cmp_id} will be enabled"

    return {'campaign_worker': cmp_obj, 'campaign_id': cmp_id}


@when('User passed all criteria in campaign', target_fixture='criteria_passed')
def pass_criteria(get_campaign, register):
    all_criteria = get_campaign['campaign_worker'].get_criteria_steps()
    email = 'test_campaign' + str(uuid.uuid4()) + '@mailinator.com'
    print(email)
    if 'HasReferrer' in all_criteria.keys():
        token = Auth(email, settings.base_user_data_password).register(
            email=email,
            password=settings.base_user_data_password,
            referralCode=settings.base_user_data_referral_code
        )['response']['data']['token']
        Verify().verify_email(token, "000000")
    else:
        token = register(
            email=email,
            password=settings.base_user_data_password
        )['token']
    client_id = Auth(email, settings.base_user_data_password).who(token)
    assert 'clientId' in client_id['response'].keys()
    client_id = client_id['response']['clientId']
    change_pd_resp = personal_data.change_personal_data(
        client_id,
        'PL'
    )
    assert change_pd_resp == True
    phone = str(randint(10000000, 99999999))
    set_phone_response = Verify().set_phone_request(
        token,
        phone
    )
    assert set_phone_response['response']['result'] == 'OK'
    verify_phone = Verify().verify_phone(token,
        phone)
    assert verify_phone['response']['result'] == 'OK'


    if 'KYC' in all_criteria.keys():
        deposit_status = 2 if 'KycDepositPassed' in all_criteria['KYC'] else 0
        trade_status = 2 if 'KycTradePassed' in all_criteria['KYC'] else 0
        withdrawal_status = 2 if 'KycWithdrawalPassed' in all_criteria['KYC'] else 0
        result = kyc.set_kys_status(
            client_id,
            DepositStatus=deposit_status,
            TradeStatus=trade_status,
            WithdrawalStatus=withdrawal_status
        )
        assert result
    return {
        'registered_email': email,
        "client_id": client_id,
        'campaign_id': get_campaign['campaign_id'],
        "campaign_parser_obj": get_campaign['campaign_worker']}


# {'KYC': ['KycDepositPassed', 'KycTradePassed', 'KycWithdrawalPassed'], 'HasReferrer': True}


@then("User has campaign in the context")
def check_user_context(criteria_passed):
    count = 0
    while True:
        campaign_context = json.loads(
            campaigns.get_client_context(
                criteria_passed['client_id']
            )
        )
        try:
            all_cmp_ids = [
                campaign['CampaignId']
                for campaign in campaign_context['Contexts']
            ]
        except KeyError:
            all_cmp_ids = []
        except Exception as err:
            raise Exception(f"""
                Some error with getting ids of context campaigns. 
                Response from context grpc: {campaign_context}.
                Error: {err}
            """)
        if criteria_passed['campaign_id'] not in all_cmp_ids and count < 15:
            sleep(15)
        elif criteria_passed['campaign_id'] not in all_cmp_ids and count >= 15:
            assert criteria_passed['campaign_id'] in all_cmp_ids
        else:
            return


@when("User passed conditions", target_fixture='pass_condition')
def pass_condition(criteria_passed, auth):
    passed_conditions = []
    conditions = criteria_passed['campaign_parser_obj'].get_condition_steps()
    if len(conditions.keys()):
        for condition in conditions.items():
            if condition[0] == 'KYCCondition':
                deposit_status: int = 2 if condition[1]['Steps']['CheckDepositKyc'] else 0
                trade_status: int = 2 if condition[1]['Steps']['CheckTradeKyc'] else 0
                withdrawal_status: int = 2 if condition[1]['Steps']['CheckWithdrawalKyc'] else 0
                result = kyc.set_kys_status(
                    criteria_passed['client_id'],
                    DepositStatus=deposit_status,
                    TradeStatus=trade_status,
                    WithdrawalStatus=withdrawal_status
                )
                assert result
                passed_conditions.append(conditions['KYCCondition']['Id'])
                conditions['KYCCondition']['Passed'] = True
            elif condition[0] == 'DepositCondition':
                if condition[1]['Steps']['DepositAsset'] == 'USD':
                    token = auth(
                        criteria_passed['registered_email'],
                        settings.base_user_data_password
                    )['response']
                    assert 'data' in token.keys(), \
                        f"Expected that 'data' key will be in response. But response is: {token}"
                    token = token['data']['token']
                    uid = str(uuid.uuid4())
                    amount: int = int(condition[1]['Steps']['DepositAmountInSelectedAsset'])
                    amount: int = int(amount + ((amount * 15) / 100))  # take 15% more
                    Circle().create_fast_deposit(
                        token,
                        uid,
                        condition[1]['Steps']['DepositAsset'],
                        amount
                    )
                    conditions['DepositCondition']['Passed'] = True
                    passed_conditions.append(conditions['DepositCondition']['Id'])
            elif condition[0] == 'TradeCondition':
                asset: str = condition[1]['Steps']['TradeAsset']
                amount: int = int(condition[1]['Steps']['TradeAmountInSelectedAsset'])
                amount: int = int(amount + ((amount * 15) / 100))  # take 15% more
                cb_result = change_balance.changeBalance(
                    clientId=criteria_passed['client_id'],
                    amount=amount,
                    walletId=f"SP-{criteria_passed['client_id']}",
                    asset=asset
                )
                assert cb_result
                token = auth(
                    criteria_passed['registered_email'],
                    settings.base_user_data_password
                )['response']
                assert 'data' in token.keys(), \
                    f"Expected that 'data' key will be in response. But response is: {token}"
                token = token['data']
                swap_obj = Swap()
                quote = swap_obj.get_quote(
                    token=token,
                    _from=asset,
                    to='USD' if asset != 'USD' else 'EUR',
                    fromToVol=amount,
                    fix=True
                )['response']
                assert 'data' in quote.keys(), \
                    f"Expected that 'data' key will be in response. But response is: {quote}"
                quote = quote['data']
                exec_quote = swap_obj.execute_quote(
                    token=token,
                    body=quote
                )['response']
                assert 'data' in exec_quote.keys(), \
                    f"Expected that 'data' key will be in response. But response is: {exec_quote}"
                conditions['TradeCondition']['Passed'] = True
                passed_conditions.append(conditions['TradeCondition']['Id'])
            elif condition[0] == 'ConditionsCondition':
                conditions_list = str(condition[1]['Steps']['ConditionsList']).split(',')
                if all([
                    condition_condition in passed_conditions
                    for condition_condition in conditions_list
                ]):
                    conditions['ConditionsCondition']['Passed'] = True
    return conditions

    """
    {
  'DepositCondition': {
    'weight': 2,
    'Steps': {
      'DepositAmountInSelectedAsset': '100',
      'DepositAsset': 'USD'
    },
    'Id': '5dfe531d69454df1a9db2eae43fed0e9',
    'Passed': False,
    'Rewards': {
      
    }
  },
  'TradeCondition': {
    'weight': 3,
    'Steps': {
      'TradeAmountInSelectedAsset': '100',
      'TradeAsset': 'USD'
    },
    'Id': 'ac37b267578a428798c900535fe7192d',
    'Passed': False,
    'Rewards': {
      
    }
  },
  'ConditionsCondition': {
    'weight': 99,
    'Steps': {
      'ConditionsList': 'ac37b267578a428798c900535fe7192d',
      'AllowExpired': ''
    },
    'Id': '4320bd33093e4322b81afef04fd67d7e',
    'Passed': False,
    'Rewards': {
      
    }
  },
  'KYCCondition': {
    'weight': 1,
    'Steps': {
      'CheckTradeKyc': 'True',
      'CheckDepositKyc': 'True',
      'CheckWithdrawalKyc': ''
    },
    'Id': 'b94d6334714947eaa6e2b2d8b741d722',
    'Passed': False,
    'Rewards': {
      'ReferrerPaymentAbsolute': {
        'asset': 'LTC',
        'amount': '10'
      },
      'ClientPaymentAbsolute': {
        'amount': '1010',
        'asset': 'XLM'
      },
      'FeeShareAssignment': {
        'feeShareGroup': 'USDC22'
      }
    }
  }
}
    """


@then('User gets some reward')
def check_rewards(pass_condition, criteria_passed, auth, find_record_in_op):
    if len(pass_condition.keys()):
        for condition_name, condition_value in pass_condition.items():
            if condition_value['Passed'] and len(condition_value['Rewards']):
                for reward_name, reward_value in condition_value['Rewards'].items():
                    if reward_name == 'ReferrerPaymentAbsolute':
                        token = auth(
                            settings.base_user_data_email,
                            settings.base_user_data_password
                        )['response']
                        assert 'data' in token.keys(), \
                            f"Expected that 'data' key will be in response. But response is: {token}"
                        reward_to_referrer = find_record_in_op(
                            token=token['data']['token'],
                            search_by={"balanceChange": reward_value['amount'], "operationType": 11},
                            asset=reward_value['asset'],
                            time_compare=65,
                        )
                        assert reward_to_referrer, \
                            f"""
                                Can not find 'ReferrerPaymentAbsolute' reward for user: {settings.base_user_data_email}
                                Campaign id: {criteria_passed['campaign_id']}
                                Refferal: {criteria_passed['client_id']}
                                Expected record in operation history: 
                                {"balanceChange": {reward_value['amount']}, "operationType": 11}
                                asset: {reward_value['asset']}
                            """
                    elif reward_name == 'ClientPaymentAbsolute':
                        token = auth(
                            criteria_passed['registered_email'],
                            settings.base_user_data_password
                        )['response']
                        assert 'data' in token.keys(), \
                            f"Expected that 'data' key will be in response. But response is: {token}"
                        reward_to_client = find_record_in_op(
                            token=token['data']['token'],
                            search_by={"balanceChange": reward_value['amount'], "operationType": 11},
                            asset=reward_value['asset'],
                            time_compare=100,
                            research_count=15,
                            sleep_for=20
                        )
                        assert reward_to_client, \
                            f"""
                            Can not find 'ClientPaymentAbsolute' reward for user: {criteria_passed['client_id']}
                            Campaign id: {criteria_passed['campaign_id']}
                            Expected record in operation history: 
                            "balanceChange": {reward_value['amount']}, "operationType": 11
                            asset: {reward_value['asset']}
                            """
                    elif reward_name == 'FeeShareAssignment':
                        pass
