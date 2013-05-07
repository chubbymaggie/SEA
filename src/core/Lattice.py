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

from Types import *

gs = [("Data32","Num32"), ("Data32","Ptr32"), ("Data32","HPtr32"), ("Data32","SPtr32"), ("Data32","GPtr32"),
      ("Num32", "Ptr32"), ("Num32","HPtr32"), ("Num32","SPtr32"), ("Num32","GPtr32"),
      ("Ptr32", "SPtr32"),  ("Ptr32", "HPtr32"), ("Ptr32", "GPtr32")]

mlattice = dict()

for t in ptypes:
    mlattice[str(t), str(t)] = 0
for (pt1, pt2) in gs:
    mlattice[str(pt1), str(pt2)] = 1
    mlattice[str(pt2), str(pt1)] = -1
    
#import lattice

def join(pt1, pt2):
    p = (str(pt1), str(pt2))
    if p in mlattice:
        if mlattice[p] >= 0:
          return pt2
        if mlattice[p] < 0:
          return pt1
    else:
      return Type("Bot32")

#print join(Type("HPtr32"), Type("GPtr32"))
