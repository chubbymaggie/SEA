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

from src.core import *


class EXISTPathGenerator(PathGenerator):
  
  def __init__(self, program, start, ends, epsilon):
    self.program = program
    self.start = start
    self.epsilon = epsilon
    
    # for all possible labels
    self.max_counts = dict()
    
    # label population
    for (s, y) in self.epsilon:
      for label in s:
        self.max_counts[label] = 0
        
    self.train()
    
  def count(self, seq, labels):
    
    res = dict()
    
    for label in labels:
      res[label] = seq.count(label)
	
    return res
  
  def train(self):
    
    labels = self.max_counts.keys()
    #self.max_counts = self.count(self.epsilon[0], self.labels)
    
    for (s, y) in self.epsilon:
      if y:
	res = self.count(s,labels)
	
	for label in res.keys():
	  if (res[label] > self.max_counts[label]):
	    self.max_counts[label] = res[label]
    
    for label in self.max_counts.keys():
      print label, self.max_counts[label]
  
  def prob(self, k, res):
    
    if self.max_counts[k] == 0: 
      return 0
    return float(self.max_counts[k] - res[k])/float(self.max_counts[k])
  
  def select(self, seq, states):
    
    res = self.count(seq, states)
    
    probs = map(lambda k: self.prob(k,res), states) 
    m = max(probs)
    
    if (m == 0.0):
      return None
    
    indexes = [i for i, j in enumerate(probs) if j == m]
    
    return random.choice(indexes)
    
  
  def next(self):
    self.program.reset(self.start)
    seq = []
    count = 0
    max_count = 10
    
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
        
  return (x > 0 and 2*x == y and z == 1)
  

def generatePaths(filename, start, n):
  
  program = BapProgram(filename)
  random_paths = RandomPathGenerator(program, start, set())
  epsilon = list()
  
  for (i,path) in enumerate(random_paths):
    epsilon.append((path, detectFeasible(path)))
        
    if (i==10000):
      break
      
  gen_paths = EXISTPathGenerator(program, start, set(), epsilon)
  paths = []
  
  for (i,path) in enumerate(gen_paths):
    paths.append((path, detectFeasible(path)))
    
    print paths[-1]
    
    if (i==n):
      break
  
  #print paths
  

      

