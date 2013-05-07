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

#foldr = lambda l,f,e: reduce(f, l, e)
concatSet = lambda l: reduce(set.union, l, set())

from core import *

def getType(inss, op, initial_type):
  assert(len(inss) > 0)
  
  # code should be copied and reversed
  inss.reverse()
  
  # counter is set
  counter = len(inss)
  
  # we will track op
  mlocs = set(op.getLocations())
  
  # at first, final type is the initial type    
  final_type = initial_type
  
  for ins in inss:
    print str(ins)
    ins_write_vars = map(lambda op: set(op.getLocations()), ins.getWriteVarOperands())
    write_locs = concatSet(ins_write_vars)
    
    ins_read_vars  = map(lambda op: set(op.getLocations()), ins.getReadVarOperands())
    read_locs  = concatSet(ins_read_vars)
    
    for loc in mlocs:
      print loc
          
    if len(write_locs.intersection(mlocs)) > 0: 
      
      mlocs = mlocs.difference(write_locs) 
      mlocs = read_locs.union(mlocs)
      #mvars = set(filter(lambda o: o.name <> "ebp", mvars))
      """
      smt_conds.add(condition.getEq())
      """
    #counter = counter - 1
    
  
  """
  for iop in initial_values.keys():
    if not (iop in ssa):
      del initial_values[iop]
    
  ssa_map = ssa.getMap(set(), set(), set(initial_values.keys()))
  eq = Eq(None, None)
    
  for iop in initial_values:
    smt_conds.add(eq.getEq(ssa_map[iop.name],initial_values[iop]))
  
  op.name = op.name+"_0"
  smt_conds.solve()
  
  return smt_conds.getValue(op)
  """
  return None

"""
class Callstack:
  def __init__(self, reil_code):
    
    # The first instruction should be a call
    self.callstack = [None]
    self.stack_diff = []
    
    self.index = 0
    
    # aditional information need to compute the callstack
    self.calls = [None]
    self.esp_diffs = [None]
    self.reil_code = reil_code
    reil_size = len(reil_code)
    start = 0  
  
    for (end,ins) in enumerate(self.reil_code):
      if (ins.isCall() and ins.called_function == None) or ins.isRet():
        self.__getStackDiff__(ins, reil_code[start:end])
        start = end
        
    if (start <> reil_size-1):
      ins = reil_code[start]
      self.__getStackDiff__(ins, reil_code[start:reil_size-1])
      
    self.index = len(self.callstack) - 1
  
  def __str__(self):
    ret = ""
    for (addr, sdiff) in zip(self.callstack, self.stack_diff):
      if (addr <> None):
        ret = ret + " " + hex(addr) + "[" +str(sdiff)+"]"
    
    return ret
  
  def reset(self):
    self.index = 0
  
  def nextInstruction(self, ins):
    if (ins.isCall() and ins.called_function == None) or ins.isRet():
      self.index = self.index + 1
  
  
  def prevInstruction(self, ins):
    if (ins.isCall() and ins.called_function == None) or ins.isRet():
      self.index = self.index - 1
  
  def currentCall(self):
    return self.callstack[self.index]
    
  def currentStackDiff(self):
    return self.stack_diff[self.index]
  
  def currentCounter(self):
    return 1 # TODO!
  
  def firstCall(self):
    return self.index == 1
  
  def convertStackMemOp(self, op):
    self.index = self.index - 1
    
    mem_source =  "s."+hex(self.currentCall())+"."+str(self.currentCounter())
    if self.index == 1:
      mem_offset = (op.mem_offset)+self.currentStackDiff()-4#+16
    else:
      mem_offset = (op.mem_offset)+self.currentStackDiff()#+16
    name = mem_source+"@"+str(mem_offset)
    
    self.index = self.index + 1
    
    return Operand(name,"BYTE", mem_source, mem_offset)
  
  def __getStackDiff__(self, ins, reil_code):
    
    addr = ins.address
    if ins.isCall():
      call = int(addr, 16)
      print "addr of call:", call
      esp_diff = self.__getESPdifference__(reil_code, 0) 
        
      self.calls.append(call)
      self.callstack.append(call)
        
      self.stack_diff.append(esp_diff)
      self.esp_diffs.append(esp_diff)
      
    elif ins.isRet():
        
      if (reil_code[0].isCall()):
        self.stack_diff.append(self.__getESPdifference__(reil_code, 0))
      else:
        self.calls.pop()
        self.esp_diffs.pop()
          
        call = self.calls[-1]
        esp_diff = self.esp_diffs[-1]
          
        self.stack_diff.append(self.__getESPdifference__(reil_code, esp_diff)) 
        self.callstack.append(call)
    else:
      assert(False)
  
  def __getESPdifference__(self, reil_code, initial_esp):
    if len(reil_code) == 0:
      return initial_esp
    
    esp_op = RegOp("esp","DWORD")
    initial_values = dict([ (esp_op, ImmOp(str(0), "DWORD"))])
    return getValueFromCode(reil_code, initial_values, esp_op)+ initial_esp
"""
