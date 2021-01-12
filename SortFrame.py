from PIL import Image, ImageTk
from math import log2, ceil
from random import shuffle
from time import sleep
import os
import tkinter as tk
import threading
import enum


PATH = os.getcwd()
WIDTH = 15
IMG_NUM = 50
MAX_HEIGHT = 500

class SortFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.type = self.SortType.NONE
        self.lock = threading.Lock()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #Tests shuffle button
        self.shuffle = tk.Button(self, text="Shuffle", fg="blue", command=self.shuffle_list)
        self.shuffle.grid(column=28, row=0)

        #Quit button
        self.quit = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit.grid(column=29, row=0)

        #Sorting Buttons
        self.bubble_button = tk.Button(self, text="Bubble Sort", command=self.bubble)
        self.bubble_button.grid(column=0, row=0)

        self.insertion_button = tk.Button(self, text="Insertion Sort", command=self.insertion)
        self.insertion_button.grid(column=1, row=0)

        self.selection_button = tk.Button(self, text="Selection Sort", command=self.selection)
        self.selection_button.grid(column=2, row=0)

        self.merge_button = tk.Button(self, text="Merge Sort", command = self.merge)
        self.merge_button.grid(column=3, row=0)

        self.quick_button = tk.Button(self, text="Quick Sort", command=self.quick)
        self.quick_button.grid(column=4, row=0)

        #Creates images and canvas
        self.rect = []
        for i in range(IMG_NUM):
            self.rect.append(ImageTk.PhotoImage(
                Image.open(PATH + "\\Images\\rect" + str(IMG_NUM-i) + ".png")))
        self.canvas = tk.Canvas(self, width=(IMG_NUM+1)*WIDTH, height=MAX_HEIGHT+20)
        self.display_list()

    def bubble(self):
        self.shuffle_list()
        self.type = self.SortType.BUBBLE
        self.display_list()
        self.bubble_thread = BubbleSort(self, "Bubble Sort Thread")
        self.bubble_thread.start()

    def insertion(self):
        self.shuffle_list()
        self.type = self.SortType.INSERTION
        self.display_list()
        self.insertion_thread = InsertionSort(self, "Insertion Sort Thread")
        self.insertion_thread.start()

    def selection(self):
        self.shuffle_list()
        self.type = self.SortType.SELECTION
        self.display_list()
        self.selection_thread = SelectionSort(self, "Selection Sort Thread")
        self.selection_thread.start()

    def merge(self):
        self.shuffle_list()
        self.type = self.SortType.MERGE
        self.display_list()
        self.merge_thread = MergeSort(self, "Merge Sort Thread")
        self.merge_thread.start()

    def quick(self):
        self.shuffle_list()
        self.type = self.SortType.QUICK
        self.display_list()
        self.quick_thread = QuickSort(self, "Quick Sort Thread")
        self.quick_thread.start()

    def display_list(self):
        self.canvas.delete("all")
        for i in range(IMG_NUM):
            self.canvas.create_image(i*WIDTH, MAX_HEIGHT+10, anchor=tk.SW, 
                image=self.rect[i])
        self.canvas.grid(column=0, row=1, rowspan=20, columnspan=30)

    def shuffle_list(self):
        self.type = SortFrame.SortType.NONE
        self.lock.acquire()
        shuffle(self.rect)
        sleep(.5)
        self.display_list()
        self.lock.release()

    class SortType(enum.Enum):
        NONE = enum.auto()
        BUBBLE = enum.auto()
        INSERTION = enum.auto()
        SELECTION = enum.auto()
        MERGE = enum.auto()
        QUICK = enum.auto()

#Thread to execute bubble sort
class BubbleSort(threading.Thread):
    def __init__(self, own_app, name):
        threading.Thread.__init__(self)
        self.app = own_app
        self.name = name

    def run(self):
        change = False
        while (self.app.type == SortFrame.SortType.BUBBLE):
            try:
                sleep(.5)
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

