"""
    This file is part of SEA.

    SEA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SEA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SEA.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2013 by neuromancer
"""



from core        import *

from SSA         import SSA
from Function    import *
from Condition   import *
from SMT         import SMT, Solution
from Typing      import *

def setInitialConditions(ssa, initial_values, smt_conds):
  ssa_map = ssa.getMap(set(), set(), set(initial_values.keys()))
  eq = Eq(None, None)
  
  for iop in initial_values:
    
    if (iop.isReg()):
      if ":" in iop.name:
        smt_conds.add(eq.getEq(iop,initial_values[iop]))
      else:
        smt_conds.add(eq.getEq(ssa_map[iop.name],initial_values[iop]))
    elif (iop.isMem()):
      smt_conds.add(eq.getEq(iop,initial_values[iop]))
    else:
      assert(False)
      
      
def getValueFromCode(inss, callstack, initial_values, memory, op, debug = False):
  
  # Initialization
  
  # we reverse the code order
  inss.reverse()
  
  # we reset the used memory variables
  Memvars.reset()
  
  # we save the current callstack
  last_index = callstack.index  # TODO: create a better interface
  
  # we set the instruction counter
  counter = len(inss)-1
  
  # ssa and smt objects
  ssa = SSA()
  smt_conds  = SMT()
  
  val_type = None
  mvars = set()
 
  #if (op |iss| ImmOp):
    #return op
  #elif (op.isMem()):
    #for i in range(op.size):
      #name = op.mem_source+"@"+str(op.mem_offset+i)
      #mvars.add(Operand(name, "BYTE", op.mem_source, op.mem_offset+i))
      ##print name
  #else:
    ## we will start tracking op
    #mvars.add(op)
  
  mvars.add(op)
  
  # we start without free variables
  fvars = set()
  
  ssa.getMap(mvars, set(), set())

  for ins in inss:
    
    if debug:
      print ">", ins.instruction, counter ,str(ins.called_function)

    if memory.getAccess(counter) <> None:
      ins.fixMemoryAccess(memory.getAccess(counter))
  
    ins_write_vars = set(ins.getWriteVarOperands())
    ins_read_vars = set(ins.getReadVarOperands())
 
    if len(ins_write_vars.intersection(mvars)) > 0: 
      
      ssa_map = ssa.getMap(ins_read_vars.difference(mvars), ins_write_vars, ins_read_vars.intersection(mvars))

      cons = conds.get(ins.instruction, Condition)
      condition = cons(ins, ssa_map)
     
      mvars = mvars.difference(ins_write_vars) 
      mvars = ins_read_vars.union(mvars)
   
      smt_conds.add(condition.getEq())
    
    # simple typing
    #new_val_type = detectType(mvars, ins, counter, callstack)
    
    # additional conditions
    mvars = addAditionalConditions(mvars, ins, ssa, callstack, smt_conds)
    
    #val_type = max(val_type, new_val_type)

    # no more things to do
    # we update the counter 
    counter = counter - 1    
    # we update the current call for next instruction
    callstack.prevInstruction(ins) 
  
  #if val_type == None:
    #val_type = "imm"
  
  for v in mvars:
    if not (v in initial_values):
      print "#Warning__", str(v), "is free!" 
  
  setInitialConditions(ssa, initial_values, smt_conds)
  smt_conds.solve(True)
  
  if op |iss| RegOp:
    op.name = op.name+"_0"
    
  elif op.isMem():
    op.mem_source = op.mem_source+"_0"
  
  callstack.index = last_index  # TODO: create a better interface
  return smt_conds.getValue(op)
  
  #if (debug):
    #print val_type, op, smt_conds.getValue(op)
  #return mkVal(val_type, smt_conds.getValue(op))

def getTypedValueFromCode(inss, callstack, initial_values, memory, op, debug = False):
  assert(0)
  
def getPathConditions(trace):
  assert(0)
  
