#!/usr/bin/env python3

import argparse
from math import cos, pi
import io
import queue
from threading import Thread
import xml.etree.ElementTree as ET

def input_thread(q):
	while True:
		try:
			line_in = input()
			#print("Processing line '{}'".format(line_in))
			freqb = list(map(float,(line_in.split(' '))))
			q.put(freqb)
			print(q)
		except EOFError:
			print("Reached EOF")
			return

def process(q, template, outfile, other_thread):
	root = template.getroot()
	c = [0] * len(root)
	while True:

		if not other_thread.is_alive() and q.empty():
			return

		try:
			p = c # p = previous, c = current spectrum list
			c = q.get(False)
		except queue.Empty:
			continue

		print("\tProcessing: {}".format(c))

		for i in range(5):
			for j in range(len(c)-1):
				root[j+1].attrib['coefs'] = '1 0 0 1 0 {}'.format((p[j]+c[j])/2+(p[j]-c[j])/2*cos(pi*i/5))

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