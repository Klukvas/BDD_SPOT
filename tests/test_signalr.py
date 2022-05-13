import time
from API.SignalR import SignalR
from pytest_bdd import scenario, then, when
import settings


@scenario(f'../features/signalr.feature', 'Check that all hubs returned a response')
def test_signalr_responses():
    pass


@when('We initialize a signalR', target_fixture='signalr_class')
def get_signalr(auth):
    token = auth(
        settings.base_user_data_email,
        settings.base_user_data_password
    )['response']
    assert 'data' in token, f"'data' key not in response"
    token = token['data']['token']
    return SignalR(token)


@then('signalR has to return response at all hubs')
def check_hub_responses(signalr_class):
    # waiting 10s before parsing signalR responses hubs
    time.sleep(10)
    try:
        response_dict = signalr_class.get_response_from_handled_hubs()
        for hub, response in response_dict.items():
            assert len(response) > 0, f'{hub} hub did not return response to {settings.signalr_email}'
    finally:
        signalr_class.close()
