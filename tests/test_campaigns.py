from pytest_bdd import scenario, given, when, parsers, then
from GRPC.Сampaigns.campaigns import get_campaign_by_id
from API.CampaignsParser import CampaignWorker


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

    return {'campaign_worker': cmp_obj}


@when('User passed all criteria in campaign')
def pass_criteria(get_campaign):
    all_criteria = get_campaign['campaign_worker'].get_criteria_steps()
    for crt_name, crt_val in all_criteria.items():
        if crt_name == "KYC":
            pass
        elif crt_name == 'HasReferrer':
            pass
        else:
            raise Exception(f"Unknown criteria of campaign: {crt_name}")

# {'KYC': ['KycDepositPassed', 'KycTradePassed', 'KycWithdrawalPassed'], 'HasReferrer': True}


@then("User has campaign in the context")
def check_user_context():
    pass


@when("User passed conditions")
def pass_condition():
    pass


@then('User gets some reward')
def check_rewards():
    pass
