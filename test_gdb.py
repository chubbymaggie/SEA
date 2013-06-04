#!/usr/bin/gdb -x

import sys
import gdb

gdb.execute("start")

to_addr = None

while (True):

  gdb.execute("si")
  raw_ins = gdb.execute("disassemble $eip,+0")
  
  print str(raw_ins)
  if (" j" in str(raw_ins)):
    print "jmp!"

  addr = str(gdb.parse_and_eval("$eip")).split(" ")[0]
  
  #print int(addr,16), type(addr)#,raw_ins

#gdb.execute("file " + sys.argv[-1])
#type = gdb.Type(sys.argv[0])
#print "sizeof %s = x" % (sys.argv[0])
