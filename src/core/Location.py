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

class Location:

  def __init__(self, name, index):
    self.type = None
    self.name = str(name)
    self.index = index
    
  def getIndex(self):
    return self.index

  def __str__(self):
    assert(False)

  def __cmp__(self, op):
    return cmp(self.name,op.name) * cmp(self.index,op.index)
  
  def __hash__(self):
    return hash(self.__str__())
    
  def __int__(self, base=10):
    assert(False)

class ImmLoc(Location):
  def __str__(self):
    return self.name
  
  def __int__(self, base=10):
  
    if ("0x" in self.name):    
      return int(self.name.replace("0x",""),16)
    else:
      return int(self.name,10)

class AddrLoc(Location):
  def __str__(self):
    return self.name+"("+str(self.index)+")"

class pAddrLoc(Location):
  pass

class RegLoc(Location):
  def __str__(self):
    return self.name+"("+str(self.index)+")"

class pRegLoc(Location):
  pass

class MemLoc(Location):
  def __str__(self):
    return self.name+"("+str(self.index)+")"

class NoLoc(Location):
  pass

