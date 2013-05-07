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
  
print "stack:",Callstack(path)
print getType(path[0:8], RegOp("t1",32), Type("Data32"))
