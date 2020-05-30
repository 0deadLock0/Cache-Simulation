'''Brief:
	Author-0deadLock0
	Contact- guptaabhimanyu23@gmail.com
	Functionality- Simulation of single level cache
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

def read_from_cache(type,cacheMemory,address):
	if type=='D':
		lineSize=int(math.log2(len(cacheMemory)))
		blockOffsetSize=int(math.log2(len(cacheMemory[0][1])))
		tagSize=memoryAddresslength-lineSize-blockOffsetSize
		
		tag=address[0:tagSize]
		line=int(address[tagSize:tagSize+lineSize],2)
		blockOffset=int(address[memoryAddresslength-blockOffsetSize:],2)

		if cacheMemory[line][0]==tag:
			print("Cache Hit")
		else:
			print("Cache Miss")
			print("Bringing block from main memory.....")
			
			oldTag=None
			oldBlocks=None
			replace=False
			if cacheMemory[line][0]!=None:
				oldTag=cacheMemory[line][0]
				replace=True
				oldBlocks=list(cacheMemory[line][1])
			
			cacheMemory[line][0]=tag
			cacheMemory[line][1]=list(mainMemory[line+int(tag,2)*len(cacheMemory)])
			
			if replace:
				mainMemory[line+int(oldTag,2)*len(cacheMemory)]=list(oldBlocks)	

		print("Value-",cacheMemory[line][1][blockOffset])
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
				print("Cache Hit")
				break

		if line==-1:
			print("Cache Miss")
			print("Bringing block from main memory.....")
			
			cacheMemory.insert(0,[block,list(mainMemory[int(block,2)])])
			if cacheMemory[-1][0]!=None:
				mainMemory[int(cacheMemory[-1][0],2)]=list(cacheMemory[-1][1])
			del cacheMemory[-1]
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
				print("Cache Hit")
				break

		if line==-1:
			print("Cache Miss")
			print("Bringing block from main memory.....")
			
			cacheMemory[sets].insert(0,[tag,list(mainMemory[sets+int(tag,2)*len(cacheMemory)])])
			if cacheMemory[sets][-1][0]!=None:
				mainMemory[sets+int(cacheMemory[sets][-1][0],2)*len(cacheMemory)]=list(cacheMemory[sets][-1][1])
			del cacheMemory[sets][-1]
			line=0

		print("Value-",cacheMemory[sets][line][1][blockOffset])

def write_to_cache(type,cacheMemory,address,value):
	if type=='D':
		lineSize=int(math.log2(len(cacheMemory)))
		blockOffsetSize=int(math.log2(len(cacheMemory[0][1])))
		tagSize=memoryAddresslength-lineSize-blockOffsetSize
		
		tag=address[0:tagSize]
		line=int(address[tagSize:tagSize+lineSize],2)
		blockOffset=int(address[memoryAddresslength-blockOffsetSize:],2)

		if cacheMemory[line][0]==tag:
			print("Cache Hit")
			cacheMemory[line][1][blockOffset]=value
		else:
			print("Cache Miss")
			print("Bringing block from main memory.....")
			
			oldTag=None
			oldBlocks=None
			replace=False
			if cacheMemory[line][0]!=None:
				oldTag=cacheMemory[line][0]
				replace=True
				oldBlocks=list(cacheMemory[line][1])
			
			cacheMemory[line][0]=tag
			cacheMemory[line][1]=list(mainMemory[line+int(tag,2)*len(cacheMemory)])
			cacheMemory[line][1][blockOffset]=value

			if replace:
				mainMemory[line+int(oldTag,2)*len(cacheMemory)]=list(oldBlocks)

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
				print("Cache Hit")
				break

		if line==-1:
			print("Cache Miss")
			print("Bringing block from main memory.....")
			
			cacheMemory.insert(0,[block,list(mainMemory[int(block,2)])])
			if cacheMemory[-1][0]!=None:
				mainMemory[int(cacheMemory[-1][0],2)]=list(cacheMemory[-1][1])
			del cacheMemory[-1]
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
				print("Cache Hit")
				break

		if line==-1:
			print("Cache Miss")
			print("Bringing block from main memory.....")
			
			cacheMemory[sets].insert(0,[tag,list(mainMemory[sets+int(tag,2)*len(cacheMemory)])])
			if cacheMemory[sets][-1][0]!=None:
				mainMemory[sets+int(cacheMemory[sets][-1][0],2)*len(cacheMemory)]=list(cacheMemory[sets][-1][1])
			del cacheMemory[sets][-1]
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
	cacheMemory=None
	
	mappingType=input("Choose Mapping Type\nDirect Mapping(D)\tFully Associative Mapping(F)\tSet Associative Mapping(S)\n")
	if mappingType=='D' or mappingType=='d':
		mappingType='D'
		cacheMemory=[[None,[-1 for _ in range(lineSize)]] for _ in range(cacheLines)]
	elif mappingType=='F' or mappingType=='F':
		mappingType='F'
		cacheMemory=[[None,[-1 for _ in range(lineSize)]] for _ in range(cacheLines)]
	elif mappingType=='S' or mappingType=='s':
		mappingType='S'
		sets=int(input("Enter number of sets "))
		if not(is_in_power_of_2(sets)):
			raise ValueError("Number of Sets should be in power of 2");
		if sets>cacheLines:
			raise ValueError("Number of sets should be less than or equal to number of cache lines")
		cacheMemory=[[[None,[-1 for _ in range(lineSize)]] for _ in range(cacheLines//sets)] for _ in range(sets)]
	else:
		raise TypeError("Invalid Mapping Type '"+mappingType+"'")
	
	blockSize=lineSize
	blocksCount=mainMemorySize//blockSize
	mainMemory=[[-1 for _ in range(blockSize)] for _ in range(blocksCount)]

	print()
	# print("Main-")
	# print_main()
	print("Cache-")
	print_cache(mappingType,cacheMemory)
	print()
	
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
			read_from_cache(mappingType,cacheMemory,querries[0]);
		else:
			write_to_cache(mappingType,cacheMemory,querries[0],querries[1]);

		print()
		# print("Main Memory")
		# print_main()
		print("Cache Memory")
		print_cache(mappingType,cacheMemory)