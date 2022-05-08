import uuid
from pytest_bdd import scenario, given, when, parsers, then
import settings
from GRPC.Kyc import kyc
from API.CampaignsParser import CampaignWorker
from API.Auth import Auth
from API.Swap import Swap
from GRPC.Сampaigns import campaigns
import json
from GRPC.ChangeBalance import change_balance


@scenario(f'../features/campaigns.feature', 'Check campaign')
def test_campaigns():
    pass


@given(parsers.parse("User gets campaign with id: {cmp_id}"), target_fixture='get_campaign')
def check_campaign(cmp_id):
    cmp_obj = CampaignWorker()
    cmp = cmp_obj.find_campaign_by_id(cmp_id)
    assert len(cmp) == 1, \
        f"Expected that campaign with id: {cmp_id} would be found"
    cmp = cmp[0]
    assert cmp['Status'] == 'Active', \
        f"Expected that status of campaign with id: {cmp_id} will be 'Active'. But returned: {cmp}"
    assert cmp['IsEnabled'], f"Expected that campaign with id: {cmp_id} will be enabled"

    return {'campaign_worker': cmp_obj, 'campaign_id': cmp_id}


@when('User passed all criteria in campaign', target_fixture='criteria_passed')
def pass_criteria(get_campaign, register):
    new_user_registered = False
    all_criteria = get_campaign['campaign_worker'].get_criteria_steps()
    if 'HasReferrer' in all_criteria.keys():
        email = 'test_campaign' + str(uuid.uuid4()) + '@mailinator.com'
        token = Auth(email, settings.me_tests_password).register(
            email=email,
            password=settings.me_tests_password,
            referralCode=settings.me_tests_referral_code
        )['response']['data']['token']
        new_user_registered = True
    if 'KYC' in all_criteria.keys():
        if not new_user_registered:
            email = 'test_campaign' + str(uuid.uuid4()) + '@mailinator.com'
            token = register(
                email=email,
                password=settings.me_tests_password
            )['token']
        client_id = Auth(email, settings.me_tests_password).who(token)
        assert 'clientId' in client_id['response'].keys()
        client_id = client_id['response']['clientId']
        deposit_status = 2 if 'KycDepositPassed' in all_criteria['KYC'] else 0
        trade_status = 2 if 'KycTradePassed' in all_criteria['KYC'] else 0
        withdrawal_status = 2 if 'KycWithdrawalPassed' in all_criteria['KYC'] else 0
        result = kyc.set_kys_allowed(
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
    except Exception as err:
        raise Exception(f"""
            Some error with getting ids of context campaigns. 
            Response from context grpc: {campaign_context}.
            Error: {err}
        """)
    assert criteria_passed['campaign_id'] in all_cmp_ids


@when("User passed conditions")
def pass_condition(criteria_passed, auth):
    conditions = criteria_passed['campaign_parser_obj'].get_condition_steps()
    for condition in conditions.items():
        if condition[0] == 'KYCCondition':
            deposit_status: int = 2 if condition['Steps']['CheckDepositKyc'] else 0
            trade_status: int = 2 if condition['Steps']['CheckTradeKyc'] else 0
            withdrawal_status: int = 2 if condition['Steps']['CheckWithdrawalKyc'] else 0
            result = kyc.set_kys_allowed(
                criteria_passed['client_id'],
                DepositStatus=deposit_status,
                TradeStatus=trade_status,
                WithdrawalStatus=withdrawal_status
            )
            assert result
        elif condition[0] == 'DepositCondition':
            pass
        elif condition[0] == 'TradeCondition':
            asset: str = condition['Steps']['TradeAsset']
            amount: int = int(condition['Steps']['TradeAmountInSelectedAsset'])
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
                settings.me_tests_password
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
        elif condition[0] == 'ConditionsCondition':
            pass
    """
    {
    "KYCCondition":{
        "weight":1,
        "Steps":{
            "CheckWithdrawalKyc":"",
            "CheckTradeKyc":"True",
            "CheckDepositKyc":"True"
        },
        "Rewards":{
            "ReferrerPaymentAbsolute":{
                "asset":"LTC",
                "amount":"10"
            },
            "ClientPaymentAbsolute":{
                "asset":"XLM",
                "amount":"1010"
            },
            "FeeShareAssignment":{
                "feeShareGroup":"USDC22"
            }
        }
    },
    "DepositCondition":{
        "weight":2,
        "Steps":{
            "DepositAsset":"USD",
            "DepositAmountInSelectedAsset":"100"
        },
        "Rewards":{
            
        }
    },
    "TradeCondition":{
        "weight":3,
        "Steps":{
            "TradeAsset":"USD",
            "TradeAmountInSelectedAsset":"100"
        },
        "Rewards":{
            
        }
    },
    "ConditionsCondition":{
        "weight":99,
        "Steps":{
            "ConditionsList":"ac37b267578a428798c900535fe7192d",
            "AllowExpired":""
        },
        "Rewards":{
            
        }
    }
}
    """


@then('User gets some reward')
def check_rewards():
    pass
