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
from __init__ import *
#from Types import *

gs = [("Data32","Num32"), ("Data32","Ptr32"), ("Data32","HPtr32"), ("Data32","SPtr32"), ("Data32","GPtr32"),
      ("Num32", "Ptr32"), ("Num32","HPtr32"), ("Num32","SPtr32"), ("Num32","GPtr32"),
      ("Ptr32", "SPtr32"),  ("Ptr32", "HPtr32"), ("Ptr32", "GPtr32")]

mlattice = dict()

for t in ptypes:
    mlattice[t.name, t.name] = 0
for (pt1, pt2) in gs:
    mlattice[pt1, pt2] = 1
    mlattice[pt2, pt1] = -1
    
#import lattice

def propagateInfo(pt1_info, pt2_info):
  if (pt1_info == pt2_info):
    return pt1_info
  
  if (pt1_info == None):
    return pt2_info
  
  if (pt2_info == None):
    return pt1_info

def join(pt1, pt2):
    p = (pt1.name, pt2.name)
    
    einfo = propagateInfo(pt1.einfo, pt2.einfo)
    
    if p in mlattice and pt1.index == pt2.index:
        if mlattice[p] >= 0:

	  pt2.setInfo(einfo)
          return pt2
          
        if mlattice[p] < 0:
	  
	  pt1.setInfo(einfo)
          return pt1
    else:
      return Type("Bot32", None)
      
def joinset(s):
  
  assert(len(s) > 0)
  
  for pt in s:
  
    if (not isinstance(pt,Type)):
      for e in s:
        if (not isinstance(e,Type)):
          print e.__class__, "--",
        else:
	  
          print e, "--",
      assert(0)
  
  r = s.pop()
  
  for pt in s:
    r = join(r, pt)
  
  
  return r

#print join(Type("HPtr32"), Type("GPtr32"))
