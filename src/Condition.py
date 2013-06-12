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

import sys

try:

  sys.path.append("z3py/build/")
  import z3

except:
  sys.exit("You should run bootstrap.sh to download and compile z3 support") 

from core import *
from MemVars import Memvars

def mkArray(name):
  return z3.Array(name, z3.BitVecSort(16), z3.BitVecSort(8))

def mkByteList(op):
  locs = op.getLocations()
  
  if (len(locs) > 1):
    return map(lambda b: z3.BitVec(str(b),8), locs)
  else:
    return [z3.BitVec(str(locs[0]),8)]


def mkByteListVar(op):
  locs = op.getLocations()
  
  if (len(locs) > 1):
    return (map(lambda b: z3.BitVec(str(b),8), locs))
  else:
    return [z3.BitVec(str(locs[0]),8)]

def mkByteVar(op):
  locs = op.getLocations()
  
  if (len(locs) > 1):
    return z3.Concat(map(lambda b: z3.BitVec(str(b),8), locs))
  else:
    return z3.BitVec(str(locs[0]),8)

def mkByteListConst(imm):
  locs = imm.getLocations()
  
  if (len(locs) > 1):
    return (map(lambda b: z3.BitVecVal(str(b),8), locs))
  else:
    return [ z3.BitVecVal(str(locs[0]),8)]

#def mkByteConst(imm):
#  locs = imm.getLocations()
  
#  if (len(locs) > 1):
#    return z3.Concat(map(lambda b: z3.BitVecVal(str(b),8), locs))
#  else:
#    return z3.BitVecVal(str(locs[0]),8)

def mkConst(imm):
  return z3.BitVecVal(imm.getValue(),imm.size)

class Condition:

  def __apply_ssa(self, op):
    if op |iss| RegOp:
      return self.ssa_map[str(op)]
    return op

  def __init__(self, ins, ssa_map):
    self.ins = ins
    
    rreg = self.ins.getReadRegOperands()
    wreg = self.ins.getWriteRegOperands()
    
    self.read_operands = self.ins.getReadOperands()
    self.write_operands = self.ins.getWriteOperands()
    
    self.ssa_map = ssa_map    
    self.read_operands = map(lambda o: self.__apply_ssa(o), self.read_operands)
    self.write_operands = map(lambda o: self.__apply_ssa(o), self.write_operands)
  
  def getEq(self):
    assert(0)
    return []

  def getOperands(self, ops, concat = True):
   
    rops = [] 
    
    for op in ops:
      #print op
      if (op.isVar()):
        rops.append(mkByteVar(op))
      else:
        rops.append(mkConst(op))
    #for r in rops:
    #  print r, 

    return rops

class Call_Cond(Condition):
  def getEq(self):
    assert(0)
    return []
 
class  Jcc_Cond(Condition):
  def getEq(self):
    src = self.getOperands(self.read_operands)[0]
    
    if (self.ins.getBranchTaken() == "0"): # hack to know which branch was taken!
      return [(src == 0)] # False branch
    else: 
      return [(src <> 0)] # True branch
 
class  Str_Cond(Condition):
 def getEq(self):

   src = self.getOperands(self.read_operands)[0]
   dst = self.getOperands(self.write_operands)[0]
   
   return [(src == dst)]

class  Add_Cond(Condition):
 def getEq(self):

   src1,src2 = self.getOperands(self.read_operands)
   dst = self.getOperands(self.write_operands)[0]
   
   return [(src1 + src2 == dst)]


class  Sub_Cond(Condition):
 def getEq(self):
   
   src1,src2 = self.getOperands(self.read_operands)
   dst = self.getOperands(self.write_operands)[0]
   
   return [(src1 - src2 == dst)]


class  Mul_Cond(Condition):
 def getEq(self):
   
   src1,src2 = self.getOperands(self.read_operands)
   dst = self.getOperands(self.write_operands)[0]
   
   return [(src1 * src2 == dst)]

class  And_Cond(Condition):
 def getEq(self):

   src1,src2 = self.getOperands(self.read_operands)
   dst = self.getOperands(self.write_operands)[0]
   
   #print "src1:", src1
   #print "src2:", src2
   
   return [(src1 & src2 == dst)]

class  Or_Cond(Condition):
 def getEq(self):
  
   src1,src2 = self.getOperands(self.read_operands)
   dst = self.getOperands(self.write_operands)[0]
   
   return [(src1 | src2 == dst)]


