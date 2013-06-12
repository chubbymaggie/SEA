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

from core import *
from Condition   import *

def getInitialConditionsArgs(callstack):
  
  initial_values_at_call = dict()
  
  name = hex(callstack.currentCall())
  
  einfo = dict() 
  einfo["source.name"]=name
  einfo["source.index"]=callstack.currentCounter()
  
  arg_v = MemOp(name,"DWORD", offset=12)
  arg_v.type = Type("Ptr32",None, einfo=einfo)
  
  initial_values_at_call[arg_v] = ImmOp(str(0), "DWORD")
  
  einfo = dict() 
  einfo["source.name"]="argv[]"
  einfo["source.index"]=0
  
  arg_v = MemOp(name,"DWORD")
  arg_v.type = Type("SPtr32",None, einfo=einfo)
  
  initial_values_at_call[arg_v] = ImmOp(str(0), "DWORD")

  
  return initial_values_at_call


def getInitialConditionsCall(callstack):
  
  initial_values_at_call = dict()
  
  if callstack.index == 1:
    esp_val = 4
    
    #for i in range(0,40):
      #arg_i = Operand("argv[]@"+str(i),"BYTE", mem_source = "argv[]", mem_offset=i)
      #initial_values_at_call[arg_i] = Operand(str(0), "BYTE")
    
    #print ""
  else:
    esp_val = 8
 
  ebp_val = 0
  
  esp_op = RegOp("esp","DWORD")
  ebp_op = RegOp("ebp","DWORD")
  
  
  initial_values_at_call[esp_op] = ImmOp(str(esp_val), "DWORD")
  initial_values_at_call[ebp_op] = ImmOp(str(ebp_val), "DWORD")
  
  return initial_values_at_call

def getInitialConditionsAlloc():
  ret_op = RegOp("eax","DWORD")
  ret_val = 0
  initial_values_at_alloc = dict()
  initial_values_at_alloc[ret_op] = ImmOp(str(ret_val), "DWORD")
  
  return initial_values_at_alloc

def setInitialConditions(ssa, initial_values, smt_conds):
  ssa_map = ssa.getMap(set(), set(), set(initial_values.keys()))
  eq = Eq(None, None)
  
  for iop in initial_values:
    
    #if ":" in iop.name:
    #  smt_conds.add(eq.getEq(iop,initial_values[iop]))
    if (iop |iss| RegOp):
      #assert(0)
      #print eq.getEq(ssa_map[iop.name],initial_values[iop]), "-"
      smt_conds.add(eq.getEq(ssa_map[iop.name],initial_values[iop]))
    elif (iop.isMem()):
      smt_conds.add(eq.getEq(iop,initial_values[iop]))
    else:
      assert(False)

#def detectType(mvars, ins, counter, callstack):
  
  #if (len(mvars) == 0):
    #return None
  
  ## dection of parameters of main
  
  #name = "s."+hex(callstack.callstack[1])+".1"
  
  ## argv
  #argv_bytes = []
  
  #for i in range(12,16):
    #argv_bytes.append(Operand(name+"@"+str(i),"BYTE"))
  
  #argv_bytes = set(argv_bytes) 
  
  
  #if argv_bytes.issubset(mvars):
    #return "argv[]"
  
  ### argc
  ##argc_bytes = []
  ##
  ##for i in range(8,12):
  ##  argc_bytes.append(Operand(name+"@"+str(i),"BYTE"))
  ##
  ##argc_bytes = set(argv_bytes) 
  ##
  ##if argc_bytes.issubset(mvars):
  ##  return "argc"
  
  ## argv[0], argv[1], ... argv[10]
  #for i in range(0,40,4):
    #op = Operand("argv[]@"+str(i),"BYTE")
    #if op in mvars:
      #return "arg["+str(i / 4)+"]"
  
  #if ins.isCall() and ins.called_function == "malloc":
    
    ## heap pointers
    #if set([Operand("eax","DWORD")]).issubset(mvars):
      #return "h."+"0x"+ins.address+"."+str(counter)
  
  #elif ins.isCall() and ins.called_function == None:
    
    ## stack pointers
    #if mvars.issubset(set([Operand("esp", "DWORD"), Operand("ebp", "DWORD")])):
      #return "s."+hex(callstack.currentCall())+"."+str(callstack.currentCounter())

  ## No type deduced
  #return None 

#def mkVal(val_type,val):
  #if val_type == "imm":
    #return Operand(str(val), "")
  #elif "s." in val_type or "h." in val_type or "arg" in val_type:
    #return Operand(val_type+"@"+str(val), "", mem_source = val_type, mem_offset=val)
  #else:
    #assert(0)

def removeTrack(ops, mvars, mlocs):

  for op in ops:
    mvars.remove(op)
  
    for loc in op.getLocations():
      mlocs.remove(loc)
    
def addAditionalConditions(mvars, mlocs, ins, ssa, callstack, smt_conds):
  
  if len(mvars) == 0:
    return mvars
  
  # auxiliary eq condition
  eq = Eq(None, None)
  
 
    #name = hex(callstack.currentCall())
    #for i in range(12,16):
      
      #argv_bytes.append(MemOp(name+"@"+str(i),"BYTE"))
  
  # if the instruction was a call
  if ins.isCall() and ins.called_function == "malloc":

    if (RegOp("eax","DWORD") in mvars):
      initial_values_at_alloc = getInitialConditionsAlloc()
      setInitialConditions(ssa, initial_values_at_alloc, smt_conds)
      removeTrack([RegOp("eax","DWORD")], mvars, mlocs)
      #mvars.remove(RegOp("eax","DWORD"))
      
  elif ins.isCall() and ins.called_function == None:
    initial_values_at_call = getInitialConditionsCall(callstack)
      
    
    for iop in initial_values_at_call.keys():
      #print "iop:",iop
      if not (iop in mvars):  
        del initial_values_at_call[iop]
      
      
    setInitialConditions(ssa, initial_values_at_call, smt_conds)
    removeTrack(initial_values_at_call.keys(), mvars, mlocs)
    
    if (ins.getCounter() == 0):
    
      initial_values = getInitialConditionsArgs(callstack)
      setInitialConditions(ssa, initial_values, smt_conds)
    
    #mvars = set(filter(lambda o: not (o in initial_values_at_call.keys()), mvars))
    
    
      
    #new_mvars = set()
    #for v in mvars:
      ## we convert stack memory variables from one frame to the previous one
      #if callstack.currentCounter()>1 and v.isStackMem() and v.mem_offset >= 4: 
        #eop = callstack.convertStackMemOp(v)
        #smt_conds.add(eq.getEq(v,eop))
        #new_mvars.add(eop)
      #else:
        #new_mvars.add(v)
      
    #mvars = set(filter(lambda o: not (o.isStackMem() and o.mem_offset >= 4), mvars))
    #mvars = mvars.union(new_mvars)
  
  return mvars
  
