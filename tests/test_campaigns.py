import uuid
from pytest_bdd import scenario, given, when, parsers, then
import settings
from GRPC.Kyc import kyc
from API.CampaignsParser import CampaignWorker
from API.Auth import Auth
from GRPC.Сampaigns import campaigns
import json

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
    return {'registered_email': email, "client_id": client_id, 'campaign_id': get_campaign['campaign_id']}

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
def pass_condition():
    pass


@then('User gets some reward')
def check_rewards():
    pass
