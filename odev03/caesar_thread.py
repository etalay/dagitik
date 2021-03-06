# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:55:37 2015

@author: e-talay
"""

import string
import threading
import time
import sys


#Kriptolama icin kullandigimiz algoritma.
def caesar(substring, shift_number, decode = False):
   if decode: shift_number = 26 - shift_number
   return substring.translate(
       string.maketrans(
           string.ascii_uppercase + string.ascii_lowercase,
           string.ascii_uppercase[shift_number:] + string.ascii_uppercase[:shift_number] +
           string.ascii_lowercase[shift_number:] + string.ascii_lowercase[:shift_number]
           )
       )

#thread class'larinin olusturulmasi.
class myThread (threading.Thread):
    def __init__(self, threadID,counter,fread,fwrite,shiftNumber):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.counter = counter
        self.fread = fread
        self.fwrite = fwrite
        self.shiftNumber = shiftNumber
    def run(self):
        global exit
        while not exit:
            threadLock.acquire()
            buffin=fread.read(self.counter)
            if not buffin:
                exit = 1
                threadLock.release()
            else:
                buffout=caesar(buffin,self.shiftNumber).upper()             
                fwrite.write(''.join(buffout))
                threadLock.release()
            time.sleep(0.001)

threads = []
threadLock = threading.Lock()
fread = open("metin.txt","r")
path = "crypted_"+sys.argv[1]+"_"+sys.argv[2]+"_"+sys.argv[3]+".txt"
fwrite = open(path,"w")

#thread'larin olusturulmasi.
for i in range(int(sys.argv[2])):
    threadd = myThread(i,int(sys.argv[3]),fread,fwrite,int(sys.argv[1]))
    threads.append(threadd)
    threadd.start()

#thread'larin olusturulacak dosyaya yazma sirasina gore bekletilmesi.
for t in threads:
    t.join()


#yazma ve okuma islemleri icin kullandigimiz dosyalarin kapatilmasi.
fwrite.close()
fread.close()
