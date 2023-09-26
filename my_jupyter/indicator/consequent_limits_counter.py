from my_jupyter.indicator.indicator_base import IndicatorBase


class ConsequentLimitsCounterIndicator(IndicatorBase):
    def __init__(self, period):
        super().__init__(period + 1)
        self.period = period

    def output(self, ohlc):
        count = 0
        i = 0
        previous_candles = 1
        ohlc_previous = ohlc[previous_candles:]
        try:
            ohlc_limited_len = len(ohlc_previous[: self.period])

            if ohlc_previous["high"][i] < ohlc_previous["high"][i + 1]:
                count -= 1
                while (
                    i < ohlc_limited_len - 1
                    and ohlc_previous["high"][i] <= ohlc_previous["high"][i + 1]
                ):
                    i += 1
                    count -= 1
            elif ohlc_previous["low"][i] > ohlc_previous["low"][i + 1]:
                count += 1
                while (
                    i < ohlc_limited_len - 1
                    and ohlc_previous["low"][i] >= ohlc_previous["low"][i + 1]
                ):
                    i += 1
                    count += 1
            print(f"counting: {count}")
            return count
        except Exception as e:
            print(i, len(ohlc))
            print(e)
