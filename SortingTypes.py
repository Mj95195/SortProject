import threading
from SortFrame import SortFrame

class BubbleSort(threading.Thread):
    def __init__(self, own_app, name):
        threading.Thread.__init__(self)
        self.app = own_app
        self.name = name

    def run(self):
        change = False
        while (self.app.type == SortFrame.SortType.BUBBLE):
            try:
                time.sleep(.5)
                self.app.lock.acquire()
                change = False
                for i in range(len(self.app.rect)-1):
                    if (self.app.rect[i].height() > self.app.rect[i+1].height()):
                        self.app.rect[i], self.app.rect[i+1] = self.app.rect[i+1], self.app.rect[i]
                        change = True
                self.app.display_list()
                self.app.lock.release()
                if (not change):
                    break
            except:
                break