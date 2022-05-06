from API.Candle import Candle
from pytest_bdd import scenario, given, parsers
import settings
import datetime


@scenario(f'../features/chart.feature', 'Receive chart data')
def test_chart_data():
    pass

@given(parsers.parse('User send request for chart with next data: {instrument}, {period}'))
def get_enc_key(instrument, period, auth):
    token = auth(
        settings.me_tests_email,
        settings.me_tests_password
    )['response']['data']['token']
    
    fromDate = int(
            (datetime.datetime.today() - datetime.timedelta(
                days=settings.chart_data[period]['dateFromDifferetn']
            )
         ).timestamp() * 1000)
    toDate = int((datetime.datetime.today() - datetime.timedelta(days = 1)).timestamp() *1000)
    
    can = Candle().get_candels(
            token,
            settings.chart_data[period]['type'],
            instrument,
            fromDate,
            toDate,
            settings.chart_data[period]['mergeCount'] 
        )
    assert type(can) == dict, f"Expected that returned dict but gets: {can}"
    assert len(can['data']) >= settings.chart_data[period]['expected_count'] - 15, f"Expected count: {settings.chart_data[period]['expected_count']} - 15. Returned: {len(can['data'])}\nurl for reproduce: {can['url']}"
    assert len(can['data']) <= settings.chart_data[period]['expected_count'] + 15, f"Expected count: {settings.chart_data[period]['expected_count']} + 15. Returned: {len(can['data'])}\nurl for reproduce: {can['url']}"
