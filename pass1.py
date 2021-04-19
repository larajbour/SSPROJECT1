 
 #PASS 1 

import tkinter as tk
from tkinter import filedialog , Text 
import os 
from tkinter import *



Directives =[ "START", "END", "BYTE", "WORD", "RESB", "RESW", "LTORG"]
#Input Files
sourceFile = open("sourceFile.asm", "r")
opCodeFile = open("opCodeFile.txt ","w+")

#Output Files 
symbolFile = open("symbolFile.txt","w+")
IntermediateFile = open("IntermediateFile.mdt","w+")
literalFile= open("literalFile.txt", "w+")
ErrorFile = open("errorFile.txt","w+")

#initialize components
ProgName = ""
Literal_Table ={}
OpTable = {}
symboltab = {}
Literal_Pool = {}
label = ""
opCode = ""
E_Found = 0
startAdd = 0


#store opcode table in  list
for line in opCodeFile:
    OpTable[line[0:10].split(' ')[0]] = line[11:20].strip()
    
#read first line
SIC_Inst = sourceFile.readlines()
firstLine = SIC_Inst[0]
if firstLine[11:20].strip() == "START":
    startAdd = int(firstLine[21:38].strip(),16)
    ProgName =  firstLine[0:10].strip()
    LocCtr = startAdd
    
    blank = 10-len(str((LocCtr)))
    v =hex(LocCtr)[2:]
    IntermediateFile.write(v + " " *blank+firstLine)
    
    
else:
    LocCtr = 0

for index , line in enumerate(SIC_Inst):
    opCode = line[11:20].strip()
    if(opCode != "START" and opCode!= "END" ):
        if line[0] != '.':  
            if(opCode != "LTORG"): 
                blank = 10-len(str((LocCtr)))
                b=hex(LocCtr)[2:]+" "*blank+line
                IntermediateFile.write(b)
            else :
                IntermediateFile.write(" "*10+line)

            label = line[0:10].strip()
            if label != "":
                if label not in symboltab:
                    symboltab[label] = hex(LocCtr)[2:]
                    symbolFile.write(symboltab[label]+" "*10)
                    symbolFile.write(line[0:10].strip() + "\n")    
                else :
                    E_Found = 1
                    print( "This" +label+"lable is already exists"  )
                    ErrorFile.write("This" +label+"lable is already exists"+"\n" )
                    break
        
                

            e = 0 
            if opCode not in OpTable:
                Operand = 0
            else:
                e = 1
                LocCtr += 3 


           
            if (e == 0 and opCode in Directives):
                
                if opCode == "WORD":
                    LocCtr += 3 
                    
                elif opCode == "RESW":
                     Operand = line[21:38].strip()
                     LocCtr += 3 
                     LocCtr = LocCtr * int(Operand)
                elif opCode == "RESB":
                    Operand = line[21:38].strip()
                    LocCtr += int(Operand) 
                elif opCode == "BYTE":
                        Operand = line[21:38].strip()
                        if Operand[0] == 'C':
                            LocCtr += (len(Operand)-3)
                        elif Operand[0] == 'X':
                            LocCtr += int((len(Operand)-3)/2)
                elif opCode == "LTORG":
                    for x in Literal_Table:
                        Literal_Table[x][2] = hex(LocCtr)[2:] 
                        blank = 10-len(str((LocCtr)))
                        IntermediateFile.write(hex(LocCtr)[2:]+" "*blank+"*"+" "*7+"="+x+"\n")
                        LocCtr = LocCtr +  int(Literal_Table[x][1])
                    Literal_Table = {}

            if line[21:22] == '=':
                Literal_List = []
                found = 1
                literal = line[22:38].strip()
                if literal[0]=='C':
                    hexadecimalC = literal[2:-1].encode("utf-8").hex()
                elif literal[0]== 'X':
                    hexadecimalC = literal[2:-1]

                else:
                    ErrorFile.write("not tru literal  : "+" "+line[22:39].strip())
                    print("Tihs literal is not true")
                    break
                

                if literal  not in Literal_Pool :
                    Literal_List=[hexadecimalC,len(hexadecimalC)/2, 0]
                    Literal_Table[literal]= Literal_List
                    Literal_Pool[literal]= Literal_List
                    literalFile.write(str(Literal_Pool[literal]) + "\n") 
                    
                else:
                    exist = 0


            op = line[11:20].strip()

            if (op not in OpTable and op not in Directives):
                ErrorFile.write("not True opcode "+ "\n")
                print("not True opcode ")
                
                break
             
if opCode == "END":
    IntermediateFile.write(" "*10+line)
if Literal_Table:   
    for y in Literal_Table:
        Literal_Table[y][2] = hex(LocCtr)[2:]
        blank = 10-len(str((LocCtr)))
        IntermediateFile.write(hex(LocCtr)[2:]+" "*blank+"*"+" "*7+"="+y+"\n")
        LocCtr = LocCtr + int(Literal_Table[y][1])


programLength = 0
lastaddress=LocCtr
ProgLen = int(lastaddress) - int(startAdd)
ProgLen1 = hex(int(ProgLen))[2:].format(int(ProgLen))
LocCtr1 = hex(int(LocCtr))[2:].format(int(LocCtr))

sourceFile.close()
opCodeFile.close()
IntermediateFile.close()





# GUI
root = tk.Tk()
root.title("SIC Assembler ") 
P_L = Label(root ,text = " LOCCTR -->" + str(LocCtr1) , font='time 15 bold roman ', fg='red')
P_L.pack()

P_L = Label(root ,text = " PRGLTH -->" + str(ProgLen1) , font='time 15 bold roman ', fg='red')
P_L.pack() 

P_N = Label(root ,text = "PRGNAME -->" + ProgName, font='time 15 bold roman', fg='red')
P_N.pack()


TI = Label(root, text=" SYBTAB  ", font= 'time 15 bold roman ' , fg='black')
TI.pack()

ST = Text(root ,font='time 15 bold roman' , height=100, width=100 )
ST.configure(background = "white")
ST.insert(END,symboltab)
ST.pack()


literals = Label(root, text=" Literal  :", font='time 15 bold roman')
literals.pack()
literals1 = Text(root, height=100, width=100 , font='time 15 roman'  )
literals1.insert(END,Literal_Table)
literals1.pack()
root.mainloop()




