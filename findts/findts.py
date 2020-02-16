#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
from __future__ import print_function
import platform
import subprocess
import sys

import EitSupport
import MetaSupport
import CutsSupport

class color:
    norm            = "\033[m"
    yellow          = "\033[3;33m"
    yellowbright    = "\033[1;33m"
    redbright       = "\033[1;31m"
    white           = "\033[1;37m"
    darkgrey        = "\033[1;30m"
    blue            = "\033[0;34m"
    aqua_underline  = "\033[4;36m" #"\033[4;36m"
    green           = "\033[0;32m"
    find = redbright
    path = aqua_underline
    details =darkgrey
    tag = blue
    name = white
    sum = "\033[100;37m"

class C:
    NULL = "\x00"
    EXT = "\x13"
    FE  = "\xFE"
    F8  = "\xF8"

    DC3  = "\x05"

def sum_output():
    pass



if not "linux".upper() in platform.platform().upper():
    print("Falsches Betriebsystem: %s\r\n  nur unter Linux moeglich" % platform.platform())
    exit()



i_path, i_file = range(2)

args = sys.argv[1:]

if len(args) == 0 or "-h" in args or "--h" in args:
    print("")
    print("Sucht im Dateinamen den Filmtitel")
    print("")
    print("Keine Argumente angegeben: findts teildesfilmnames [-d]")
    print(" -e -E    EPG Daten/erweiterte Daten Anzeigen")
    print(" -d -D    Dauer Anzeigen/Dauer in Minuten anzeigen")
    print(" -n       Namen anzeigen")
    print(" -N       Dateinamen ausblenden (Zeigt statdessen den Namen an)")
    print(" -m       Metadaten anzeigen")
    print(" -M       Dateinamen ausblenden, Metadaten anzeigen")
    print(" -a       erweiterte Meta Daten anzeigen")
    print(" -t       Tags anzeigen")
    print(" -c       Vortschritt anzeigen")
    print(" -C       Cuts Anzeigen")
    print(" -S       Summe anzeigen")
    print(" -h       Hilfe Dialog")

    exit()


findarg = args[0]
bashstr = "find /media/hdd/dlna/Video -iname *" + findarg + "*.ts"
bashstr = bashstr.split(" ")


available_parms_eit = ("-e", "-E", "-d", "-D", "-n", "-N")
available_parms_meta = ("-M", "-m","-a","-t" )
available_parms_else = ("-S", "-c", "-C" )


get_eit,get_else,get_meta = [],[],[]
for i in available_parms_else:
    if i in args:
        get_else.append(i)
for i in available_parms_eit:
    if i in args:
        get_eit.append(i)
for i in available_parms_meta:
    if i in args:
        get_meta.append(i)

if "-N" in get_eit and not "-n" in get_eit: get_eit.append("-n")
if "-M" in get_meta and not "-m" in get_meta: get_meta.append("-m")


file_list = subprocess.check_output(bashstr).split("\n")[:-1]
for idx,i in enumerate(file_list):
    file_list[idx] =  file_list[idx].rsplit("/",1,)
    #prisnt(idx,i)
    pass

path = ""
print(color.white)
sum_e, sum = 0,0
for i in file_list:

    if not i[i_path] == path:
        if "-S" in get_else and sum_e > 0:
            print(color.sum + "Anzahl: " + str(sum_e) + color.norm + "\n")
            sum_e = 0
        print(color.path + i[i_path] + color.norm)
        path = i[i_path]

    sum_e += 1
    sum   += 1

    #print(get_else,get_eit,get_meta)
    if not "-N" in get_eit and not "-M" in get_meta:
        #Dateinamen Ausgabe
        if "*" in findarg:
            print(color.white + i[i_file])
        else:
            pos = str.find(i[i_file].upper(), findarg.upper())
            print(color.white +  i[i_file][:pos] + color.find + i[i_file][pos:pos+len(findarg)] + color.white + i[i_file][pos+len(findarg):])

    if get_meta:
        Meta = MetaSupport.MetaList(i[i_path] + "/" + i[i_file] + ".meta")
        if "-M" in get_meta or "-m" in get_meta: print(color.white + Meta.name)
        if "-a" in get_meta and len(Meta.description) > 0: print(color.details + Meta.description)
        if "-t" in get_meta and len(Meta.tags) > 0:
            print(color.tag,end = "")
            for i in Meta.tags: print(i + " ", end="")
            print()

    if "-C" in get_else or "-c" in get_else or "-d" in get_eit or "-D" in get_eit:
        Cuts = CutsSupport.CutsList(i[i_path] + "/" + i[i_file] + ".cuts")

        if "-C" in get_else:
            for ts,t in Cuts.cuts:
                print(color.darkgrey + ts + "\t", end="")
                if t=="LAST":
                    print("\033[1;32mLAST" + color.norm)
                elif t=="MARK":
                    print("\033[1;31mMARK" + color.norm)
                else:
                    print("\033[0;33m"+ t + color.norm)



    if get_eit:

        Eit = EitSupport.EitList(i[i_path]+"/"+i[i_file][:-3]+".eit")
        if "-n" in get_eit: print(color.white + Eit.getEitName())
        print(color.details, end="")
        if "-e" in get_eit:
            br = Eit.getEitDescription().find("\n")
            print(Eit.getEitDescription()[:br])
        if "-E" in get_eit: print(Eit.getEitDescription())
        if "-d" in get_eit: print("Dauer: " + str(Eit.getEitLength()), end= "")
        if "-D" in get_eit: print("Dauer: " + str(Eit.getEitLengthInMinutes())+ " Minuten", end = "")

        if "-d" in get_eit or "-D" in get_eit:
            try:
                seen = Cuts.last * 100 / Eit.getEitLengthInSeconds()
                #print(Cuts.last, Eit.getEitLengthInSeconds())
            except:
                seen = 0
            if seen < 5: col = color.norm
            elif seen >= 95: col= color.green
            else: col = color.blue
            print("\t" + str(seen) + "% angeschaut")

if "-S" in get_else:
    print(color.sum + "Anzahl: %i" % sum_e + color.norm + "\n")
    print(color.sum + "Gesamt: %i" % sum + color.norm)
print(color.norm)