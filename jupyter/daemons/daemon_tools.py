from tools.Mbox import Mbox
import threading
from IPython.display import display, HTML, clear_output
from datetime import timedelta
import time
from timeloop import Timeloop
import sys
# sys.path.append(".")


def atualiza_sinais(funcao, seconds=0, minutes=0, hours=0, alerta_tempo=False, **kwargs):
    tl = Timeloop()

    def sincronizar_tempo_para_minutos_restantes():
        if minutes != 0 and hours == 0:
            tcurr = time.localtime()
            faltam_minutos = minutes - tcurr.tm_min % minutes
            segundos_60 = 60
            segundos = faltam_minutos*segundos_60

            time.sleep(segundos)

    funcao(**kwargs)
    # sincronizar_tempo_por_segundos()
    # sincronizar_tempo_para_minutos_restantes()

    @tl.job(interval=timedelta(seconds=seconds, minutes=minutes, hours=hours))
    def atualiza_sinais_timeloop():
        clear_output(wait=True)
        # print(*args)
        funcao(**kwargs)
        if(alerta_tempo):
            Mbox.Alerta("SINAIS ATUALIZADOS", "OK")

    tl.start()
    while True:
        try:
            time.sleep(1)
        except:
            tl.stop()
            tl = None
            break


class DaemonThreadMini(threading.Thread):
    def __init__(self, funcao, seconds=0, minutes=0, hours=0, segundos_wait=10, alerta_tempo=False, **kwargs):
        # If you are going to have your own constructor, make sure you call the parent constructor too!
        #        Thread.__init__(self)
        super(DaemonThreadMini, self).__init__()
        self.funcao = funcao
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.segundos_wait = segundos_wait
        self.alerta_tempo = alerta_tempo
        self.kwargs = kwargs
        if 'trend' in kwargs:
            self.trend = kwargs['trend']
        if 'alarme_desativar' in kwargs:
            self.alarme_desativar = kwargs['alarme_desativar']
        if 'alarme_ativar' in kwargs:
            self.alarme_ativar = kwargs['alarme_ativar']

    def run(self):
      
      self.atualiza_sinais_por_segundo(self.funcao, self.seconds, self.minutes, self.hours, self.segundos_wait, self.alerta_tempo, **self.kwargs)

    def atualiza_sinais_por_segundo(self, funcao, seconds=0, minutes=0, hours=0, segundos_wait=10, alerta_tempo=False, **kwargs):
        def sincronizar_tempo_por_segundos():
            if minutes != 0 and hours == 0:
                tcurr = time.localtime()
                if self.minutes>1:
                    resto_minutos = tcurr.tm_min % minutes
                elif self.minutes==1:
                    resto_minutos = tcurr.tm_sec
                while resto_minutos != 0:
                    tcurr = time.localtime()
                    if self.minutes>1:
                        resto_minutos = tcurr.tm_min % minutes
                    elif self.minutes==1:
                        resto_minutos = tcurr.tm_sec
                    time.sleep(segundos_wait)
                clear_output(wait=True)
                # print('xx', self.trend)
                funcao(self, **kwargs)
                if(alerta_tempo):
                    Mbox.Alerta("SINAIS ATUALIZADOS", "OK")

        clear_output(wait=True)
        # print('xx', self.trend)
        funcao(self, **kwargs)
        while True:
            tcurr = time.localtime()
            if self.minutes>1:
                resto_minutos = tcurr.tm_min % minutes
            elif self.minutes==1:
                resto_minutos = tcurr.tm_sec

            while resto_minutos == 0:
                tcurr = time.localtime()
                if self.minutes>1:
                    resto_minutos = tcurr.tm_min % minutes
                    time.sleep(segundos_wait)
                elif self.minutes==1:
                    resto_minutos = tcurr.tm_sec
                    time.sleep(0.5)
            sincronizar_tempo_por_segundos()
