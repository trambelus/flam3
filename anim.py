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
			print("Input line '{}'".format(line_in))
			freqb = list(map(float,(line_in.split(' '))))
			q.put(freqb)
			#print(q)
		except EOFError:
			print("Reached EOF")
			return

def process_single(c, p, template, root, outfile):
	print("Processing: {}".format(c))

	for i in range(10):
		for j in range(len(c)):
			root[j+1].attrib['linear'] = str((p[j]+c[j])/2+(p[j]-c[j])/2*cos(pi*i/10))

		flame_strio = io.BytesIO()
		template.write(flame_strio)
		flame_str = flame_strio.getvalue()
		with open(outfile, 'a', encoding='UTF-8') as f:
			f.write('\n'+flame_str.decode('UTF-8'))

def process_all(q, template, outfile, other_thread):
	with open(outfile, 'w') as f:
		f.write('<spectrum>')
	root = template.getroot()
	c = [0] * len(root)
	while True:

		if not other_thread.is_alive() and q.empty():
			print('!')
			break

		a = []
		for i in range(10):
			if q.empty():
				break
			a.append(q.get())

		a = [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))] # reshape

		p = c # p = previous, c = current spectrum list
		c = [max(i) for i in a]
		c = [i/4+0.125 for i in c]
		process_single(c,p, template, root, outfile)

	with open(outfile, 'a') as f:
		f.write('</spectrum>')

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
	# t.start()
	input_thread(q)
	template = ET.parse(args.template)
	process_all(q, template, args.output, t)

if __name__ == '__main__':
	main()