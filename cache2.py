'''Brief:
	Author-0deadLock0
	Contact- guptaabhimanyu23@gmail.com
	Functionality- Simulation of two level cache
'''

import math

memoryAddresslength=16
mainMemorySize=2**memoryAddresslength
blocksCount=None
blockSize=None
mainMemory=None

def is_in_power_of_2(num):
	return num!=0 and (num&(num-1))==0

def is_valid_address(address,length):
	if len(address)!=length:
		return False
	for a in address:
		if a!='0' and a!='1':
			return False
	return True

def print_main():
	print()
	for i in range(blocksCount):
		print(bin(i)[2:],mainMemory[i])
	print()

def print_cache(type,cacheMemory):
	print()
	if type=='S':
		setNumber=0
		for sets in cacheMemory:
			print(bin(setNumber)[2:],"*"*6*len(sets[0][1]))
			setNumber+=1
			for cacheLines in sets:
				print(cacheLines)
	else:
		for cacheLines in cacheMemory:
			print(cacheLines)
	print()

def read_from_cache(type,cacheMemory,CacheMemory,address):
	if type=='D':
		blockOffsetSize=int(math.log2(len(cacheMemory[0][1])))
		
		lineSize1=int(math.log2(len(cacheMemory)))
		lineSize2=int(math.log2(len(CacheMemory)))
		tagSize1=memoryAddresslength-lineSize1-blockOffsetSize
		tagSize2=memoryAddresslength-lineSize2-blockOffsetSize
		
		tag1=address[0:tagSize1]
		line1=address[tagSize1:tagSize1+lineSize1]
		blockOffset=int(address[memoryAddresslength-blockOffsetSize:],2)
		tag2=address[0:tagSize2]
		line2=address[tagSize2:tagSize2+lineSize2]

		if cacheMemory[int(line1,2)][0]==tag1:
			print("Level 1 - Cache Hit")
		elif CacheMemory[int(line2,2)][0]==tag2:
			print("Level 1 - Cache Miss")
			print("Level 2 - Cache Hit")
			print("Transfering Memory from Level 2 to Level 1")

			oldTag1=cacheMemory[int(line1,2)][0]
			oldBlocks1=list(cacheMemory[int(line1,2)][1])

			cacheMemory[int(line1,2)][0]=tag1
			cacheMemory[int(line1,2)][1]=list(CacheMemory[int(line2,2)][1])

			CacheMemory[int(line2,2)][0]=None
			CacheMemory[int(line2,2)][1]=[-1 for _ in range(len(CacheMemory[0][1]))]

			if oldTag1!=None:
				oldLine2=oldTag1[-1]+line1
				oldTag2=CacheMemory[int(oldLine2,2)][0]
				oldBlocks2=list(CacheMemory[int(oldLine2,2)][1])

				CacheMemory[int(oldLine2,2)][0]=oldTag1[:-1]
				CacheMemory[int(oldLine2,2)][1]=list(oldBlocks1)

				if oldTag2!=None:
					mainMemory[int(oldLine2,2)+int(oldTag2,2)*len(CacheMemory)]=list(oldBlocks2)
		else:
			print("Level 1 - Cache Miss")
			print("Level 2 - Cache Miss")
			print("Bringing block from main memory.....")

			if cacheMemory[int(line1,2)][0]==None:
				cacheMemory[int(line1,2)][0]=tag1
				cacheMemory[int(line1,2)][1]=list(mainMemory[int(line1,2)+int(tag1,2)*len(cacheMemory)])
			else:
				oldTag1=cacheMemory[int(line1,2)][0]
				oldBlocks1=cacheMemory[int(line1,2)][1]
				
				oldLine2=oldTag1[-1]+line1
				oldTag2=CacheMemory[int(oldLine2,2)][0]
				oldBlocks2=list(CacheMemory[int(oldLine2,2)][1])

				CacheMemory[int(oldLine2,2)][0]=oldTag1[:-1]
				CacheMemory[int(oldLine2,2)][1]=list(oldBlocks1)

				if oldTag2!=None:
					mainMemory[int(oldLine2,2)+int(oldTag2,2)*len(CacheMemory)]=list(oldBlocks2)

				cacheMemory[int(line1,2)][0]=tag1
				cacheMemory[int(line1,2)][1]=list(mainMemory[int(line1,2)+int(tag1,2)*len(cacheMemory)])

		print("Value-",cacheMemory[int(line1,2)][1][blockOffset])
	elif type=='F':
		blockOffsetSize=int(math.log2(len(cacheMemory[0][1])))
		blockNumber=memoryAddresslength-blockOffsetSize
		
		block=address[:blockNumber]
		blockOffset=int(address[memoryAddresslength-blockOffsetSize:],2)

		line=-1
		for i in range(len(cacheMemory)):
			if cacheMemory[i][0]==block:
				line=i
				cacheMemory.insert(0,list(cacheMemory[line]))
				del cacheMemory[line+1]
				line=0
				print("Level 1 - Cache Hit")
				break

		if line==-1:
			print("Level 1 - Cache Miss")
			
			for i in range(len(CacheMemory)):
				if CacheMemory[i][0]==block:
					line=i
					cacheMemory.insert(0,list(CacheMemory[line]))
					del CacheMemory[line]
					if cacheMemory[-1][0]==None:
						CacheMemory.append(list(cacheMemory[-1]))
					else:
						CacheMemory.insert(0,list(cacheMemory[-1]))
					del cacheMemory[-1]
					line=0
					print("Level 2 - Cache Hit")
					print("Transfering Memory from Level 2 to Level 1")
					break

		if line==-1:
			print("Level 2 - Cache Miss")
			print("Bringing block from main memory.....")
			
			cacheMemory.insert(0,[block,list(mainMemory[int(block,2)])])
			if cacheMemory[-1][0]==None:
				CacheMemory.append(list(cacheMemory[-1]))
			else:
				CacheMemory.insert(0,list(cacheMemory[-1]))
			if CacheMemory[-1][0]!=None:
				mainMemory[int(CacheMemory[-1][0],2)]=list(CacheMemory[-1][1])
			del cacheMemory[-1]
			del CacheMemory[-1]
			line=0

		print("Value-",cacheMemory[line][1][blockOffset])
	else:
		setSize=int(math.log2(len(cacheMemory)))
		blockOffsetSize=int(math.log2(len(cacheMemory[0][0][1])))
		tagSize=memoryAddresslength-setSize-blockOffsetSize
		
		tag=address[0:tagSize]
		sets=int(address[tagSize:tagSize+setSize],2)
		blockOffset=int(address[memoryAddresslength-blockOffsetSize:],2)

		line=-1
		for i in range(len(cacheMemory[sets])):
			if cacheMemory[sets][i][0]==tag:
				line=i
				cacheMemory[sets].insert(0,list(cacheMemory[sets][line]))
				del cacheMemory[sets][line+1]
				line=0
				print("Level 1 - Cache Hit")
				break

		if line==-1:
			print("Level 1 - Cache Miss")
			
			for i in range(len(CacheMemory[sets])):
				if CacheMemory[sets][i][0]==tag:
					line=i
					cacheMemory[sets].insert(0,list(CacheMemory[sets][line]))
					del CacheMemory[sets][line]
					if cacheMemory[sets][-1][0]==None:
						CacheMemory[sets].append(list(cacheMemory[sets][-1]))
					else:
						CacheMemory[sets].insert(0,list(cacheMemory[sets][-1]))
					del cacheMemory[sets][-1]
					line=0
					print("Level 2 - Cache Hit")
					print("Transfering Memory from Level 2 to Level 1")
					break

		if line==-1:
			print("Level 2 - Cache Miss")
			print("Bringing block from main memory.....")

			cacheMemory[sets].insert(0,[tag,list(mainMemory[sets+int(tag,2)*len(cacheMemory)])])
			if cacheMemory[-1][0]==None:
				CacheMemory[sets].append(list(cacheMemory[sets][-1]))
			else:
				CacheMemory[sets].insert(0,list(cacheMemory[sets][-1]))
			if CacheMemory[sets][-1][0]!=None:
				mainMemory[sets+int(CacheMemory[sets][-1][0],2)*len(CacheMemory)]=list(CacheMemory[sets][-1][1])
			del cacheMemory[sets][-1]
			del CacheMemory[sets][-1]
			line=0

		print("Value-",cacheMemory[sets][line][1][blockOffset])

