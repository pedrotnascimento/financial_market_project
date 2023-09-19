# from tools.Mbox import Mbox
import threading
from IPython.display import display, HTML, clear_output
from datetime import timedelta
import time

class DaemonThreadMini(threading.Thread):
    def __init__(
        self,
        job_to_execute,
        seconds=0,
        minutes=0,
        hours=0,
        segundos_wait=10,
        alerta_tempo=False,
        **kwargs
    ):
        # If you are going to have your own constructor, make sure you call the parent constructor too!
        #        Thread.__init__(self)
        # super(DaemonThreadMini, self).__init__()
        threading.Thread.__init__(self)

        self.job_to_execute = job_to_execute
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.segundos_wait = segundos_wait
        self.alerta_tempo = alerta_tempo
        self.kwargs = kwargs

    def run(self):
        self.atualiza_sinais_por_segundo()

    def atualiza_sinais_por_segundo(self):
        clear_output(wait=True)

        self.job_to_execute(**self.kwargs)
        while True:
            self.wait_until_restart_cycle()
            self.start_cycle()

    def wait_until_restart_cycle(self):
        remaining_time_to_reset = self.get_remaining_time()

        while remaining_time_to_reset == 0:
            remaining_time_to_reset = self.get_remaining_time_with_sleep()

    def get_remaining_time(self):
        tcurr = time.localtime()
        if self.minutes > 1:
            remaining_time_to_reset = tcurr.tm_min % self.minutes
        elif self.minutes == 1:
            remaining_time_to_reset = tcurr.tm_sec
        elif self.minutes < 1:
            remaining_time_to_reset = tcurr.tm_sec % self.seconds
        return remaining_time_to_reset

    def get_remaining_time_with_sleep(self):
        tcurr = time.localtime()
        if self.minutes > 1:
            remaining_time_to_reset = tcurr.tm_min % self.minutes
            time.sleep(self.segundos_wait)
        elif self.minutes == 1:
            remaining_time_to_reset = tcurr.tm_sec
            time.sleep(0.5)
        elif self.minutes == 0 and self.seconds > 0:
            remaining_time_to_reset = tcurr.tm_sec % self.seconds
            time.sleep(0.5)
        return remaining_time_to_reset

    def start_cycle(self):
        if self.hours == 0:
            self.wait_until_finish_cycle()
            clear_output(wait=True)
            self.job_to_execute(**self.kwargs)
            # if alerta_tempo:
            #     Mbox.Alerta("SINAIS ATUALIZADOS", "OK")
            print("SINAIS ATUALIZADOS")

    def wait_until_finish_cycle(self):
        remaining_time_to_reset = self.get_remaining_time()
        while remaining_time_to_reset != 0:
            remaining_time_to_reset = self.get_remaining_time_with_sleep()
