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
                    price_first = ohlc[i]["high"]
                    while ohlc[i]["close"] <= ohlc[i]["open"]:
                        i += 1
                        count += 1
                    price_last = ohlc[i]["low"]
                elif ohlc[i]["close"] > ohlc[i]["open"]:
                    price_first = ohlc[i]["low"]
                    while ohlc[i]["close"] >= ohlc[i]["open"]:
                        i += 1
                        count += 1
                    price_last = ohlc[i]["high"]
                i += 1
                if count == 0:
                    continue

                diff = abs(price_last - price_first)
                if count not in count_dict:
                    count_dict[count] = [diff]
                else:
                    count_dict[count].append(diff)
                count = 0
        except Exception as e:
            print(i, len(ohlc))
            print(e)

        dict_avg = {}
        from math import sqrt

        for i in count_dict:
            av = sum(count_dict[i]) / len(count_dict[i])
            vals = count_dict[i]

            dict_avg[i] = {
                "avg": av,
                "std": sqrt(sum([(j - av) ** 2 for j in vals]) / len(vals)),
                "qnt": len(vals),
            }

        for i in dict_avg:
            items = dict_avg.items()
            below = list(filter(lambda x: x[0] < i, items))
            above = list(filter(lambda x: x[0] >= i, items))
            below_sum = sum([j[1]["qnt"] for j in below])
            above_sum = sum([j[1]["qnt"] for j in above])
            dict_avg[i]["prob"] = above_sum / (below_sum + above_sum)

        sort_counting = sorted(dict_avg.items(), key=lambda x: x[0])
        rates_of_frequency = [
            (
                f"{sort_counting[a][0]}X{sort_counting[a+1][0]}",
                sort_counting[a][1]["avg"] / sort_counting[a + 1][1]["avg"],
            )
            for a in range(len(sort_counting) - 1)
        ]
        average_of_rate = sum([i[1] for i in rates_of_frequency]) / len(
            rates_of_frequency
        )
        average_of_leg = sum([i[1]["avg"] for i in sort_counting]) / len(sort_counting)
        if display_statistic:
            print("quantity of size of leg given bars", *sort_counting)
            print("average of leg", average_of_leg)
            print("rate from current to next quantity of bars", *rates_of_frequency)
            print("average of rate", average_of_rate)

        return sort_counting
        std_dev = sqrt(
            sum([(a[1] - average_of_leg) ** 2 for a in sort_counting])
            / (len(sort_counting))
        )
        # print("standard deviation", std_dev)
        # print("standard deviation Up", std_dev)
        # print("standard deviation Down", average_of_frequency-abs(average_of_frequency-std_dev))