def write_to_cache(type,cacheMemory,CacheMemory,address,value):
	if type=='D':
		blockOffsetSize=int(math.log2(len(cacheMemory[0][1])))
		
		lineSize1=int(math.log2(len(cacheMemory)))
		lineSize2=int(math.log2(len(CacheMemory)))
		tagSize1=memoryAddresslength-lineSize1-blockOffsetSize
		tagSize2=memoryAddresslength-lineSize2-blockOffsetSize
		
		tag1=address[0:tagSize1]
		line1=address[tagSize1:tagSize1+lineSize1]
		blockOffset=int(address[memoryAddresslength-blockOffsetSize:],2)
		tag2=address[0:tagSize2]
		line2=address[tagSize2:tagSize2+lineSize2]

		if cacheMemory[int(line1,2)][0]==tag1:
			print("Level 1 - Cache Hit")
		elif CacheMemory[int(line2,2)][0]==tag2:
			print("Level 1 - Cache Miss")
			print("Level 2 - Cache Hit")
			print("Transfering Memory from Level 2 to Level 1")

			oldTag1=cacheMemory[int(line1,2)][0]
			oldBlocks1=list(cacheMemory[int(line1,2)][1])

			cacheMemory[int(line1,2)][0]=tag1
			cacheMemory[int(line1,2)][1]=list(CacheMemory[int(line2,2)][1])

			CacheMemory[int(line2,2)][0]=None
			CacheMemory[int(line2,2)][1]=[-1 for _ in range(len(CacheMemory[0][1]))]

			if oldTag1!=None:
				oldLine2=oldTag1[-1]+line1
				oldTag2=CacheMemory[int(oldLine2,2)][0]
				oldBlocks2=list(CacheMemory[int(oldLine2,2)][1])

				CacheMemory[int(oldLine2,2)][0]=oldTag1[:-1]
				CacheMemory[int(oldLine2,2)][1]=list(oldBlocks1)

				if oldTag2!=None:
					mainMemory[int(oldLine2,2)+int(oldTag2,2)*len(CacheMemory)]=list(oldBlocks2)
		else:
			print("Level 1 - Cache Miss")
			print("Level 2 - Cache Miss")
			print("Bringing block from main memory.....")

			if cacheMemory[int(line1,2)][0]==None:
				cacheMemory[int(line1,2)][0]=tag1
				cacheMemory[int(line1,2)][1]=list(mainMemory[int(line1,2)+int(tag1,2)*len(cacheMemory)])
			else:
				oldTag1=cacheMemory[int(line1,2)][0]
				oldBlocks1=cacheMemory[int(line1,2)][1]
				
				oldLine2=oldTag1[-1]+line1
				oldTag2=CacheMemory[int(oldLine2,2)][0]
				oldBlocks2=list(CacheMemory[int(oldLine2,2)][1])

				CacheMemory[int(oldLine2,2)][0]=oldTag1[:-1]
				CacheMemory[int(oldLine2,2)][1]=list(oldBlocks1)

				if oldTag2!=None:
					mainMemory[int(oldLine2,2)+int(oldTag2,2)*len(CacheMemory)]=list(oldBlocks2)

				cacheMemory[int(line1,2)][0]=tag1
				cacheMemory[int(line1,2)][1]=list(mainMemory[int(line1,2)+int(tag1,2)*len(cacheMemory)])

		cacheMemory[int(line1,2)][1][blockOffset]=value
		print("Value updated")
	elif type=='F':
		blockOffsetSize=int(math.log2(len(cacheMemory[0][1])))
		blockNumber=memoryAddresslength-blockOffsetSize
		
		block=address[:blockNumber]
		blockOffset=int(address[memoryAddresslength-blockOffsetSize:],2)

		line=-1
		for i in range(len(cacheMemory)):
			if cacheMemory[i][0]==block:
				line=i
				cacheMemory.insert(0,list(cacheMemory[line]))
				del cacheMemory[line+1]
				line=0
				print("Level 1 - Cache Hit")
				break

		if line==-1:
			print("Level 1 - Cache Miss")
			
			for i in range(len(CacheMemory)):
				if CacheMemory[i][0]==block:
					line=i
					cacheMemory.insert(0,list(CacheMemory[line]))
					del CacheMemory[line]
					if cacheMemory[-1][0]==None:
						CacheMemory.append(list(cacheMemory[-1]))
					else:
						CacheMemory.insert(0,list(cacheMemory[-1]))
					del cacheMemory[-1]
					line=0
					print("Level 2 - Cache Hit")
					print("Transfering Memory from Level 2 to Level 1")
					break

		if line==-1:
			print("Level 2 - Cache Miss")
			print("Bringing block from main memory.....")
			
			cacheMemory.insert(0,[block,list(mainMemory[int(block,2)])])
			if cacheMemory[-1][0]==None:
				CacheMemory.append(list(cacheMemory[-1]))
			else:
				CacheMemory.insert(0,list(cacheMemory[-1]))
			if CacheMemory[-1][0]!=None:
				mainMemory[int(CacheMemory[-1][0],2)]=list(CacheMemory[-1][1])
			del cacheMemory[-1]
			del CacheMemory[-1]
			line=0
		
		cacheMemory[line][1][blockOffset]=value
		print("Value Updated")
	else:
		setSize=int(math.log2(len(cacheMemory)))
		blockOffsetSize=int(math.log2(len(cacheMemory[0][0][1])))
		tagSize=memoryAddresslength-setSize-blockOffsetSize
		
		tag=address[0:tagSize]
		sets=int(address[tagSize:tagSize+setSize],2)
		blockOffset=int(address[memoryAddresslength-blockOffsetSize:],2)

		line=-1
		for i in range(len(cacheMemory[sets])):
			if cacheMemory[sets][i][0]==tag:
				line=i
				cacheMemory[sets].insert(0,list(cacheMemory[sets][line]))
				del cacheMemory[sets][line+1]
				line=0
				print("Level 1 - Cache Hit")
				break

		if line==-1:
			print("Level 1 - Cache Miss")
			
			for i in range(len(CacheMemory[sets])):
				if CacheMemory[sets][i][0]==tag:
					line=i
					cacheMemory[sets].insert(0,list(CacheMemory[sets][line]))
					del CacheMemory[sets][line]
					if cacheMemory[sets][-1][0]==None:
						CacheMemory[sets].append(list(cacheMemory[sets][-1]))
					else:
						CacheMemory[sets].insert(0,list(cacheMemory[sets][-1]))
					del cacheMemory[sets][-1]
					line=0
					print("Level 2 - Cache Hit")
					print("Transfering Memory from Level 2 to Level 1")
					break

		if line==-1:
			print("Level 2 - Cache Miss")
			print("Bringing block from main memory.....")

			cacheMemory[sets].insert(0,[tag,list(mainMemory[sets+int(tag,2)*len(cacheMemory)])])
			if cacheMemory[-1][0]==None:
				CacheMemory[sets].append(list(cacheMemory[sets][-1]))
			else:
				CacheMemory[sets].insert(0,list(cacheMemory[sets][-1]))
			if CacheMemory[sets][-1][0]!=None:
				mainMemory[sets+int(CacheMemory[sets][-1][0],2)*len(CacheMemory)]=list(CacheMemory[sets][-1][1])
			del cacheMemory[sets][-1]
			del CacheMemory[sets][-1]
			line=0

		cacheMemory[sets][line][1][blockOffset]=value
		print("Value updated")


