#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Multi Thread md5 cracker by 0x94

import Queue
import threading
import sys
import time
import hashlib

queue = Queue.Queue()
#Ayarlar----------------------------------
kirilacak=sys.argv[1]
print "Kırılacak Olan Hash : %s " %(kirilacak)
maxthread=20
liste=sys.argv[2]
print "Wordlist Dosyasi : %s " %(liste)
#---------------------------------------


class hazirla:
    def __init__(self):
        self.stop   = False
        
    def thbaslat(self,sifreler):
        lock    = threading.Lock()
        for sifre in sifreler:
            if sifre.strip():
                queue.put(sifre.strip())
        threads = []
                
        for i in range(maxthread):
            t = md5kir(queue,lock, self)
            t.setDaemon(True)
            threads.append(t)
            t.start()
            
        while any([x.isAlive() for x in threads]):
            time.sleep(0.0)
            
        #queue.join()
        
    def main(self):
        try:
            dosya      = open(liste)
        except IOError:
            print "dosya bulunamadi %s" % (liste)
            sys.exit(0)
        try:
            self.thbaslat(dosya.xreadlines()) 
        except (KeyboardInterrupt,SystemExit):
            self.stop = True
            print "iptal edildi"
            exit()
            
class md5kir(threading.Thread):
    def __init__(self, queue,lock, parent):
        threading.Thread.__init__(self)
        self.queue      = queue
        self.br         = None
        self.lock       = lock
        self.stop       = parent.stop
        
    def run(self):
        start=time.time()
        while not self.queue.empty() and not self.stop: 
            quedekiverim = self.queue.get()
            md5=hashlib.md5(quedekiverim).hexdigest()
            if (kirilacak==md5):
                with self.lock:
                    print "Cracked :%s" % (quedekiverim)
                    print "Bitis Zamani: %s" % (time.time() - start)
                    self.stop   = True
                    exit()
                #self.queue.task_done()
        print ""         
    
if __name__ == "__main__":
    x=hazirla()
    x.main()
