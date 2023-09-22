from math import sqrt


class CountConsequentBarsReversal:
    def __init__(self, period=99999):
        self.period = period

    def output(self, ohlc, display_statistic=False):
        count = 0
        count_dict = {}
        i = 0
        try:
            while i < len(ohlc) - 3:
                if ohlc[i]["close"] < ohlc[i]["open"]:
                    while ohlc[i]["close"] <= ohlc[i]["open"]:
                        i += 1
                        count += 1
                elif ohlc[i]["close"] > ohlc[i]["open"]:
                    while ohlc[i]["close"] >= ohlc[i]["open"]:
                        i += 1
                        count += 1
                i += 1

                if count not in count_dict:
                    count_dict[count] = 1
                else:
                    count_dict[count] += 1
                count = 0
        except Exception as e:
            print(i, len(ohlc))
            print(e)

        sort_counting = sorted(count_dict.items(), key=lambda x: x[0])

        rates_of_frequency = [
            (
                f"{sort_counting[a][0]}X{sort_counting[a+1][0]}",
                sort_counting[a][1] / sort_counting[a + 1][1],
            )
            for a in range(len(sort_counting) - 1)
        ]
        average_of_rate = sum([i[1] for i in rates_of_frequency]) / len(
            rates_of_frequency
        )
        average_of_closing_bars = sum([i[1] for i in sort_counting]) / len(
            sort_counting
        )

        if display_statistic:
            print("quantity of consequent closing bars", *sort_counting)
            print("average of consequent closing bars", average_of_closing_bars)
            print("rate from current to next quantity of bars" * rates_of_frequency)
            print("average of rate", average_of_rate)
        return sort_counting

        std_dev = sqrt(
            sum([(a[1] - average_of_closing_bars) ** 2 for a in sort_counting])
            / (len(sort_counting))
        )
        # print("standard deviation", std_dev)
        # print("standard deviation Up", std_dev)
        # print("standard deviation Down", average_of_frequency-abs(average_of_frequency-std_dev))
