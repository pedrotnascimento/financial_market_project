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
                if ohlc[i]["high"] <= ohlc[i + 1]["high"]:
                    while ohlc[i]["high"] <= ohlc[i + 1]["high"]:
                        i += 1
                        count += 1
                elif ohlc[i]["low"] >= ohlc[i + 1]["low"]:
                    while ohlc[i]["low"] >= ohlc[i + 1]["low"]:
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

        sort_count = sorted(count_dict.items(), key=lambda x: x[0])
        average_of_leg = sum([i[1] for i in sort_count]) / len(sort_count)

        rates_of_frequency = [
            (f"{sort_count[a][0]}X{sort_count[a+1][0]}", sort_count[a][1] / sort_count[a + 1][1])
            for a in range(len(sort_count) - 1)
        ]
        average_of_rate = sum([i[1] for i in rates_of_frequency]) / len(
            rates_of_frequency
        )
        if display_statistic:
            print("consequent high/low higher/lower than previous high/previous low", *sort_count)
            print("average of frequency", average_of_leg)
            print("frequency from current to next level", *rates_of_frequency)
            print("average of rate", average_of_rate)
            
        return sort_count
        std_dev = sqrt(
            sum([(a[1] - average_of_leg) ** 2 for a in sort_count]) / (len(sort_count))
        )
        # print("standard deviation", std_dev)
        # print("standard deviation Up", std_dev)
        # print("standard deviation Down", average_of_frequency-abs(average_of_frequency-std_dev))
