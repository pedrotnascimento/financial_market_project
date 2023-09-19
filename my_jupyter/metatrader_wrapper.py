import MetaTrader5 as mt


class MetatraderWrapper:
    MT_XM_GLOBAL_TESTER = r"C:\\Program Files\\XM Global MT5\\terminal64.exe"
    MT_XM_GLOBAL_PROD = r"C:\\Program Files\\XM Global MT5\\terminal64.exe"
    MT_XP_TESTER = r"C:\Program Files\MetaTrader 5\terminal64.exe"

    mt_on = False
    mt = mt

    def prod_on(self):
        self.mt_on = mt.initialize(self.MT_XM_GLOBAL_TESTER)
        return mt

    def demo_on(self):
        self.mt_on = mt.initialize(self.MT_XP_TESTER)
        return mt