if __name__=="__main__":

	memoryAddresslength=int(input("Enter length of memory address "))
	if memoryAddresslength<1:
		raise ValueError("Address length should be positive")
	mainMemorySize=2**memoryAddresslength

	cacheSize=int(input("Enter cache size "))
	if not(is_in_power_of_2(cacheSize)):
		raise ValueError("Cache Size should be in power of 2")
	if cacheSize>mainMemorySize:
		raise ValueError("Cache Size should be less than Main Memory Size")
	lineSize=int(input("Enter blockSize "))
	if not(is_in_power_of_2(lineSize)):
		raise ValueError("Block Size should be in power of 2");
	cacheLines=cacheSize//lineSize
	
	sets=None
	cacheMemory1=None
	cacheMemory2=None

	mappingType=input("Choose Mapping Type\nDirect Mapping(D)\tFully Associative Mapping(F)\tSet Associative Mapping(S)\n")
	if mappingType=='D' or mappingType=='d':
		mappingType='D'
		cacheMemory2=[[None,[-1 for _ in range(lineSize)]] for _ in range(cacheLines)]
		cacheMemory1=[[None,[-1 for _ in range(lineSize)]] for _ in range(cacheLines//2)]
	elif mappingType=='F' or mappingType=='F':
		mappingType='F'
		cacheMemory2=[[None,[-1 for _ in range(lineSize)]] for _ in range(cacheLines)]
		cacheMemory1=[[None,[-1 for _ in range(lineSize)]] for _ in range(cacheLines//2)]
	elif mappingType=='S' or mappingType=='s':
		mappingType='S'
		sets=int(input("Enter number of sets "))
		if not(is_in_power_of_2(sets)):
			raise ValueError("Number of Sets should be in power of 2");
		if sets>(cacheLines/2):
			raise ValueError("Number of Sets should be atleast 2 times the number of cache Lines");
		cacheMemory2=[[[None,[-1 for _ in range(lineSize)]] for _ in range(cacheLines//sets)] for _ in range(sets)]
		cacheMemory1=[[[None,[-1 for _ in range(lineSize)]] for _ in range((cacheLines//2)//sets)] for _ in range(sets)]
	else:
		raise TypeError("Invalid Mapping Type '"+mappingType+"'")
	
	blockSize=lineSize
	blocksCount=mainMemorySize//blockSize
	mainMemory=[[-1 for _ in range(blockSize)] for _ in range(blocksCount)]

	print()
	# print("Main-")
	# print_main()
	print("Cache 1-")
	print_cache(mappingType,cacheMemory1)
	print()
	print("Cache 2-")
	print_cache(mappingType,cacheMemory2)
	
	print("Enter each querry in seperate lines")
	print("To view a memory location, just enter the address")
	print("To write to a memory location, enter address with value to be written, on the same line")
	print("Enter "+str(memoryAddresslength)+" characters long address")
	print("Enter 'E' any time to exit the program")
	print()
	
	while True:
		querry=input()
		if querry=="E":
			print("Exit initiated")
			break

		querries=querry.strip().split(" ")
		if len(querries)<1 or len(querries)>2:
			raise TypeError("Invalid Querry")
		if not(is_valid_address(querries[0],memoryAddresslength)):
			raise TypeError("Invalid address format '"+querries[0]+"'")
		if len(querries)==1:
			read_from_cache(mappingType,cacheMemory1,cacheMemory2,querries[0]);
		else:
			write_to_cache(mappingType,cacheMemory1,cacheMemory2,querries[0],querries[1]);

		print()
		# print("Main Memory")
		# print_main()
		print("Cache Level 1:")
		print_cache(mappingType,cacheMemory1)
		print("Cache Level 2:")
		print_cache(mappingType,cacheMemory2)