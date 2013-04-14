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
from Operand import *
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

ReilParser = reil.parseString

class REILInstruction(Instruction):
  def __init__(self, pins, mem_access, mem_regs = True):
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
        self.operands.append(Operand(aopers[i-1], aopers[i-2]))
    self.operands.append(Operand(aopers[-1], aopers[-2]))
    
    self.read_operands = []
    self.write_operands = []
    
    # ldm: op_2 = [op_0]
    if (pins.instruction == "ldm"):
      
      self.write_operands = [self.operands[2]]
      self.mem_reg = self.operands[0]
      
      if (mem_access <> None):
        
        #if (mem_regs):
        #  self.read_operands  = [self.operands[0]]
        
        mem_source = mem_access["source"]
        mem_offset = mem_access["offset"]
        for i in range(self.operands[2].size):
          name = mem_source+"@"+str(mem_offset+i)
          self.read_operands.append(Operand(name, "BYTE", mem_source, mem_offset+i))
         
        #self.read_operands.append(self.operands[0])
      #else:
      #  print "#WARNING: No memory access information of ldm in", self.address
      
    # stm: [op_2] = op_0
    elif (pins.instruction == "stm"):
      
      self.read_operands.append(self.operands[0])
      self.mem_reg = self.operands[2]
      
      if (mem_access <> None):
      #  if (mem_regs):
      #    self.write_operands = [self.operands[2]]
        
        mem_source = mem_access["source"]
        mem_offset = mem_access["offset"]
        for i in range(self.operands[0].size):
          name = mem_source+"@"+str(mem_offset+i)
          self.write_operands.append(Operand(name, "BYTE", mem_source, mem_offset+i))
      #else:
      #  print "#WARNING: No memory access information of stm in", self.address
      
    elif (pins.instruction == "jcc"):
      self.read_operands  = filter(lambda o: not o.isEmpty(), self.operands[0:2])
      self.write_operands = []
      
    elif (pins.instruction == "call"):
      #print self.operands[0].name
      if (self.operands[0].name <> "EMPTY"):
        self.called_function = self.operands[0].name
      
    else:
      
      self.read_operands  = filter(lambda o: not o.isEmpty(), self.operands[0:2])
      self.write_operands = filter(lambda o: not o.isEmpty(), self.operands[2:3])
