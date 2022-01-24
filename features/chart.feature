Feature: Charts
    @candels
    Scenario Outline: Receive chart data
        Given User send request for chart with next data: <instrument>, <period>
        Examples:
            | instrument | period   |
            | ETHUSD     | DAY      |
            | ETHUSD     | WEEK     |
            | ETHUSD     | MOUNTH   |
            | ETHUSD     | YEAR     |
            | XLMUSD     | DAY      |
            | XLMUSD     | WEEK     |
            | XLMUSD     | MOUNTH   |
            | XLMUSD     | YEAR     |
            | LTCUSD     | DAY      |
            | LTCUSD     | WEEK     |
            | LTCUSD     | MOUNTH   |
            | LTCUSD     | YEAR     |
            | BTCUSD     | DAY      |
            | BTCUSD     | WEEK     |
            | BTCUSD     | MOUNTH   |
            | BTCUSD     | YEAR     |
