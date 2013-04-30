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

from Operand import *

class Instruction:
  """An abstract instruction class"""
  def __init__(self, raw_ins, mem_regs = True):
    pass
  
  def fixMemoryAccess(mem_access):
    pass

  def getOperands(self):
    return list(self.read_operands + self.write_operands)
  
  def getReadOperands(self):
    return list(self.read_operands)

  def getWriteOperands(self):
    return list(self.write_operands)

  def getReadRegOperands(self):
    return filter(lambda o: o.isReg(), self.read_operands)

  def getWriteRegOperands(self):
    return filter(lambda o: o.isReg(), self.write_operands)
  
  def getReadVarOperands(self):
    return filter(lambda o: o.isVar(), self.read_operands)

  def getWriteVarOperands(self):
    return filter(lambda o: o.isVar(), self.write_operands)
  
  def getReadMemOperands(self):
    return filter(lambda o: o.isMem(), self.read_operands)

  def getWriteMemOperands(self):
    return filter(lambda o: o.isMem(), self.write_operands)
  
  def getMemReg(self):
    return self.mem_reg 
    
  def isCall(self):
    pass
  def isRet(self):
    pass
    
  def isJmp(self):
    pass
    
  def isCJmp(self):
    pass

