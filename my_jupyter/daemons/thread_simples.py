import threading

class ThreadSimples(threading.Thread):
    def __init__(self, funcao, **kwargs):
        # If you are going to have your own constructor, make sure you call the parent constructor too!
        #        Thread.__init__(self)
        super(ThreadSimples, self).__init__()
        self.funcao = funcao
        

    def run(self):
      self.funcao()
