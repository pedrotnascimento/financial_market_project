import ctypes  # An included library with Python install.
import winsound

from my_jupyter.daemons.thread_simples import ThreadSimples


class Mbox:
    OK = 1
    CANCELADO = 2

    def BoxOkCancel(title, text):
        winsound.MessageBeep(winsound.MB_OK)
        ctypes.windll.user32.MessageBoxW(0, text, title, 1)

    def Alerta(title, text=""):
        winsound.MessageBeep(winsound.MB_OK)
        funcao = lambda: ctypes.windll.user32.MessageBoxW(0, text, title, 0x1000)
        Mbox.executar_alerta_paralelo(funcao)

    def executar_alerta_paralelo(funcao_alerta, *args):
        thread_exec = ThreadSimples(funcao_alerta, *args)
        thread_exec.start()

    def BoxOkCancelAsync(title, text):
        Mbox.executar_alerta_paralelo(Mbox.BoxOkCancel, title, text)
