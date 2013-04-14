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
    
class Path:
    def __init__(self, filename, parser, first, last, is_reversed = False):
        
        self.filename = filename
        self.parser   = parser
        self.openf = open(filename)
        self.code = self.openf.readlines()[first:last+1]
        self.code = map(self.parser, self.code)
        
        self.len = len(self.code)
        
        self.first = first
        self.last = first + self.len
        
        self.is_reversed = is_reversed
        
        if (self.is_reversed):
          self.current = self.len - 1
        else:
          self.current = 0

    def __iter__(self):
        return self
    
    def __len__(self):
        return self.len

    def next(self):
        #print self.current, self.is_reversed, self.len
        if (self.is_reversed):
          if self.current < 0:
            raise StopIteration
          else:
            self.current -= 1
            return self.code[self.current + 1]
        else:
          if self.current >= self.len:
            raise StopIteration
          else:
            self.current += 1
            return self.code[self.current - 1]  
          
    
    def reverse(self):
        self.is_reversed = not (self.is_reversed)
        if (self.is_reversed):
          self.current = self.len - 1
        else:
          self.current = 0
        
    def reset(self):
        if (self.is_reversed):
          self.current = self.len - 1
        else:
          self.current = 0
        
    def __getitem__(self, i):
        
        if (type(i) == slice):
          (first, last, stride) = i.indices(self.len)
          return Path(self.filename, self.parser, first, last-1) 
        else:
          return self.code[i]
