#!/usr/bin/gdb -x

import sys
import gdb

def parse_jmp_addr(raw_ins):
  jmp = raw_ins.split("\n")[1].split("\t")[1].split("<")[0]
  addr = jmp.split(" ")[-2]

  return addr

def getPath(data, size):
  
  jmp_addr = None

  gdb.execute("start", to_string=True)  

  # set initial conditions

  for i in range(0,10): # wait for 10 instructions
    gdb.execute("si", to_string=True)

  gdb.execute("set *(char*) ($ebp-48) = "+str(size)) #
  gdb.execute("set *(char**) ($ebp-28) = "+str(46)) 
  gdb.execute("set *(char**) ($ebp-29) = "+str(10)) 


  while (True):
  
    gdb.execute("si", to_string=True)
    addr = str(gdb.parse_and_eval("$eip")).split(" ")[0]
    #addr = gdb.parse_and_eval("$eip")

    raw_ins = gdb.execute("disassemble $eip,+1", to_string=True)
    raw_ins = str(raw_ins)
 
    if jmp_addr <> None:
      print addr, jmp_addr, addr == jmp_addr
      jmp_addr = None

    #print str(raw_ins)
    if ("j" in raw_ins) and not ("jmp" in raw_ins):
      jmp_addr = parse_jmp_addr(raw_ins)
    elif ("call" in str(raw_ins)):
      break
    elif ("ret" in str(raw_ins)):
      break


for i in range(2,3):
  print "size:", i
  getPath(None, i)

gdb.execute("quit", to_string=True)
