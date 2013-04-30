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

from core        import *
from Common      import getPathConditions

input_vars = ["stdin:", "arg[0]@0:", "arg[1]@0:", "arg[2]@0:"]

def getJumpConditions(trace, addr):
  last_ins = (trace["code"][-1])
  addr = int(addr, 16)
  pos = trace["code"].last - 1
  
  if (last_ins.instruction == "jcc"):
    jmp_op = last_ins.operands[2]
    
    if (jmp_op.isVar()):
      
      #print addr  
      trace["final_conditions"] = dict([( jmp_op , Operand(str(addr), "DWORD"))])
      sol = getPathConditions(trace)
      
      if (sol <> None):
        print "SAT conditions found!"
        filename = last_ins.instruction + "[" + str(pos)  +"]"
        dumped = sol.dump(filename,input_vars)
        for filename in dumped:
          print filename, "dumped!"
      else:
        print "Impossible to jump to", hex(addr), "from", last_ins.instruction, "at", pos
    else:
      print "Jump operand (", jmp_op.name ,") in last instruction (", last_ins.instruction, ") is not variable!" 
      return None
    
  else:
    print "Last instructions (", last_ins, ") is not a jmp" 
    return None