class  Xor_Cond(Condition):
 def getEq(self):

   src1,src2 = self.getOperands(self.read_operands)
   dst = self.getOperands(self.write_operands)[0]
   
   return [(src1 ^ src2 == dst)]

class  Shift_Cond(Condition):
 def getEq(self):
   #print self.read_operands[1] 
   sdir = ""
   
   src1,src2 = self.getOperands(self.read_operands)
   dst = self.getOperands(self.write_operands)[0]
   n =  self.read_operands[1].getValue()

   if n > 0:
     sdir = "left"
   elif n < 0:
     sdir = "right"
     #self.read_operands[1].name = self.read_operands[1].name.replace("-","") #ugly hack!
   else:
     sdir = "null"
   
   #print self.read_operands[1].name
  

   #print sdir, src2.as_long()
   if sdir == "right": 
     return [(z3.Extract(self.write_operands[0].getSizeInBits()-1, 0,z3.LShR(src1,-n)) == dst)]
   elif sdir == "left":
     return [(z3.Extract(self.write_operands[0].getSizeInBits()-1, 0,(src1 << n)) == dst)]
   elif sdir == "null":
     return [(src1 == dst)]
   else:
     assert(False)

class  Bisz_Cond(Condition):
 def getEq(self):
   src = self.getOperands(self.read_operands)[0]
   dst = self.getOperands(self.write_operands)[0]
   
   return [z3.If(src == 0, dst == 1, dst == 0)]

class  Ldm_Cond(Condition):
  def getEq(self):
    
    conds = []
    
    src = self.ins.getReadMemOperands()[0]
    srcs = src.getLocations()
    
    dst = (self.write_operands)[0]
    if dst.isVar():
      dsts = mkByteListVar(dst)    
    else:
      dsts = mkByteListConst(dst)
    
    for (src,dst) in zip(srcs, dsts):
      sname = Memvars.read(src)
      array = mkArray(sname)
      conds.append(array[src.getIndex()] == dst)
    
    return conds
    
class  Stm_Cond(Condition):
  def getEq(self):
    
    src = self.read_operands[0]
    
    if src.isVar():
      srcs = mkByteListVar(src)    
    else:
      srcs = mkByteListConst(src)
       
    dst = self.write_operands[0]
    dsts = dst.getLocations()
    
    conds = []
    
    old_sname, new_sname = Memvars.write(dsts[0])

    #array = mkArray(old_sname)
    #new_array = mkArray(new_sname)

    old_array = mkArray(old_sname)
    array = mkArray(new_sname)

    for (src,dst) in zip(srcs, dsts):
      array = z3.Store(array, dst.getIndex(), src)
      
    conds = [(old_array == array)]

    return conds


## exploit conditions

#class  Write_with_stm(Condition):
#  def getEq(self, value, address):
#    op_val,op_addr = self.getOperands(self.read_operands)
#    print [op_val == value, op_addr == address]
#    return [op_val == value, op_addr == address]
  
# generic conditions  
  
class  Eq(Condition):
  def __init__(self, pins, ssa):
    pass
  def getEq(self, x, y):
    
    assert(x.getSizeInBytes() == y.getSizeInBytes())
    
    conds = []
    
    if x.isMem() and y.isMem():
      
      srcs = x.getLocations()
      dsts = y.getLocations()
      
      for (src,dst) in zip(srcs, dsts):
        sname = Memvars.read(src)
        src_array = mkArray(sname)
        
        sname = Memvars.read(dst)
        dst_array = mkArray(sname)
        
        conds.append(src_array[src.getIndex()] == dst_array[dst.getIndex()])
      
      return conds
    
    elif x.isMem() and y |iss| ImmOp:
      #assert(0)
      srcs = x.getLocations()
      dsts = mkByteListConst(y)
    
      for (src,dst) in zip(srcs, dsts):
        #print str(x)
        sname = Memvars.read(src)
        src_array = mkArray(sname)
        conds.append(src_array[src.getIndex()] == dst)
    
      return conds
    else:

      src, dst = self.getOperands([x,y])      
      return [src == dst]  


