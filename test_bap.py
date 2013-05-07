
import random
import src.core
pr = src.core.BapProgram("tests/bap/httpd.json")
bap_path = []

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
  print addr, "->", ins.ins
  bap_path.append((addr, ins))
  
  print ins.isCall()
  if ins.isCall():
    print "call detected! (", ins.branchs[0], ")"
    if str(ins.branchs[0]) == "0x8048890":
      print "exit reached!"
      break
    elif str(ins.branchs[0]) == "0x8048fbe":
      print "process client reached!"
      #pr.stepIn()
      break
     
    #i = raw_input(">")
    #if int(i) == 1:
    #  pr.stepIn()
  
  if ins.isCJmp():
    #print ins.raw
      i = raw_input(">")
      if int(i) == 0:
        pr.selectFalseBranch()
      else:
        pr.selectTrueBranch()

  else:
    pass
    #print " "
    

path = src.core.Path(map(lambda p: p[1], bap_path),0,len(bap_path))
print "Path selected:"
#for (addr, ins) in bap_path:
#  print str(addr)+":", ins.ins, ins.read_operands
  #last_current = pr.current
    #break
    
for ins in path[10:15]:
  print ins.ins
    
#print pr.labels
#print pr.code
