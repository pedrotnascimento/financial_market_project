from jupyter.metatrader_wrapper import MetatraderWrapper


class MarketDataRepository:
    mt_wrapper = MetatraderWrapper()
    mt = None

    def __init__(self):
        self.mt = self.mt_wrapper.demo_on()
        pass

    def read_data(self, stock, timeframe=None, interval_required: int = None):
        shift = 0
        if timeframe is None:
            timeframe = self.mt.TIMEFRAME_D1
        ohcl = self.mt.copy_rates_from_pos(stock, timeframe, shift, interval_required)
        return ohcl

    def buy(self, stock, volume):
        self.mt.Buy(stock, volume, comment=f"Fapi: {stock} {volume}")

    def sell(self, stock, volume):
        self.mt.Sell(stock, volume)


# rico_prod = "C:\\Program Files\\Rico - MetaTrader 5\\terminal64.exe"
