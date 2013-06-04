#!/usr/bin/gdb -x

import sys
import gdb

gdb.execute("start")

last_eip = None
eip = None 

def parse_jmp_addr(raw_ins):
  jmp = raw_ins.split("\n")[1].split("\t")[1].split("<")[0]
  addr = jmp.split(" ")[-2]

  return addr

# prelude
for i in range(0,10):
  gdb.execute("si")

gdb.execute("set *(char*) ($ebp-48) = 0x1")
jmp_addr = None

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
   
  #print int(addr,16), type(addr)#,raw_ins

#gdb.execute("file " + sys.argv[-1])
#type = gdb.Type(sys.argv[0])
#print "sizeof %s = x" % (sys.argv[0])
