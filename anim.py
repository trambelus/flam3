#!/usr/bin/env python3

import argparse
from math import cos, pi
import io
import queue
from threading import Thread
import xml.etree.ElementTree as ET

def input_thread(q):
	while True:
		freqb = list(map(float,(input().split(' '))))
		q.put(freqb)

def process(q, template, outfile, other_thread):
	root = template.getroot()
	c = [0] * len(root)
	while True:

		if not other_thread.is_alive():
			return


		try:
			p = c # p = previous, c = current spectrum list
			c = q.get(False)
		except queue.Empty:
			continue

		for i in range(5):
			for j in range(len(c)):
				root[j].attrib['coefs'] = '1 0 0 1 0 {}'.format((p[j]+c[j])/2+(p[j]-c[j])/2*cos(pi*i/5))

			flame_strio = io.BytesIO()
			template.write(flame_strio)
			flame_str = flame_strio.getvalue()
			with open(outfile, 'a', encoding='UTF-8') as f:
				f.write('\n'+flame_str.decode('UTF-8'))

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('template',
		help="File from which to read flame template")
	parser.add_argument('output',
		help="File to which to write flame animation frames")
	return parser.parse_args()

def main():
	args = parse_args()
	q = queue.Queue()
	t = Thread(target=input_thread, args=(q,))
	t.start()
	template = ET.parse(args.template)
	process(q, template, args.output, t)

if __name__ == '__main__':
	main()