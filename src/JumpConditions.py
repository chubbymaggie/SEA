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

from sys         import exit

from core        import *
from Common      import getPathConditions

#input_vars = ["stdin:", "arg[0]@0:", "arg[1]@0:", "arg[2]@0:"]

def getJumpConditions(trace, addr):
  last_ins = (trace["code"][-1])
  addr = int(addr, 16)
  pos = trace["code"].last - 1
  
  if (last_ins.isJmp() or last_ins.isCJmp()):
    jmp_op = last_ins.operands[2]
    
    if (jmp_op.isVar()):
      
      #print addr  
      trace["final_conditions"] = dict([( jmp_op , ImmOp(str(addr), "DWORD"))])
      (fvars, sol) = getPathConditions(trace, False)
      
      #print sol 
      return (fvars, sol)

    else:
      print "Jump operand (", jmp_op ,") in last instruction (", last_ins.instruction, ") is not variable!" 
      return (set(), None)
    
  else:
    exit("Last instruction ( "+ str(last_ins)+ " ) is not a jmp")
