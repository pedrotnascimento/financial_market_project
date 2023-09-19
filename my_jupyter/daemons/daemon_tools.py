# from tools.Mbox import Mbox
import threading
from IPython.display import display, HTML, clear_output
from datetime import timedelta
import time


class DaemonThreadMini(threading.Thread):
    def __init__(
        self,
        job_to_execute,
        mseconds=0,
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
        self.mseconds = mseconds
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.segundos_wait = segundos_wait
        self.alerta_tempo = alerta_tempo
        self.kwargs = kwargs

    def run(self):
        self.atualiza_sinais_por_segundo()

    def atualiza_sinais_por_segundo(self):
        # clear_output(wait=True)

        self.job_to_execute(**self.kwargs)
        while True:
            self.wait_until_restart_cycle()
            self.start_cycle()

    def wait_until_restart_cycle(self):
        remaining_time_to_reset = self.get_remaining_time()
        time.sleep(remaining_time_to_reset)
        # remaining_time_to_reset = self.get_remaining_time_with_sleep()

    def get_remaining_time(self):
        tcurr = time.localtime()
        seconds_in_minute = 60
        remaining_time_to_reset_in_seconds = 1
        if self.minutes > 1:
            remaining_time_to_reset_in_seconds = (
                tcurr.tm_min % self.minutes
            ) * seconds_in_minute - tcurr.tm_sec
        elif self.minutes == 1:
            remaining_time_to_reset_in_seconds = seconds_in_minute - tcurr.tm_sec
        elif self.minutes < 1:
            if self.seconds > 1:
                remaining_time_to_reset_in_seconds = tcurr.tm_sec % self.seconds
            elif self.seconds == 1:
                remaining_time_to_reset_in_seconds = 1
            elif self.seconds < 1 and self.mseconds > 0:
                miliseconds_in_second = 1000.0
                remaining_time_to_reset_in_seconds = self.mseconds / miliseconds_in_second
        if remaining_time_to_reset_in_seconds != 0:
            return remaining_time_to_reset_in_seconds
        non_zero_remaining_time = 1
        return non_zero_remaining_time

    def get_remaining_time_with_sleep(self):
        remaining_time_to_reset = self.get_remaining_time()
        time.sleep(0.010)
        return remaining_time_to_reset

    def start_cycle(self):
        if self.hours == 0:
            # self.wait_until_finish_cycle()
            # clear_output(wait=True)
            self.job_to_execute(**self.kwargs)
            # if alerta_tempo:
            #     Mbox.Alerta("SINAIS ATUALIZADOS", "OK")
            print("SINAIS ATUALIZADOS")

    def wait_until_finish_cycle(self):
        remaining_time_to_reset = self.get_remaining_time()
        while remaining_time_to_reset != 0:
            remaining_time_to_reset = self.get_remaining_time_with_sleep()