#Thread to execute insertion sort
class InsertionSort(threading.Thread):
    def __init__(self, own_app, name):
        threading.Thread.__init__(self)
        self.app = own_app
        self.name = name

    def run(self):
        i = 1
        while (self.app.type == SortFrame.SortType.INSERTION and i < IMG_NUM):
            try:
                sleep(.5)
                self.app.lock.acquire()
                check = self.app.rect[i]
                j = i-1
                while (j >= 0 and self.app.rect[j].height() > check.height()):
                    self.app.rect[j+1] = self.app.rect[j]
                    j -= 1
                self.app.rect[j+1] = check
                i += 1
                self.app.display_list()
                self.app.lock.release()
            except:
                break

#Thread to execute selection sort
class SelectionSort(threading.Thread):
    def __init__(self, own_app, name):
        threading.Thread.__init__(self)
        self.app = own_app
        self.name = name

    def run(self):
        i = 0
        while (self.app.type == SortFrame.SortType.SELECTION and i < IMG_NUM):
            try:
                sleep(.5)
                self.app.lock.acquire()
                min = self.app.rect[i]
                index = i
                for j in range(i, len(self.app.rect)):
                    if (self.app.rect[j].height() < min.height()):
                        min = self.app.rect[j]
                        index = j
                self.app.rect[i], self.app.rect[index] = self.app.rect[index], self.app.rect[i]
                i += 1
                self.app.display_list()
                self.app.lock.release()
            except:
                break

#Thread to execute Merge Sort
class MergeSort(threading.Thread):
    def __init__(self, own_app, name):
        threading.Thread.__init__(self)
        self.app = own_app
        self.name = name
        
    def run(self):
        #initiatlization
        self.copy = [tk.PhotoImage()] * IMG_NUM
        curr_size = 1
        while (self.app.type == SortFrame.SortType.MERGE and curr_size < IMG_NUM):
            try:
                sleep(.5)
                self.app.lock.acquire()
                i = 0

                #Calls merge
                while (i < IMG_NUM and self.app.type and self.app.type == SortFrame.SortType.MERGE):
                    self.merge(i, min(i+curr_size, IMG_NUM), min(i+2*curr_size, IMG_NUM))
                    i += 2 * curr_size
        
                if (self.app.type != SortFrame.SortType.MERGE):
                    self.app.lock.release()
                    break

                #Diplays the new rect
                for j in range(IMG_NUM):
                    self.app.rect[j] = self.copy[j]
                self.app.display_list()
                curr_size = 2 * curr_size
                self.app.lock.release()
            except:
                break
    
    def merge(self, left, right, end):
        i = left
        j = right
        for k in range(left, end):
            if (i < right and (j >= end or self.app.rect[i].height() < self.app.rect[j].height())):
                self.copy[k] = self.app.rect[i]
                i += 1
            else:
                self.copy[k] = self.app.rect[j]
                j += 1

#Thread to execute Quick Sort
class QuickSort(threading.Thread):
    def __init__(self, own_app, name):
        threading.Thread.__init__(self)
        self.app = own_app
        self.name = name

    def run(self):
        stack = [0] * (IMG_NUM)
        top = 0
        stack[top] = 0
        top += 1
        stack[top] = IMG_NUM-1

        while (self.app.type == SortFrame.SortType.QUICK and top >= 0):
            try:
                sleep(.5)
                self.app.lock.acquire()
                h = stack[top]
                top -= 1
                l = stack[top]
                top -= 1

                index = self.partition(l, h)
                if (index-1 > l):
                    top += 1
                    stack[top] = l
                    top += 1
                    stack[top] = index - 1
                
                if (index + 1 < h):
                    top += 1
                    stack[top] = index + 1
                    top += 1
                    stack[top] = h
                
                self.app.display_list()
                self.app.lock.release()
            except:
                break

    def partition(self, l, h):
        i = (l-1)
        check = self.app.rect[h]

        for j in range(l, h):
            if self.app.rect[j].height() <= check.height():
                i += 1
                self.app.rect[i], self.app.rect[j] = self.app.rect[j], self.app.rect[i]
        self.app.rect[i+1], self.app.rect[h] = self.app.rect[h], self.app.rect[i+1]
        return (i+1)

    