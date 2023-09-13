import MetaTrader5 as mt

class MetatraderWrapper:
    PATHS = {
        "MT_XP_TESTER": "C:\\Program Files\\XM Global MT5\\terminal64.exe",
        "MT_XP_PROD": "C:\\Program Files\\XM Global MT5\\terminal64.exe",
    }
    
    mt_on = False
    mt = mt
    def prod_on(self):
        self.mt_on = mt.initialize(self.PATHS["MT_XP_PROD"])
        return mt

    def demo_on(self):
        self.mt_on = mt.initialize(self.PATHS["MT_XP_TESTER"])
        return mt
