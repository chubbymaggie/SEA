"""
   Copyright (c) 2013 neuromancer
   All rights reserved.
   
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions
   are met:
   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
   3. The name of the author may not be used to endorse or promote products
      derived from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
   IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
   IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
   NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from pkgs.pyparsing import Word, Literal, alphas, alphanums, delimitedList
#from Operand import *
from NewOperand import *
from Instruction import Instruction

address         = Word( alphanums).setResultsName("address")
colon           = Literal( ":" )
instruction     = Word( alphas ).setResultsName("instruction")
left_sbracket   = Literal("[")
right_sbracket  = Literal("]")
operand         = Word( alphanums+"-_" ).setResultsName("operand")
size            = Word( alphas ).setResultsName("size")
no_operand      = Literal( "EMPTY" ).setResultsName("operand") 

aug_operand = (size + operand) | no_operand

comma           = Literal(",")
body            = aug_operand + comma + aug_operand + comma + aug_operand
body            = body.setResultsName("augmented_operands")

reil = address + colon + instruction + left_sbracket + body + right_sbracket

# Quick detection of operand
def RegImmNoOp((name,size)):
  
  if name == "EMPTY":
    return NoOp(name,size)
  
  try:
    y = int(name)
    return ImmOp(name,size)
  except ValueError:
    return RegOp(name,size)


class REILInstruction(Instruction):
  def __init__(self, raw_ins, mem_regs = True):
    
    pins = reil.parseString(raw_ins)
    self.address = pins.address
    self.instruction = pins.instruction
    self.operands = []
    
    # for memory instructions
    self.mem_reg = None
    
    # for call instructions
    self.called_function = None
    
    aopers = pins.augmented_operands
    for (i,x) in enumerate(aopers):
       if x == ",":
        self.operands.append((aopers[i-1], aopers[i-2]))
    self.operands.append((aopers[-1], aopers[-2]))
    
    self.read_operands = []
    self.write_operands = []
    
    # ldm: op_2 = [op_0]
    if (pins.instruction == "ldm"):
      
      
      self.write_operands = [RegImmNoOp(self.operands[2])]
      
      name, size = self.operands[0]
      t = RegImmNoOp((name,size))
      
      if (t |iss| ImmOp):
        self.mem_reg = AddrOp(name, size)
        #self.read_operands = [pAddrOp(name, size)]
      elif (t |iss| RegOp):
        self.mem_reg = RegOp(name, size)
        #self.read_operands = [pRegOp(name, size)]
      else:
        assert(False)
      
    # stm: [op_2] = op_0
    elif (pins.instruction == "stm"):
      
      self.read_operands.append(RegImmNoOp(self.operands[0]))
      name, size = self.operands[2]
      t = RegImmNoOp((name,size))
      
      if (t |iss| ImmOp):
        self.mem_reg = AddrOp(name, size)
        #self.write_operands = [pAddrOp(name, size)]
      elif (t |iss| RegOp):
        self.mem_reg = RegOp(name, size)
        #self.write_operands = [pRegOp(name, size)]
      else:
        assert(False)
      
    #  self.mem_reg = self.operands[2]
      
    elif (pins.instruction == "jcc"):
      #pass
      self.operands = map(RegImmNoOp, self.operands)
      self.read_operands  = filter(lambda o: not (o |iss| NoOp), self.operands[0:3])
      self.write_operands = []
      
    elif (pins.instruction == "call"):
      
      #print "n:", self.operands[0].name
      #print self.operands[0].name
      if (self.operands[0][0] <> "EMPTY"):
         self.called_function = self.operands[0][0]
      
    else:
      
      self.operands = map(RegImmNoOp, self.operands)
      
      self.read_operands  = filter(lambda o: not (o |iss| NoOp), self.operands[0:2])
      self.write_operands = filter(lambda o: not (o |iss| NoOp), self.operands[2:3])
      
    self.fixOperandSizes()
      
  def fixOperandSizes(self):
    
    if self.instruction in ["call", "bisz", "bsh", "stm", "ldm", "jcc"]:
      return
    #print self.instruction 
    write_sizes = map(lambda o: o.size, self.write_operands)
    read_sizes = map(lambda o: o.size, self.read_operands)
    
    size = min(min(write_sizes), min(read_sizes))
    assert(size > 0)
    
    #print "corrected size:", size
    
    for o in self.write_operands:
      o.resize(size)
   
    for o in self.read_operands:
      o.resize(size)
  
  
  
  def fixMemoryAccess(self, mem_access):
    assert(False)
    assert(mem_access <> None)
    #print self.instruction
    
    if (self.instruction == "ldm"):
      
      self.write_operands = [self.operands[2]]
      self.mem_reg = self.operands[0]
      
      #if (mem_regs):
      #  self.read_operands  = [self.operands[0]]
        
      mem_source = mem_access["source"]
      mem_offset = mem_access["offset"]
      for i in range(self.operands[2].size):
        name = mem_source+"@"+str(mem_offset+i)
        self.read_operands.append(Operand(name, "BYTE", mem_source, mem_offset+i))
         
      #self.read_operands.append(self.operands[0])
      
    # stm: [op_2] = op_0
    elif (self.instruction == "stm"):
      
      self.read_operands.append(self.operands[0])
      self.mem_reg = self.operands[2]
      
      mem_source = mem_access["source"]
      mem_offset = mem_access["offset"]
      for i in range(self.operands[0].size):
        name = mem_source+"@"+str(mem_offset+i)
        self.write_operands.append(Operand(name, "BYTE", mem_source, mem_offset+i))
    else:
      assert(False)
  
  def isCall(self):
    return self.instruction == "call"
  def isRet(self):
    return self.instruction == "ret"
    
  def __str__(self):
    r = self.instruction + "-> "
    for op in self.read_operands:
      r = r + str(op) + ", "
    
    r = r + "| "
    
    for op in self.write_operands:
      r = r + str(op) + ", "
    
    return r
  
def ReilParser(filename):
    openf = open(filename)
    r = []
    for raw_ins in openf.readlines():
      r.append(REILInstruction(raw_ins))
    
    return r
