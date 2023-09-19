from my_jupyter.tools.Mbox import Mbox
from my_jupyter.metatrader_wrapper import MetatraderWrapper


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
        ohlc = self.mt.copy_rates_from_pos(stock, timeframe, shift, interval_required)
        ohlc_0_based = ohlc[::-1]
        return ohlc_0_based

    def buy(self, stock, volume):
        current_bar = self.mt.copy_rates_from_pos(stock, self.mt.TIMEFRAME_D1, 0, 1)
        close_price = current_bar["close"][0]
        order = {
            "action": self.mt.TRADE_ACTION_DEAL,
            "symbol": stock,
            "volume": float(volume/1.0),
            "type": self.mt.ORDER_TYPE_BUY,
            "price": close_price,
            "deviation": 10,
            "magic": 1618,
            "comment": f"{stock} {volume}",
        }
        # option = Mbox.BoxOkCancel("ENVIAR ORDEM", f"Buy {stock} {volume} {close_price}")
        # if option == Mbox.CANCELADO:
        #     return
        res = self.enviar_solicitacao_ao_homebroker(order)
        # if res:
        #     self.printing.printa_para_excel(ordem)
        #     return True
        self.last_response_from_homebroker = res
        return False

    def sell(self, stock, volume):
        current_bar = self.mt.copy_rates_from_pos(stock, self.mt.TIMEFRAME_D1, 0, 1)
        close_price = current_bar["close"][0]
        order = {
            "action": self.mt.TRADE_ACTION_DEAL,
            "symbol": stock,
            "volume": float(volume/1.0),
            "type": self.mt.ORDER_TYPE_SELL,
            "price": close_price,
            "deviation": 10,
            "magic": 1618,
            "comment": f"{stock} {volume}",
        }
        # option = Mbox.BoxOkCancel("ENVIAR ORDEM", f"Buy {stock} {volume} {close_price}")
        # if option == Mbox.CANCELADO:
        #     return
        res = self.enviar_solicitacao_ao_homebroker(order)
        # if res:
        #     self.printing.printa_para_excel(ordem)
        #     return True
        self.last_response_from_homebroker = res
        return False

    def positions(self, stock):
        posicoes = self.mt.positions_get(symbol=stock)
        return posicoes


    def enviar_solicitacao_ao_homebroker(self, request):
        print(
            "1. order_send(): by {} {} lots at {} with deviation={} points".format(
                request["symbol"], request["volume"], request["price"], 2
            )
        )
        result = self.mt.order_send(request)

        # # verificamos o resultado da execução
        if result is None:
            print("order_send() FAILED, error code =", self.mt.last_error())
        else:
            print(result)
        if result.retcode != self.mt.TRADE_RETCODE_DONE:
            print("2. order_send FAILED, retcode={}".format(result.retcode))
            # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print(
                            "       traderequest: {}={}".format(
                                tradereq_filed, traderequest_dict[tradereq_filed]
                            )
                        )
            return False
        return True


# rico_prod = "C:\\Program Files\\Rico - MetaTrader 5\\terminal64.exe"
