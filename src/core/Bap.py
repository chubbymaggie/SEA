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

from json import *
from NewOperand import *
from Instruction import *

class BinOp:
  def __init__(self, name, op1, op2):
    self.name = name
    self.op1 = op1
    self.op2 = op2
  
  def __str__(self):
    return str(self.name)+"("+str(self.op1)+","+str(self.op2)+")"


class BapInstruction(Instruction):
  
  def __readAttributes__(self, d):
    if 'attributes' in d:
      atts = d['attributes']
      for att in atts:
        if 'strattr' in att:
          self.isCallV = ('call' == att['strattr'])
        if 'strattr' in att:
          self.isRetV = ('ret' == att['strattr'])
  
  def __getBinOp__(self, d):
    
    name = d["binop_type"]
    op1  = self.__getExp__(d["lexp"])
    op2  = self.__getExp__(d["rexp"])
    
    return BinOp(name, op1, op2)
  
  def __getStore__(self, d):
    address = self.__getExp__(d['address'])
    value = self.__getExp__(d['value'])
 
    print address, "->", value
    endian = d['endian']
    assert(0)


  def __getExp__(self, d):
    
    if 'var' in d:
      return self.__getVar__(d['var'])
    if 'inte' in d:
      return self.__getInt__(d['inte'])
    elif 'binop' in d:
      return self.__getBinOp__(d['binop'])
    elif 'store' in d:
      return self.__getStore__(d['store'])
    else:
      #pass
      print "exp:"
      print d
      assert(0)
  
  def __getInt__(self, d):
    return int(d['int'])

  def __getVar__(self, d):
    
    if ('reg' in d['typ']):
      return RegOp(d['name'], d['typ'])
    else:
      #pass
      print d['name'], d['typ']
      assert(False)

  def __getLoad__(self, d):
    return self.__getInt__(d['address']['inte'])

  def __getBranch__(self, d):
    size = "DWORD"
    if 'inte' in d:
      name = hex(self.__getInt__(d['inte']))
      return AddrOp(name, size)
    elif 'lab' in d:
      name = d['lab']
      return AddrOp(name, size)
    elif 'load' in d:
      name = hex(self.__getLoad__(d['load']))
      return pAddrOp(name, size)
    elif 'var' in d:
      return self.__getVar__(d['var'])
    else:
      print d
      assert(False)
      
  def __init__(self, dins):
    
    self.read_operands = []
    self.write_operands = []
    self.branchs = []
    # self.address = pins.address
    # self.instruction = pins.instruction
    # self.operands = []
    
    # # for memory instructions
    # self.mem_reg = None
    
    # # for call instructions
    self.called_function = None
    self.instruction = None
    self.raw = str(dins)
    self.isCallV = False
    self.isRetV  = False
    #self.isJmp = False
    
    if ('label_stmt' in dins):
      assert(False)
    elif ('move' in dins):
        #pass
        self.instruction = 'move'
        
        print "moving to:", self.__getVar__(dins['move']['var']) 
        
        exp = self.__getExp__(dins['move']['exp'])
        
        self.read_operands = [exp]
        
        self.write_operands = [self.__getVar__(dins['move']['var'])]
        
        #print self.write_operands[0], "=", self.read_operands[0]
        #var = dins['move']['var']
        #exp = dins['move']['exp']
        #print 'dst', var['name']
        #print 'src', exp
    elif ('jmp' in dins):
        self.instruction = 'jmp'
        #self.isJmp = True
        self.__readAttributes__(dins['jmp'])
        
        if 'exp' in dins['jmp']:
          self.branchs = [self.__getBranch__(dins['jmp']['exp'])]
            
        #print 'jmp:', dins['jmp']
    elif ('cjmp' in dins):
        self.instruction = 'cjmp'
        #self.isJmp = True
        self.__readAttributes__(dins['cjmp'])
        
        if 'iftrue' in dins['cjmp']:
          d = dins['cjmp']['iftrue']
          self.branchs = [self.__getBranch__(d)]
        
        if 'iffalse' in dins['cjmp']:
          d = dins['cjmp']['iffalse']
          self.branchs.append(self.__getBranch__(d))
                  
         
    else:
        self.instruction = "xxx"
        #assert(False)
        
        
  def isCall(self):
    return self.isCallV
  def isRet(self):
    return self.isRetV
    
  def isJmp(self):
    return self.instruction == "jmp"
    
  def isCJmp(self):
    return self.instruction == "cjmp"
    

def BapParser(filename):
    openf = open(filename)
    size = "DWORD" #size of address
    r = []
    
    for dins in load(openf):
      if ('label_stmt' in dins):
        if 'label' in dins['label_stmt']:
          label = dins['label_stmt']['label']
          if 'name' in label:
            r.append(AddrOp(label['name'], size))
          else:
            r.append(AddrOp(hex(int(label['addr'])), size))
      else:
        r.append(BapInstruction(dins))
        
    return r
    
