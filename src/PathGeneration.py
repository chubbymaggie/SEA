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

import random

from core import *

from Lifting import *
from Prelude import *
from Common import getPathConditions

class PathInfo:
  def __init__(self, ilabels):
    self.E_viw = dict()
    
    self.vi = dict()
    labels = list(ilabels)
    labels.insert(0,"start")
    labels.append("end")
    
    for label in labels:
      self.vi[label] = 0
    
    for (i, label) in enumerate(labels[:-1]):
      self.vi[label] = self.vi[label] + 1 
      self.E_viw[(label, self.vi[label], labels[i+1])] = True
      
  def E(self, v,i, w, j):
    
    return ((v, i, w) in self.E_viw) and j <= self.vi[w] 


class EXISTPathGenerator(PathGenerator):
  
  def __init__(self, program, start, ends, epsilon):
    self.program = program
    self.start = start
    self.epsilon = epsilon
    
    ## for all possible labels
    #self.max_counts = dict()
    
    ## label population
    #for (s, y) in self.epsilon:
      #for label in s:
        #self.max_counts[label] = 0
        
    self.train()
    
  def count(self, seq, labels):
    pass
    #res = dict()
    
    #for label in labels:
      #res[label] = seq.count(label)
	
    #return res
  
  def train(self):
    
    self.pathinfos = []
    
    for (i, (labels, y)) in enumerate(self.epsilon):
      if y:
	pi = PathInfo(labels)
	self.pathinfos.append(pi)
	#print pi.E_viw
  
  def prob(self, v,i, w,j):
    
    count = 0
    for pi in self.pathinfos:
      
      if pi.E(v,i, w, j):
        count = count + 1
    
    if count == 0:
      return 1.0
    
    return float(count)/float(len(self.pathinfos))
    #if self.max_counts[k] == 0: 
      #return 0
    #return float(self.max_counts[k] - res[k])/float(self.max_counts[k])
  
  def select(self, seq, states):
    
    v = seq[-1]
    
    probs = map(lambda w: self.prob(v, seq.count(v) ,w , seq.count(w)+1), states) 
    m = max(probs)
    
    #if (m == 0.0):
    #  return None
    
    indexes = [i for i, j in enumerate(probs) if j == m]
    
    return random.choice(indexes)
    
  
  def next(self):
    self.program.reset(self.start)
    seq = ["start"]
    count = 0
    max_count = 20
    
    for ins in self.program:
      ##print str(ins.raw)
      ##print ins.ins
      if count == max_count:
        break
      
      ##if branches_taken <> []:
        ##print "last:", branches_taken[-1]
  
      if ins.isCall():
	pass
        ##if str(ins.branchs[0]) == "0x8048890":
          ##branches_taken.append("exit")
          ##break
      
        ##if str(ins.branchs[0]) == "0x8048800":
          ##branches_taken.append("__stack_chk_fail")
          ##break
    
      elif ins.isCJmp():
        count = count + 1
        i = self.select(seq, map(str, ins.branchs))
        
        #print i,
        
        if i == None:
	  return seq
        
        if i == 0:
          seq.append(str(self.program.selectFalseBranch()))
        elif i == 1:
          seq.append(str(self.program.selectTrueBranch()))
        else:
	  assert(False)
	
	if seq[-1] == "end":
	  break
        
    
    return seq
    #return branches_taken
        
def detectFeasible(path):
  
  x,y,z = (0,0,0)
  
  for l in path:
    if l == "nocjmp7":
      z = z + 1
    if l == "0x8048423":
      x = x + 1
    if l == "0x804845d":
      y = y + 1
  return (x,y,z)      
  #return (x > 0 and 2*x == y and z == 1)
  

def generatePaths(program, start, n):

  #assert(0)
  random_paths = ManualPathGenerator(program, start, set())
  epsilon = dict()#list()
  rand_count = 0
  gen_count = 0
  
  for (i,(path, labels)) in enumerate(random_paths):
    #print "hola" 
    for label in labels:
      print label,
    print "end"
    #(x,y,z) = detectFeasible(path)
    
    
    #if (x > 0 and 2*x == y and z == 1):
    #  epsilon[(x,y,z)] = (path, True)
    #  rand_count = rand_count + 1
    #epsilon.append((path, detectFeasible(path)))
    #print len(path)
    path.reset()
    trace = mkTrace(path, [])
    path.reset()
    print getPathConditions(trace, True)
    if (i==0):
      break
 
  assert(0) 
  print float(rand_count)/10000
  
  #print epsilon
  
  gen_paths = EXISTPathGenerator(program, start, set(), epsilon.values())
  paths = []
  
  
  
  for (i,path) in enumerate(gen_paths):
    
    
    (x,y,z) = detectFeasible(path)
    
    
    #paths.append((path,(x > 0 and 2*x == y and z == 1)))
    
    
    if ((x > 0 and 2*x == y and z == 1)):
      gen_count = gen_count + 1
    
    #print paths[-1]
    #if :
      
    
    
    if (i==10000):
      break
  
  #print paths
  print float(gen_count)/10000

      

