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

import copy

class Type:
  def __init__(self, name, index, einfo = None):
    self.name = str(name)
    self.index = index
    self.setInfo(einfo)
    
  def __str__(self):
    
    r = str(self.name)
    
    if (self.index <> None):
      r = r +"("+str(self.index)+")"
      
    if (self.einfo <> None):
      r = r + " with "
      for k in self.einfo:
        r = r + str(k)+"="+str(self.einfo[k])+", "
    
    return r
    
  def setInfo(self, einfo):
    self.einfo = copy.copy(einfo)
  
  def addTag(self, tag, value):
    if self.einfo == None:
      self.einfo = dict()
    
    self.einfo[tag] = value
    
    
def getMemInfo(ptype):
    
    mem_source = str(ptype.einfo["source.name"])+str(ptype.einfo["source.index"])
    mem_offset = ptype.einfo["offset"]
    return (mem_source, mem_offset)
    
ptypes = [Type("Data32", None), 
          Type("Num32", None) , 
          Type("Ptr32", None) , 
          Type("SPtr32", None), 
          Type("HPtr32", None), 
          Type("GPtr32", None), 
          Type("Bot32", None) ]
