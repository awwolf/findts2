#!/usr/bin/env python
# encoding: utf-8
# -*- coding: iso-8859-1 -*-

import struct

def CutListEntry(where, what):
	w = where / 90
	ms = w % 1000
	s = (w / 1000) % 60
	m = (w / 60000) % 60
	h = w / 3600000
	if what == 0:
		type = "IN"
		type_col = 0x004000
	elif what == 1:
		type = "OUT"
		type_col = 0x400000
	elif what == 2:
		type = "MARK"
		type_col = 0x000040
	elif what == 3:
		type = "LAST"
		type_col = 0x000000
	return "%dh:%02dm:%02ds:%03d" % (h, m, s, ms), type

def toSec(where):
    w = where / 90
    return (w / 1000)

class CutsList():
    cuts = []
    last = None
    def __init__(self,file):
        try:
            fobj = open(file,"rb")

            data = fobj.read()
            #data = fobj.read(4)
            fobj.close()
            if not len(data) % 12 == 0:
                print("Cuts Datei ist ungülgtig")

            self.cuts = []
            self.last = None
            for i in range(len(data)/12):
                ts, = struct.unpack(">Q", data[0 + (i * 12):8 + (i * 12)])
                t, = struct.unpack(">I", data[8 + (i * 12):12 + (i * 12)])
                self.cuts.append(CutListEntry(ts,t))
                if t == 3:
                    self.last = toSec(ts)

        except:
            print("Fehler beim Cut Datei lesen")
