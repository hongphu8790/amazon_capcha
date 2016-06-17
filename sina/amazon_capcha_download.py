#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Chuande Wang on 16/6/13
import os
import re
from PIL import Image
from HTMLParser import HTMLParser
import urllib
import urllib2
import os
import threading
import Queue
from amazon_capcha import  binarized

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            if len(attrs) == 0: pass
            else:
                for (variable, value)  in attrs:
                    if variable == "src":
                        res = re.search('https:.*jpg',value)
                        if res:
                            #  ''.join(res.group())
                            self.links.append(''.join(res.group()))
def download_images(queue):
    while True:
        picurl, picture_name =  queue.get()

        if not os.path.exists('amazonpicture'):
            os.mkdir('amazonpicture')

        save_path = "amazonpicture/"
        imgData = urllib2.urlopen(picurl).read()
        # 给定图片存放名称
        picName = save_path + picture_name
        print picName

        output = open(picName, 'wb+')
        output.write(imgData)
        output.close()

def create_threads(thread_num, thread_queue, fun):
    """创建处理单url的线程"""

    for i in range(thread_num):
        th = threading.Thread(target=fun, args = (thread_queue,))
        th.daemon = True
        th.start()




def main():

    hp = MyHTMLParser()
    queue = Queue.Queue()
    create_threads(8, queue, download_images)

    for filename in os.listdir(r'debug'):
        htmlname = 'debug/{}'.format(filename)
        #print(htmlname)
        f = open(htmlname, 'r')
        data = f.read()
        f.close()
        hp.feed(data)
        hp.close()

    for picurl in hp.links:
        picture_name =  binarized(picurl)
        queue.put(picurl, picture_name)

    queue.join()


    print "Finished download \n"



if __name__ == '__main__':
    main()