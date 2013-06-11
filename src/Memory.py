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
from Common      import getValueFromCode
from TypeSlicer  import getTypedValue
  
class MemAccess:
  def __init__(self):
    self.access = dict()
  
  def __str__(self):
    
    counters = self.access.keys()
    counters.sort()
    
    ret = "Memory accesses detected:\n"
    
    for c in counters:
      pt, offset = self.access[c]["access"]
      ret = ret + str(c) + " -> " + str(self.access[c]["type"]) + " : " 
      ret = ret + str(pt) + "@" + str(offset) + "\n"
    
    return ret
  
  def getAccess(self, counter):
    
    if counter in self.access:
      return self.access[counter]
    
    return None

  def detectMemAccess(self, reil_code, callstack, inputs, counter):
    #print reil_code.first, reil_code.last
    ins = reil_code[-1]
    
    assert(ins.isReadWrite()) 
    addr_op = ins.getMemReg()
    #pt = getType(reil_code, callstack, self, addr_op, Type("Ptr32", None)) 
    
    #if str(pt) == "Ptr32":
    #  pt = Type("GPtr32", None)
    #  pt.addTag("source.name","0x00000000")
    #  pt.addTag("source.index",0)
    
    # we reset the path
    #reil_code.reverse()
    #reil_code.reset()
    
    (val,pt) = getTypedValue(reil_code, callstack, self, addr_op, Type("Ptr32", None))
    
    self.access[counter] = self.__mkMemAccess__(ins, pt, val)
      
  def __mkMemAccess__(self, ins, ptype, offset):

    mem_access = dict()
    mem_access["type"]    = ins.instruction
    mem_access["address"] = ins.address
    mem_access["access"]   = (ptype, offset)
    
    return mem_access
