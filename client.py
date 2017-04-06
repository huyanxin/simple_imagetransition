#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import socket
import cv2
import numpy
import zlib

address = ('127.0.0.1', 6666)


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return 0
        buf += newbuf
        count -= len(newbuf)
    return buf

def run(addr):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    try:
        while True:
                length = recvall(client, 16)
                stringData = recvall(client, int(length))
                stringData = zlib.decompress(stringData)
                data = numpy.fromstring(stringData, dtype='uint8')
                decimg=cv2.imdecode(data,1)
                r,l,n = decimg.shape
                decimg = cv2.resize(decimg,(int(r*1.5),int(l)))
                cv2.imshow('Client1',decimg)
                if cv2.waitKey(10) == 27:
                    break

    except KeyboardInterrupt:
        client.close()
        cv2.destroyAllWindows()
    client.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # print "please input destination ip address:"
    # ip = raw_input(">>")
    # print "please input destination port:"
    # port = int(raw_input(">>"))
    ip,port = ("127.0.0.1", 6666)
    port = int(port)
    print ip, port,type(port)
    run((ip, port))
