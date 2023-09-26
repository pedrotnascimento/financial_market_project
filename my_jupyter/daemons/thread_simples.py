import threading


class ThreadSimples(threading.Thread):
    def __init__(self, funcao, *args, **kwargs):
        # If you are going to have your own constructor, make sure you call the parent constructor too!
        #        Thread.__init__(self)
        super().__init__()
        self.funcao = funcao
        self.kwargs = kwargs
        self.args = args

    def run(self):
        self.funcao(*self.args, **self.kwargs)
