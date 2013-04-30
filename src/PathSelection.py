"""
    This file is part of SEA.

    SEA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SEA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SEA.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2013 by neuromancer
"""

import src.core

def help_path(filename):
  print "To select interactively a path in", filename, " use:"
  print "t to continue with the true branch."
  print "f to continue with the false branch."
  print "i to step in."
  print "o to step out."
  print "e to finish recording a path."
  
def ask(values):
  
  i = None
  
  while (not (i in values)):
    if i <> None:
      print "Invalid selection"
    i = raw_input(">")
  
  return i
  
def selectPath(filename):

  pr = src.core.BapProgram(filename)
  bap_path = []
  help_path(filename)

  #def readRelocTable(filename):
  #  openf = open(filename)
  #  r = dict()
  #  for ln in openf.readlines():
  #    (addr,func) = ln.replace("\n","").split(" ")
  #    r[hex(int(addr,16))] = func
  #  
  #  return r

  #print pr
  #reloc = readRelocTable("tests/bap/httpd.rel")
  #callstack = []
  #assert(False)
  
  for (addr, ins) in pr:
    #print addr, ">", ins.ins
    bap_path.append((addr, ins))
  
    if ins.isCall():
      print "call detected! (", ins.branchs[0], ")"
      i = ask(["i", "o", "e"])
      
      if (i == "e"):
	break
      elif (i == "i"):
        pr.stepIn()
      elif (i == "o"):
        pass
    
    #if str(ins.branchs[0]) == "0x8048890":
    #  print "exit reached!"
    #  break
    #elif str(ins.branchs[0]) == "0x8048fbe":
    #  print "process client reached!"
      #pr.stepIn()
    #i = raw_input(">")
    #if int(i) == 1:
    #  pr.stepIn()
  
    if ins.isCJmp():
    #print ins.raw
      print "conditional jmp detected!" #(", ins.branchs[0], ")"
      i = ask(["t", "f", "e"])
      
      if (i == "e"):
	break
      elif i == "f":
        pr.selectFalseBranch()
      elif i == "t":
        pr.selectTrueBranch()

  #else:
  ##pass
    #print " "
    
  print bap_path
#path = src.core.Path(map(lambda p: p[1], bap_path),0,len(bap_path))
#print "Path selected:"
#for (addr, ins) in bap_path:
#  print str(addr)+":", ins.ins, ins.read_operands
  #last_current = pr.current
    #break
    
#for ins in path[10:15]:
  #print ins.ins