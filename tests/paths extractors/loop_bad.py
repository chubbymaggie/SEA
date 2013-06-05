#!/usr/bin/gdb -x

import sys
import gdb
import random

#def parse_jmp_addr(raw_ins):
#  jmp = raw_ins.split("\n")[1].split("\t")[1].split("<")[0]
#  addr = jmp.split(" ")[-2]

#  return addr

def getRandomData(values, size):
  data = ""
  value_size = len(values)
  for i in range(size):
    data = data + values[random.randint(0,value_size-1)]

  return data

def setData(data, data_addr, size, size_addr):

  assert(len(data) == size)
  gdb.execute("set *(int*) ("+size_addr+") = (int) "+str(size)) #

  for i in range(size):
    #print "set *(char*) ("+data_addr+"+"+str(i)+") = (char) "+str(ord(data[i]))
    gdb.execute("set *(char*) ("+data_addr+"+"+str(i)+") = (char) "+str(ord(data[i])))


def getPath(data, size):
  
  was_jmp = False
  r = []
  gdb.execute("start", to_string=True)  

  # set initial conditions

  for i in range(0,10): # wait for 10 instructions
    gdb.execute("si", to_string=True)

  setData(data,"$ebp-29", size, "$ebp-48")
  while (True):
  
    gdb.execute("si", to_string=True)
    addr = str(gdb.parse_and_eval("$eip")).split(" ")[0]
    #addr = gdb.parse_and_eval("$eip")

    raw_ins = gdb.execute("disassemble $eip,+1", to_string=True)
    raw_ins = str(raw_ins)
 
    if was_jmp:
      #print "hola!"
      r.append(addr)#, addr == jmp_addr
      was_jmp = False

    #print str(raw_ins)
    if ("j" in raw_ins) and not ("jmp" in raw_ins):
      was_jmp = True
      #jmp_addr = parse_jmp_addr(raw_ins)
    elif ("call" in str(raw_ins)):
      break
    elif ("ret" in str(raw_ins)):
      break

  return r

import csv
import random

with open('loop_bad.csv', 'wb') as csvfile:
  pathwriter = csv.writer(csvfile)
  path_set = set()
  for i in range(100): 
    for size in range(2,11):
      #print "size:", i
      path = getPath(getRandomData([".","\n"], size), size)
      path_str = str(path)

      if not (path_str in path_set):
        pathwriter.writerow(path)
        path_set.add(path_str)
      

gdb.execute("quit", to_string=True)
