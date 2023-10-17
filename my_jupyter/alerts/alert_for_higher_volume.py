from my_jupyter import metatrader_wrapper
from my_jupyter.daemons.daemon_tools import DaemonThreadMini
from datetime import timedelta as td, datetime as dt
import MetaTrader5 as mt
from IPython import display
import pandas as pd
from my_jupyter.modules.simple_alert import SimpleAlert
import time


class AlertVolumeHigher:
    def __init__(self):
        self.mt_rep = MarketDataRepository()
        self.mt = self.mt_rep.mt

    def run_daemon(self):
        thread_exec = DaemonThreadMini(self.exec_daemon, seconds=0, mseconds=800)
        thread_exec.start()

    def exec_daemon(self, **kwargs):
        utc_time = 3
        td_ = td(hours=utc_time, minutes=1)
        now = dt.now()
        nexti = now - td_

        def alert_ticks(stock, type):
            ticks = self.mt.copy_ticks_range(stock, nexti, now, mt.COPY_TICKS_TRADE)
            ticks_frame = pd.DataFrame(ticks)
            nanoseconds_in_miliseconds = 10000
            ticks_time_in_miliseconds = (
                ticks_frame["time_msc"] / nanoseconds_in_miliseconds
            )
            ticks_frame["time"] = pd.to_datetime(ticks_time_in_miliseconds, unit="s")
            ticks_frame_vol = ticks_frame[ticks_frame["volume"] > (7 + 23)]
            if len(ticks_frame_vol) > 0:
                display.clear_output()
                frame_buy = ticks_frame_vol.copy(deep=True)
                frame_buy["flags"] = frame_buy["flags"] & (
                    mt.TICK_FLAG_BUY | mt.TICK_FLAG_BID
                )
                frame_buy = frame_buy[frame_buy["flags"] > 0]

                frame_sell = ticks_frame_vol.copy(deep=True)
                frame_sell["flags"] = ticks_frame_vol["flags"] & (
                    mt.TICK_FLAG_SELL | mt.TICK_FLAG_ASK
                )
                frame_sell = frame_sell[frame_sell["flags"] > 0]

                if len(frame_buy) > 0:
                    print(">>Comprando")
                    display.display(frame_buy)
                    SimpleAlert.BoxOkCancelAsync("alerta IND", "Comprando")
                    time.sleep(29)
                elif len(frame_sell) > 0:
                    print(">>Vendendo")
                    display.display(frame_sell)
                    SimpleAlert.BoxOkCancelAsync("alerta IND", "Vendendo")
                    time.sleep(29)

        alert_ticks("INDV23", -1)
