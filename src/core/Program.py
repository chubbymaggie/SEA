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

from NewOperand  import * 
from Instruction import Instruction
#from Path        import Path

class Program:
    def __init__(self, filename, parser):
        
        self.filename = filename
        self.parser   = parser
        self.current  = 0
        self.labels   = dict()
        self.all = self.parser(self.filename)
        self.code = []
        
        #print self.all
        
        for e in self.all:
          if (isinstance(e, Addr)):
            self.labels[str(e)] = self.current
          elif (isinstance(e, Instruction)):
            self.code.append(e)
            self.current = self.current + 1
          else:
            assert(False)
        
        self.current = 0
        #self.code = map(cons, self.code)
        
        self.len = len(self.code)
        
        self.first = 0
        self.last = self.len
        self.path = None

    def __iter__(self):
        return self
    
    def __len__(self):
        return self.len

    def stepIn(self):
      
      assert(not (self.prev_ins == None))
      assert(self.prev_ins.isCall())
      
      branchs = self.prev_ins.branchs
      taken = branchs[0]
      
      if not (isinstance(taken, Addr)):
         print "Impossible to step into this call"
         assert(False)
      
      if str(taken) in self.labels:
        #print taken, "taken!"
        self.current = self.labels[str(taken)]
      else:
	assert(False)
        
    def selectTrueBranch(self):
        #ins = self.code[self.current-1]
        assert(not (self.prev_ins == None))
        branchs = self.prev_ins.branchs
        
        if (len(branchs) == 0):
            print "This instruction is not a jmp/call"
            assert(False)
        else:
            taken = branchs[0]
            
            if not (isinstance(taken, Addr)):
              print "Impossible to follow jmp"
              assert(False)
            
            if str(taken) in self.labels:
              #print taken, "taken!"
              self.current = self.labels[str(taken)]#[0]
              self.selected = True
            else:
              print "Unresolved jmp to", str(taken)
              assert(False)
              
        self.prev_ins = None
        
    def selectFalseBranch(self):
        #ins = self.code[self.current-1]
        assert(not (self.prev_ins == None))
        branchs = self.prev_ins.branchs
        
        if (len(branchs) == 0):
            print "This instruction is not a jmp/call"
            assert(False)
        else:
            taken = branchs[-1]
            
            if not (isinstance(taken, Addr)):
              print "Impossible to follow jmp"
              assert(False)
            
            if str(taken) in self.labels:
              self.current = self.labels[str(taken)]
            else:
              print "Unresolved jmp to", str(taken)
              assert(False)
              
        self.prev_ins = None
            
    
    def next(self):

      if (self.current == None):
	raise BranchUnselected
    
      if self.current >= self.len:
        raise StopIteration
      else:
	
	(addr, ins) = (self.current, self.code[self.current])
	
	if (ins.isCJmp()):
	  self.current = None
	  self.prev_ins = ins
	elif (ins.isJmp()):
	  if (ins.isCall()):
	      self.prev_ins = ins
	      self.current += 1
	      #pass # fixme
	  else:
	    # next instruction is the only possible branch
	    taken = ins.branchs[0]
	    self.current = self.labels[str(taken)]
	else:
	  # next instruction is the following 
	  self.current += 1
	
	return (addr, ins)
        
    def reset(self):
      self.current = 0
        
    def __getitem__(self, i):
        
        if (type(i) == slice):
          raise NoSlice
        else:
          return self.code[i]
