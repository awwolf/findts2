#!/usr/bin/python
# encoding: utf-8
# -*- coding: iso-8859-1 -*-
#
# MetaSupport
# Copyright (C) 2011 betonme
#
# In case of reuse of this source code please do not remove this copyright.
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	For more information on the GNU General Public License see:
#	<http://www.gnu.org/licenses/>.
#

# Modifyed 2019 AWW

class MetaList():
    name = ""
    description = ""
    tags = []
    def __init__(self,file):
        try:
            fobj = open(file,"rb")
            meta = []
            fobj.readline()
            self.name = fobj.readline().replace("\n","")
            self.description = fobj.readline().replace("\n","")
            fobj.readline()
            tags = fobj.readline()
            if len(tags) > 1:
                self.tags = tags.replace("\n","").split(" ")
            else:
                self.tags = []
            fobj.close()
        except:
            print("Fehler beim Meta Datei lesen")