#def getTypedValueFromCode(inss, callstack, initial_values, memory, op, debug = False):
  
  ## Initialization
  
  ## we reverse the code order
  #inss.reverse()
  
  ## we reset the used memory variables
  #Memvars.reset()
  
  ## we save the current callstack
  #last_index = callstack.index  # TODO: create a better interface
  
  ## we set the instruction counter
  #counter = len(inss)-1
  
  ## ssa and smt objects
  #ssa = SSA()
  #smt_conds  = SMT()
  
  #val_type = None
  #mvars = set()
 
  #if (op |iss| ImmOp):
    #return op
  #elif (op.isMem()):
    #for i in range(op.size):
      #name = op.mem_source+"@"+str(op.mem_offset+i)
      #mvars.add(Operand(name, "BYTE", op.mem_source, op.mem_offset+i))
      ##print name
  #else:
    ## we will start tracking op
    #mvars.add(op)
    
  ## we start without free variables
  #fvars = set()
  
  #ssa.getMap(mvars, set(), set())

  #for ins in inss:
    
    #if debug:
      #print ">", ins.instruction, counter ,str(ins.called_function)

    #if memory.getAccess(counter) <> None:
      #ins.fixMemoryAccess(memory.getAccess(counter))
  
    #ins_write_vars = set(ins.getWriteVarOperands())
    #ins_read_vars = set(ins.getReadVarOperands())
 
    #if len(ins_write_vars.intersection(mvars)) > 0: 
      
      #ssa_map = ssa.getMap(ins_read_vars.difference(mvars), ins_write_vars, ins_read_vars.intersection(mvars))

      #cons = conds.get(ins.instruction, Condition)
      #condition = cons(ins, ssa_map)
     
      #mvars = mvars.difference(ins_write_vars) 
      #mvars = ins_read_vars.union(mvars)
   
      #smt_conds.add(condition.getEq())
    
    ## simple typing
    #new_val_type = detectType(mvars, ins, counter, callstack)
    
    ## additional conditions
    #mvars = addAditionalConditions(mvars, ins, ssa, callstack, smt_conds)
    
    #val_type = max(val_type, new_val_type)

    ## no more things to do
    ## we update the counter 
    #counter = counter - 1    
    ## we update the current call for next instruction
    #callstack.prevInstruction(ins) 
  
  #if val_type == None:
    #val_type = "imm"
  
  #for v in mvars:
    #if not (v in initial_values):
      #print "#Warning__", str(v), "is free!" 
  
  #setInitialConditions(ssa, initial_values, smt_conds)
  #smt_conds.solve(debug)
  
  #if op.isReg():
    #op.name = op.name+"_0"
    
  #elif op.isMem():
    #op.mem_source = op.mem_source+"_0"
  
  #callstack.index = last_index  # TODO: create a better interface
  #if (debug):
    #print val_type, op, smt_conds.getValue(op)
  #return mkVal(val_type, smt_conds.getValue(op))


#def getPathConditions(trace):
  
  #inss = trace["code"]
  #callstack = trace["callstack"]
  
  #initial_values = trace["initial_conditions"]
  #final_values = trace["final_conditions"]
  #memory = trace["mem_access"]
  #parameters = trace["func_parameters"]
  
  ## we reverse the code order
  #inss.reverse()
  
  ## we reset the used memory variables
  #Memvars.reset()
  
  ## we set the instruction counter
  #counter = len(inss)-1
  
  ## ssa and smt objects
  #ssa = SSA()
  #smt_conds  = SMT()
  
  ## auxiliary eq condition
  
  #eq = Eq(None, None)
  #mvars = set()
  
  ## final conditions:
  
  #for (op, _) in final_values.items():
    #mvars.add(op)
  
  #ssa.getMap(mvars, set(), set())
  #setInitialConditions(ssa, final_values, smt_conds)
  
   
  ## we start without free variables
  #fvars = set()

  #for ins in inss:
    
    #if memory.getAccess(counter) <> None:
      #ins.fixMemoryAccess(memory.getAccess(counter))
  
    #ins_write_vars = set(ins.getWriteVarOperands())
    #ins_read_vars = set(ins.getReadVarOperands())
 
    #if ins.instruction == "jcc" or len(ins_write_vars.intersection(mvars)) > 0:
      
      #ssa_map = ssa.getMap(ins_read_vars.difference(mvars), ins_write_vars, ins_read_vars.intersection(mvars))

      #cons = conds.get(ins.instruction, Condition)
      #condition = cons(ins, ssa_map)
     
      #mvars = mvars.difference(ins_write_vars) 
      #mvars = ins_read_vars.union(mvars)
   
      #smt_conds.add(condition.getEq())
      
    #elif (ins.isCall() and ins.called_function <> None):
      
      #func_cons = funcs.get(ins.called_function, Function)
      #func = func_cons(None, parameters.getParameters(counter))
      
      #func_write_vars = set(func.getWriteVarOperands())
      #func_read_vars = set(func.getReadVarOperands())
      
      #if len(func_write_vars.intersection(mvars)) > 0:
        #ssa_map = ssa.getMap(func_read_vars.difference(mvars), func_write_vars, func_read_vars.intersection(mvars))
        
        
        #cons = conds.get(ins.called_function, Condition)
        #condition = cons(func, None)
        
        #c = condition.getEq(func_write_vars.intersection(mvars))
        
        #mvars = mvars.difference(func_write_vars) 
        #mvars = func_read_vars.union(mvars)
        
        #smt_conds.add(c)
    
    ## additional conditions
    
    #mvars = addAditionalConditions(mvars, ins, ssa, callstack, smt_conds)
    

    ## no more things to do
    ## we update the counter 
    #counter = counter - 1    
    ## we update the current call for next instruction
    #callstack.prevInstruction(ins) 
  
  ##for v in mvars:
  ##  print v
  
  #fvars = filter(lambda v: not (v in initial_values.keys()), mvars)
  #for v in fvars:
  ##  print v,n
    #if not (v in initial_values) and not (":" in v.name):
      #print "#Warning", str(v), "is free!" 
  
  #setInitialConditions(ssa, initial_values, smt_conds)
  
  #if (smt_conds.is_sat()):
    #smt_conds.solve()
  
    #smt_conds.write_smtlib_file("exp.smt2")  
    #smt_conds.write_sol_file("exp.sol")
  
    #return Solution(smt_conds.m, fvars)
  #else: # unsat :(
    #return None
