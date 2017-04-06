#!/usr/bin/env python

import socket
import cv2
import numpy
import sys
import zlib
# import pylzma as lzma


def run(addr):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	sock.bind(addr)
	sock.listen(True)
	conn, addr = sock.accept()
	capture = cv2.VideoCapture(0)
	capture.set(cv2.cv.CV_CAP_PROP_FOURCC, cv2.cv.CV_FOURCC('M','P','4','2'))
	ret, frame = capture.read()
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),25]

	try :
		while ret:
			print "frame len: ",len(frame.tostring())
			result, imgencode = cv2.imencode('.jpg', frame, encode_param)

			data = numpy.array(imgencode)
			stringData = data.tostring()
			print "ori len %s" % len(stringData)
			stringData = zlib.compress(stringData, 9)
			print "zlib len %s" % len(stringData)


			try:
				conn.send(str(len(stringData)).ljust(16))
				conn.send(stringData)
			except Exception:
				break
			ret, frame = capture.read()
			if cv2.waitKey(10) == 27:
				break
	except Exception:
		print Exception.tostring()
		sock.close()
		cv2.destroyAllWindows()
	sock.close()
	cv2.destroyAllWindows()
if __name__ == "__main__":

	# port = int(sys.argv[2])
	# ip = sys.argv[1]
	ip,port = "127.0.0.1", 6666
	print "server ip is:\n %s" % ip
	address = (ip, port)
	try:
		while True:
			run(address)
	except Exception:
		sys.exit(0)