# Func conditions
class  Call_Gets_Cond(Condition):
  def __init__(self, funcs, ssa):
    self.dst = funcs.write_operands[0]
    self.size = funcs.internal_size
  
  def getEq(self, mlocs):
    
    src = InputOp("stdin", 1)
    src.size_in_bytes = self.size

    srcs = mkByteListVar(src)    
       
    dst = self.dst #self.func.write_operands[0]
    dsts = dst.getLocations()
    
    conds = []
    
    old_sname, new_sname = Memvars.write(dsts[0])

    #array = mkArray(old_sname)
    #new_array = mkArray(new_sname)

    old_array = mkArray(old_sname)
    array = mkArray(new_sname)

    for (src,dst) in zip(srcs, dsts):
      if dst in mlocs:
        array = z3.Store(array, dst.getIndex(), src)
      
      conds.append(src <> 10)
      conds.append(src <> 0)
 
    conds.append((old_array == array))
    return conds
    #r = []

    #old_sname, new_sname, offset = Memvars.write(self.dst)
      
    #old_array = mkArray(old_sname)
    #array = mkArray(new_sname)

    #for i in range(self.size):
      
      #op = Operand(self.dst.mem_source+"@"+str(offset+i), "BYTE")
      
      #if (op in mvars):
      #  array = z3.Store(array, offset+i, z3.BitVec("stdin:"+str(i)+"(0)",8))
        
      #r.append(z3.BitVec("stdin:"+str(i)+"(0)",8) <> 10)
      #r.append(z3.BitVec("stdin:"+str(i)+"(0)",8) <> 0)
      
    #r.append((old_array == array))

    #return r

"""
class  Call_Strlen_Cond(Condition):
  def __init__(self, funcs, ssa):
  
  
    self.ssa_map = ssa_map    
    self.read_operands = map(lambda o: self.__apply_ssa(o), self.read_operands)
    self.write_operands = map(lambda o: self.__apply_ssa(o), self.write_operands)
    
    self.src    = self.read_operands[0]
    self.retreg = self.write_operands[0]
    self.size = funcs.internal_size
    
  
  def getEq(self, mvars):
    
    retreg = self.getOperands([self.retreg])
    return retreg == self.size
"""

class  Call_Strcpy_Cond(Condition):
  def __init__(self, funcs, ssa):
    self.src =  funcs.read_operands[0]#funcs.parameter_vals[1]
    self.dst =  funcs.write_operands[0]#funcs.parameter_vals[0]
    self.size = funcs.internal_size
  
  def getEq(self, mlocs):
    #assert(0)
    #for loc in mlocs:
    #  print loc, "--",
    #print ""
    r = []
    src = self.src
    srcs = src.getLocations()
    sname = Memvars.read(srcs[0])

    read_array = mkArray(sname)

    dst = self.dst 
    dsts = dst.getLocations()
    
    old_sname, new_sname = Memvars.write(dsts[0])
    
    old_array = mkArray(old_sname)
    array = mkArray(new_sname)

    for (src_loc,dst_loc) in zip(srcs, dsts):

      read_val = z3.Select(read_array, src_loc.getIndex()) 
      if dst_loc in mlocs:
        array = z3.Store(array, dst_loc.getIndex(), read_val)
      
      r.append(read_val <> 0)
 
    r.append((old_array == array))
    #print r
    #assert(0)
    return r


    #print self.src, self.dst
    
    #if (self.src.isReg()):
    #  src = self.src.name
    #  self.src.size = self.size
    #  srcs = self.getOperands([self.src])
    #  print srcs
    #else:
    #  assert(0)
  
    #old_sname, new_sname, offset = Memvars.write(self.dst)
      
    #old_array = mkArray(old_sname)
    #array = mkArray(new_sname)
    
    #for i in range(self.size):
      
    #  dst_op = Operand(self.dst.mem_source+"@"+str(offset+i), "BYTE")
    #  src_var = z3.BitVec(src+":"+str(i)+"(0)",8)
      
    #  if (dst_op in mvars):
    #    array = z3.Store(array, offset+i, src_var)

    #  r.append(src_var <> 0)
      
    #r.append((old_array == array))

    return r


conds = {
    "call" : Call_Cond,
    
    "gets" : Call_Gets_Cond,
    "strcpy" : Call_Strcpy_Cond,
    
    "jcc": Jcc_Cond,
    "str": Str_Cond,
    "and": And_Cond,
    "or": Or_Cond,
    "xor": Xor_Cond,
    "bsh": Shift_Cond,
    "add": Add_Cond,
    "sub": Sub_Cond,
    "mul": Mul_Cond,
    "bisz": Bisz_Cond,
    
    "ldm": Ldm_Cond,
    "stm": Stm_Cond,
    }
