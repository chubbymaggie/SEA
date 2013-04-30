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
from Common      import getTypedValueFromCode
  
class MemAccess:
  def getAccess(self, addr):
    pass  

class MemAccessREIL(MemAccess):
  def __init__(self):
    self.access = dict()
  
  def __str__(self):
    
    counters = self.access.keys()
    counters.sort()
    
    ret = "Memory accesses detected:\n"
    
    for c in counters:
      ret = ret + str(c) + " -> " + str(self.access[c]["type"]) + " : " 
      ret = ret + str(self.access[c]["source"]) + "@" + str(self.access[c]["offset"]) + "\n"
    
    return ret
  
  def getAccess(self, counter):
    
    if counter in self.access:
      return self.access[counter]
    
    return None

  def detectMemAccess(self, reil_code, callstack, inputs, counter):
    
    ins = reil_code[-1]
    
    assert(ins.instruction in ["stm", "ldm"])
    addr_op = ins.getMemReg()
    val = getTypedValueFromCode(reil_code, callstack, inputs, self, addr_op)
    
    if (val.isMem()):
      
      #if self.__isArgMem__(val, callstack.callstack[1]):
      #  print "arg detected at", ins, "with", str(val)
      #  self.access[counter] = self.__getArgMemAccess__(ins, val, callstack.callstack[1])
      #else:
      #print val
      self.access[counter] = self.__getMemAccess__(ins, val)
    elif (val.isImm):
      self.access[counter] = self.__getGlobalMemAccess__(ins, int(val.name))
    
    else:
      assert(0)
      
  def __getMemAccess__(self, ins, val):

    mem_access = dict()
    mem_access["source"] = val.mem_source
    mem_access["offset"] = val.mem_offset
    mem_access["type"]   = ins.instruction
    mem_access["address"]   = ins.address
    
    return mem_access
      
  def __getGlobalMemAccess__(self, ins, offset):
    mem_access = dict()
    mem_access["source"] = "g.0x00000000.0"
    mem_access["offset"] = offset
    mem_access["type"]   = ins.instruction
    mem_access["address"]   = ins.address
    
    return mem_access

