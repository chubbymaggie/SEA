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

from src.core import *
#from Program     import *
#from NewOperand  import * 
import random

def generatePaths(filename, n):

  pr = BapProgram(filename)
  
  for i in range(n):
    #pr.reset("0x8049463")
    pr.reset("0x8048fbe")
    path = generatePath(pr)
    print str(i)+":",
    for label in path:
      print label, ",",
      
    print ""

def generatePath(pr, max_count = 1000):
  
  branches_taken = []
  count = 0
  for ins in pr:
    #print str(ins.raw)
    #print ins.ins
    if count == max_count:
      break
      
    #if branches_taken <> []:
      #print "last:", branches_taken[-1]
  
    if ins.isCall():
      if str(ins.branchs[0]) == "0x8048890":
        branches_taken.append("exit")
        break
      
      if str(ins.branchs[0]) == "0x8048800":
        branches_taken.append("__stack_chk_fail")
        break
        
      #print ins.branchs[0]
    
    #if ins.isRet():
    #  print "RET!"
    #  break
    
    elif ins.isCJmp():
      count = count + 1
      i = bool(random.randint(0,1))
      #print "pasa"  
      if i == False:
        branches_taken.append(pr.selectFalseBranch())
      elif i == True:
        branches_taken.append(pr.selectTrueBranch())
  
  return branches_taken