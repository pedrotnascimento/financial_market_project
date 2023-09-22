from my_jupyter.indicator.indicator_base import IndicatorBase


class ConsequentLimitsCounterIndicator(IndicatorBase):
    def __init__(self, period):
        super().__init__(period)

    def output(self, ohlc):
        count = 0
        i = 0
        try:
            while i < len(ohlc) - 3:
                if ohlc[i]["low"] < ohlc[i + 1]["low"]:
                    while ohlc[i]["low"] <= ohlc[i + 1]["low"]:
                        i += 1
                        count -=1
                elif ohlc[i]["high"] > ohlc[i + 1]["high"]:
                    while ohlc[i]["high"] >= ohlc[i + 1]["high"]:
                        i += 1
                        count += 1
                i += 1
            return count
        except Exception as e:
            print(i, len(ohlc))
            print(e)
