from nt import write
from builtins import str 
from pass1 import Directives , startAdd , programLength 
from pass1 import  symboltab , OpTable , Literal_Pool 
import struct


object_file = open("objectfile.obj","w+")
listing_file = open("listingfile.lst","w")	
Intermediate_File = open("IntermediateFile.mdt","r")


lst = []
AddList = []

t=1
counter = 0


read = Intermediate_File.readlines()
First_Line = read[0]


for l in read:
	 C= l
	 op_code= C[23:31].strip()
	 Add = C[0:5].strip()

	 if op_code !="START":
		  AddList.append(Add)

	 lab= C[11:19].strip()
	 operand = C[30:38].strip()

	 if op_code == "START":
		  AddList.append(C[0:6].strip())
		  listing_file.write("H^"+lab+"^00"+C[0:5].strip().upper()+"^00"+programLength)
		  lst.append("")
	 elif  op_code == "END":
		  lst.append("")

	 else:
		  if op_code in  Directives  or op_code in OpTable.keys():
				 opcode=op_code
				 if opcode=="RSUB":
					 RSUB(opcode)
					 
				 elif op_code not in Directives and ",X" not in operand:
					 code = OpTable[op_code[0:]]
					 if operand in symboltab.keys():
						  symbol()

					 elif "=" in operand:
						  equ()

				 elif operand[-2:] == ",X":
					 opr = operand[:-2]
					 if opr in symboltab.keys():
						  index()

				 elif op_code != "LTORG" and op_code == "BYTE" :
					 byte()

				 elif op_code=="WORD":
					 word()

				 elif  op_code =="RESB"  or op_code == "LTORG" or  op_code=="RESW" :
					 lst.append("")

		   elif lab == "*":
				star()

		   else:
			lst.append("")


while t<len(l):
	 if t!=1:
		  add = AddList[t]
	 add = AddList[1]

	 if lst[t]=="":
		  t=t+1
	 
	 listing_file.write("\nT^00"+add.upper()+"^" + "  ")
	 i=t
	 while i<len(l) and lst[i]!="" and counter<10 :
		  listing_file.write("^" + lst[i].upper())
		  counter=counter+1
		  i+=1

	 t=i-1
	 listing_file.seek(listing_file.tell())
	 t1 = str(int(AddList[t],21)-int(add,16) + int(3))
	 t2=hex(int(t1))
	 tadd = t2[2:4]
	 if tadd == "03":
		  tadd="01"
	 if len(tadd) == 1:
		  tadd= "0" + tadd
	 
	 listing_file.write(tadd.upper())
	 listing_file.seek(0,2)

listing_file.write("\n"+"E"+"^00"+str(hex(startAdd))[2:])

object_file.close()
Intermediate_File.close()
listing_file.close()


	 
				

			  
								

		

def RSUB ( opcode): 
	 code = OpTable[op_code[0:]]
	 opcode = code+"0000"
	 lst.append(opcode)
	 object_file.write(opcode)	
	 object_file.write("\n")


def symbol():
	 s = symboltab[operand[0:]]
	 a=code+s
	 object_file.write(a + "\n")	
	 lst.append(a)
	 

def equ():
	 w= Literal_Pool[str(operand)[1:]]
	 b=code+w[2]
	 object_file.write(b + "\n")	
	 lst.append(b)

def index():
	 m1 = symboltab[opr][0:1]
	 m2 = symboltab[opr[0:]]
	 hexx= hex(int(bin(int(1))[-1:]+"00"+bin(int(m1))[2:]))[-1:]
	 object_file.write(OpTable[op_code[0:]] +hexx+ (m2[1]+m2[2]+m2[3]) + "\n")
	 lst.append(OpTable[op_code[0:]] +hexx+ (m2[1]+m2[2]+m2[3]))
		  

def byte():
	 y = operand[2:len(operand)-1]	
	 if"C'" in operand:
		  h = ""
		  for i in y:	
				object_file.write(str(hex(ord(i))[2:]))
				h+=hex(ord(i))[2:]
		  lst.append(h )
		  object_file.write("\n")
				 
	 elif "X'" in operand:
		  object_file.write(y+ "\n")
		  lst.append(y)

def word():
	 x1 = str(hex(int(operand)))
	 x1 = x1[2:]
	 if len(x1)<6:
		  for i in range(6-len(x1)):
				x1 = "0"+x1	 		
	 object_file.write(x1 + "\n")		
	 lst.append(x1)


def star():
	 z = Literal_Pool[str(op_code)[1:]]
	 object_file.write(z[0] + " \n")	
	 lst.append(z[0])


