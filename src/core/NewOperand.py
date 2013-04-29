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

#import copy, math
  
size_in_bits = {
    "BYTE": 8,
    "WORD": 16,
    "DWORD": 32,
    "QWORD": 64,
    "1"    : 1,
    "8"    : 8,
    "16"    : 16,
    "32"    : 32,
}

class Operand:

  def __init__(self, name, size):
    self.type = None
    self.name = str(name)
    
    self.size_in_bits = size_in_bits.get(size, 0)
    
    if (self.size_in_bits % 8 == 0):
      self.size_in_bytes = self.size_in_bits / 8
    else:
      self.size_in_bytes = () # bottom

  def __str__(self):
    return self.name

  def __cmp__(self, op):
    return cmp(self.name,op.name)
  
  def __hash__(self):
    return hash(self.name)

class Imm(Operand):
  pass

class Addr(Operand):
  pass

class pAddr(Operand):
  pass

class Reg(Operand):
  pass

class pReg(Operand):
  pass

class NoOp(Operand):
  pass

isOp = isinstance

#def guessOperand(name, size):
  #if x == "EMPTY":
    #return NoOp(name, size)
  
  #try:
    #y = int(x)
    #return Imm(name, size)
  #except ValueError:
    #return "reg"