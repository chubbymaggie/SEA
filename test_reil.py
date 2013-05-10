from src.core import *
from src.Callstack import Callstack
from src.TypeSlicer import getType

path = ReilPath("tests/reil/stack1_vs2005.reil",0,100)

#for ins in path:
#  print ins
#  for op in ins.getReadOperands():
#    print op.size_in_bytes, "->",
#    for loc in op.getLocations():
#      print loc, "-",
#    print ""
callstack  = Callstack(path)  
print "stack:",callstack
print callstack.calls

callstack.reset()

for ins in path[0:9]:
  callstack.nextInstruction(ins)

path.reset()
  
print getType(path[0:9], callstack, RegOp("t2",32), Type("Data32", None))
