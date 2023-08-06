import re
import random
import asyncio
import numbers
async def convert(inp, t):
  try:
    return t(inp)
  except Exception:
    return 
async def get(l, i, default=0):
  try:
    i = int(str(i))
    if abs(i)==i:
      return l[i]
    else:
      raise IndexError("idk")
  except Exception:
    return default
import sys
async def aprint(*objs, sep=' ', end='\n', file=sys.stdout, flush=False):
  return print(*objs, sep=sep, end=end, file=file, flush=flush)
async def ainput(prompt=''):
  return input(prompt)
class PISSinterpreter():
  def __init__(self, printcmd=aprint, inpcmd=ainput, errorcmd=aprint):
    self.input = inpcmd
    self.print = printcmd
    self.error = errorcmd
    self.debugon = False
    self.cmdpointer = 0
  class Exit(Exception): pass
  async def EVAL(self, i):
    try:
      id = str(random.randrange(100000000, 999999999))
      i = str(i).replace("\\\\", id).replace("\\", "").replace(id, "\\")
      ei = i.split("=", 1)
      if i=="i":
        i = await self.EVAL(await self.input())
      elif i.lower()=="on" or i.lower()=="true" or i.lower()=="enable":
        i = True
      elif i.lower()=="off" or i.lower()=="false" or i.lower()=="disable":
        i= False
      elif re.match("a\[.*?\]", i.lower()):
        arg = i[4:-1]
        i = await get(self.stack, await self.EVAL(arg))
      elif len(ei) == 2:
        args = ei
        arg1 = await self.EVAL(args[0])
        arg2 = await self.EVAL(args[1])
        i = arg1==arg2
      elif i=='':
        i=0
      elif type(i)==int:
        pass
      elif i.replace(" ", "").isdigit():
        i = int(i.replace(" ", ""))
      else:
        pass
      return i
    except Exception:
      return 0
  async def debug(self, stack, cmd, rawcmd, script):
   async def inner_debug(stack, cmd, script):
    vars = {"stack": stack, "char": char, 'cmd': cmd, "script": script}
    while True:
      i = await self.input(">>")
      arg = i.split(" ")
      command=arg[0].lower()
      del arg[0]
      arg = " ".join(arg)
      if command=="":
        break
      elif command=="exit" or command=="e":
        await self.exit()
      elif command == 'view':
        val = vars.get(arg)
        if val==None:
          await self.print("You cannot view something that doesn't exist")
        else:
          if type(val) == list:
            if val==[]:
              await self.print("Its just empty")
            else:
              await self.print(*val, sep="\n")
          else:
            await self.print(val)
      elif command == 'set':
        args = arg.replace('to', "=", 1).replace(" = ", "=", 1).split("=", 1)
        ki = args[0].split(" ")
        try:
          key = ki[0]
        except IndexError:
          await self.print("I dont know how you can set something when you havent even supplied something to set")
          continue
        try:
          index = ki[1]
        except IndexError:
          index = ''
        try:
          val = args[1]
        except IndexError:
          await self.print("A value was not supplied")
          continue
        if not key in vars.keys():
          await self.print("You cannot set something that doesn't exist")
          continue
        else:
         if index=='':
          if type(vars.get(key)) == list:
            val = val.replace(", ", ",").split(",")
          else:
            pass
          vars[key] = val
          if key == "cmd":
            vars["script"][self.cmdpointer] = val
         elif type(await convert(index, int))==int:
          index = await convert(index, int)
          if abs(index) == index:
           if not index < len(vars[key]):
            await self.print("Index is not a valid number")
            continue
          elif not abs(index) <= len(vars[key]):
            await self.print("Index is not a valid number")
            continue
          if type(vars.get(key)) == list:
            vars[key][index] = val
            if index==self.cmdpointer:
              vars["cmd"] = val
          else:
            l = list(vars[key])
            l[index] = val
            vars[key] = "".join(l)
            if key == "cmd":
              vars["script"][self.cmdpointer] = "".join(l)
         else:
           await self.print("Index is not a valid number")
      elif command=="exec":
        await self.EXEC(arg, vars["stack"])
      else:
        await self.print("Bad command.")
    return vars
   vars = await inner_debug(stack, rawcmd, script)
   stack = vars["stack"]
   char = vars["char"]
   cmd = vars["cmd"]
   #if not vars["cmd"] == rawcmd:
   # rawcmd = vars["cmd"]
   # cmd = rawcmd
   # stackref = re.findall("a\[.*?\]", cmd)
   # for ref in stackref:
   #   arg = ref[4:-1]
   #   evl = await get(stack, await self.EVAL(arg))
   #   cmd=cmd.replace(ref, str(evl))
   script = vars["script"]
   return stack, char, cmd, rawcmd, script
  async def exit(self, message=''):
    if message:
      message+="\nPROGRAM TERMINATED"
    else:
      message="PROGRAM TERMINATED"
    await self.error(str(message))
    raise self.Exit(message)
  async def EXEC(self, ri, stack=[]):
    i = ri.replace("\n", "|").split("|")
    self.cmdpointer=-1
    self.stack = stack
    try:
     if i[0][0] == "d":
      dcmd = list(i[0])
      del dcmd[0]
      dcmd = "".join(dcmd).lower()
      dcmd = await self.EVAL(dcmd)
      if type(dcmd) == bool:
        self.debugon=dcmd
      else:
        await self.print(F"WARNING: COULD NOT INTERPRET '{dcmd}'")
      del i[0]
    except IndexError:
      pass
    while True:
      try:
        self.cmdpointer+=1
        pointer=0
        try:
          cmd = i[self.cmdpointer]
        except IndexError:
          await self.exit()
        while not pointer==len(cmd):
         char = cmd[pointer]
         rawcmd = cmd
         #stackref = re.findall(r"a\[.*?\]", cmd)
         #for ref in stackref:
         #  arg = ref[4:-1]
         #  evl = await get(self.stack, await self.EVAL(arg))
         #  cmd=cmd.replace(ref, str(evl))
         if self.debugon:
           self.stack, cmd, rawcmd, i = await self.debug(self.stack, cmd, rawcmd, i)
         try:
           lchar = cmd[pointer-1]
         except IndexError:
           lchar=""
         try:
           llchar = cmd[pointer-2]
         except IndexError:
           llchar=""
         if lchar == "\\" and not llchar=="\\":
           pass
         elif char=="\\":
           pass
         elif char == "+":
          args=cmd.split("+")
          arg1 = args[0]
          arg2 = args[1]
          arg1 = await self.EVAL(arg1)
          arg2 = await self.EVAL(arg2)
          if not (isinstance(arg1, numbers.Number) or isinstance(arg2, numbers.Number)):
            await self.exit("ERROR: YOU CANNOT ADD A STRING")
          self.stack.append(arg1+arg2)
         elif char == "-":
          args=cmd.split("-")
          arg1 = args[0]
          arg2 = args[1]
          arg1 = await self.EVAL(arg1)
          arg2 = await self.EVAL(arg2)
          if not (isinstance(arg1, numbers.Number) or isinstance(arg2, numbers.Number)):
            await self.exit("ERROR: YOU CANNOT SUBTRACT A STRING")
          self.stack.append(arg1-arg2)
         elif char == "*":
          args=cmd.split("*")
          arg1 = args[0]
          arg2 = args[1]
          arg1 = await self.EVAL(arg1)
          arg2 = await self.EVAL(arg2)
          if not (isinstance(arg1, numbers.Number) or isinstance(arg2, numbers.Number)):
            await self.exit("ERROR: YOU CANNOT MULTIPLY A STRING")
          self.stack.append(arg1*arg2)
         elif char == "/":
          args=cmd.split("/")
          arg1 = args[0]
          arg2 = args[1]
          arg1 = await self.EVAL(arg1)
          arg2 = await self.EVAL(arg2)
          if not (isinstance(arg1, numbers.Number) or isinstance(arg2, numbers.Number)):
            await self.exit("ERROR: YOU CANNOT DIVIDE A STRING")
          self.stack.append(arg1/arg2)
         elif char=="p":
           arg = await self.EVAL(cmd.replace("p", ""))
           await self.print(arg)
         elif char=="g":
           args = cmd.replace("g", "", 1).split(",", 1)
           con = await self.EVAL(args[0])
           line = await self.EVAL(args[1])
           if con:
             if not type(line) == int:
               await self.exit("ERROR: YOU CANNOT GOTO TO SOMETHING THAT ISNT A INT. WHAT ARE YOU, HEXAHUMAN?")
             cmdpointer=line
             try:
               cmd = i[cmdpointer]
             except IndexError:
               await self.exit()
             continue
         elif char=='s':
           self.stack.append(await self.EVAL(cmd.replace("s", "")))
         elif char=="e":
           await self.exit()
         else:
           pass
         pointer+=1
      except self.Exit as e:
        break
    return self.stack
  async def console(self):
   while True:
    inp = await self.input(">")
    if inp == "esc":
      break
    if inp == "help":
      await self.print(await self.gethelptext())
    if inp == "debug test":
      self.cmdpointer = 0
      self.stack = []
      char = "x"
      cmd = "xxx"
      rawcmd = "xxx"
      script = ["xxx", "yyy"]
      while True:
        try:
           self.stack, cmd, rawcmd, script = await self.debug(self.stack, cmd, rawcmd, script)
        except self.Exit:
          break
    else:
      await self.EXEC(inp)
   await self.error("EXITED CONSOLE")
  async def gethelptext(self):
   return """Console Only:
  'debug test' - Get put into an env to test debug mode
  'esc' | Exit console
Other:
  'pi' | Print 'i'
  'i1+i2' | Adds i1 to i2 and puts it on the stack
  'i1-i2' | Subtracts i1 from i2 and puts it on the stack
  'i1/i2' | Divides i1 by i2
  'i1/i2' | Multiplys i1 by i2'
  'gcondition,line' | Gotos line if condition is true
  'dcondition' | Enables or disables debug depending on condition, only works at the start of a program
  'si' | Push i to stack
  'e' | Exit program"""
if __name__ == "__main__":
  ip = PISSinterpreter()
  asyncio.run(ip.console())