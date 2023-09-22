import pandas as pd


class VolumeRateStrategy:
    def __init__(self, time_range=14, time_rate_ms=1000):
        self.time_range = time_range
        self.time_rate_ms = time_rate_ms

    def output(self, ticks_pos):
        ticks_frame = pd.DataFrame(ticks_pos)
        ticks_frame["time"] = round(ticks_frame["time_msc"] / 1000)
        ticks_frame["time_dt"] = pd.to_datetime(
            round(ticks_frame["time_msc"] / 1000), unit="s"
        )
        data = ticks_frame.groupby([ticks_frame["time_dt"]]).agg(
            volume=("volume", "sum")
        )

        y = list(map(lambda x: x, data.values))
        x = list(map(lambda x: x, data.index))
        return x, y
