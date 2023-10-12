from math import sqrt


class CountConsequentBarsReversal:
    def __init__(self, period=99999):
        self.period = period

    def output(self, ohlc, display_statistic=False):
        count_dict = {}
        count = 0
        i = 9
        try:
            while i < len(ohlc) - 3:
                if ohlc[i]["close"] < ohlc[i]["open"]:
                    down = False
                    close_down = ohlc[i]["close"] < ohlc[i]["open"]
                    while close_down:
                        i += 1
                        count += 1
                        close_down = (
                            ohlc[i]["close"] <= ohlc[i]["open"]
                            if down
                            else ohlc[i]["close"] >= ohlc[i]["open"]
                        )
                        down = not down

                elif ohlc[i]["close"] > ohlc[i]["open"]:
                    up = False
                    close_up = ohlc[i]["close"] > ohlc[i]["open"]
                    while close_up:
                        i += 1
                        count += 1
                        close_up = (
                            ohlc[i]["close"] >= ohlc[i]["open"]
                            if up
                            else ohlc[i]["close"] <= ohlc[i]["open"]
                        )
                        up = not up
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
            for a in range(len(sort_counting)-1)
        ]
        average_of_rate = sum([i[1] for i in rates_of_frequency]) / len(
            rates_of_frequency
        )
        average_of_leg = sum([i[1] for i in sort_counting]) / len(sort_counting)
        sum_all = sum([i[1] for i in sort_counting])
        probababilities  = [ (i, j/sum_all) for i,j in sort_counting]


        if display_statistic:
            print(f"generate statistic for bars reversal in {self.period} bar")
            print("probabilities", probababilities)
            print("quantity of consequent reversals", *sort_counting)
            print("rate from current level to next of consequent reversals", *rates_of_frequency)
            print("average of rate", average_of_rate)
        return sort_counting

        std_dev = sqrt(
            sum([(a[1] - average_of_leg) ** 2 for a in sort_counting])
            / (len(sort_counting))
        )
