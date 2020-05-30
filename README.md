DOCUMENTATION::
**************************************************************BRIEF**************************************************************************
Author:
	Abhimanyu Gupta (guptaabhimanyu23@gmail.com)
Functionality:
	Simulates working of Cache in different types of mapping
Purpose:
	End Semester Assignment for CSE112-Computer Organization, Winter Semester 2020 at IIIT Delhi

**********************************************************************************************************************************************

******************************************************INPUT/OUTPUT FORMAT*************************************************************
Input:
	* Length of main memory working with.
	* Size of Cache in focus. (Incase of 2 level cache, size of level 2 Cache)
	* Size of each Cache Line. (Main Memory Block Size will also be equal to this)
	* Type of Cache Mapping to be applied.
	* Number of sets. (Only applicable when selected N-way Set Associative Mapping) 
	* Operation (read/write) to be performed on cache in different lines.
	* 'E' (without quotes) to exit simulation any time.
Output:
	* Cache Memory after each read/write.

**********************************************************************************************************************************************

**********************************************************PROGRAM FLOW******************************************************************
* The complete description of Main memory and Cache memory is taken from the user as input.
* Each querry is read (querry here means, read/write command) from the user.
* Read querry only contains a single address, which has to be read.
* Write querry contains the address followed by the value which needs to be written on the address.
* The complete cache is printed after each querry.

Main Memory - Cache Memory Interactions:
* The two memories interact with each other on 'Write Back' principle, i.e. the block in Main Memory isn't updated till it lies in cache, irrespective of  if it is continously accessed or not.

Level 1 - Level 2 Cache Interactions:
* The two caches follow a 'Exclusive' Policy with each other, i.e. at any point of time they contains different blocks of memory from the Main Memory, irrespective of  space not being used in one. 

Cache Replacement Scheme:
* Least Recently Used - remove the least recently used block when the cache is full and a new block is requested which is not there in cache.

Types of Mapping featured:
* Direct Mapping
* Fully Associative Mapping
* N-way Set Associative Mapping

ASSUMPTIONS IN THE FLOW:
* Each word occupies exactly one unit of memory, i.e. for a cache line of size B, there are exactly B words in that line at any instacne.
* Level 1 and Level 2 Caches are mapped with same type of mapping.

**********************************************************************************************************************************************

***************************************************ERROR HANDLING******************************************************************
* The following errors are taken care of while building the program
	1) The address length is not a Natural number.
	2) Cache Size, Cache Line Size, Number of Sets are not in the form of 2^(x) for any non negative x.
	3) Size of Cache is more than Main Memory size.
	4) The number of Sets in N-way Set Asscociative Mapping exceeds number of cache lines.
	5) Address is not a binary address or is of  not of  adequate size.
	6) The value to be written is only a single word/number without any inbetween spaces.

**********************************************************************************************************************************************

***************************************************INSTRUCTIONS TO RUN******************************************************************
Language and Version Support:
* The program has been completely written in Python 3.8.1.

Method 1:    Using command prompt or terminal
	  * Run the cmd/termial in the folder where code file -"cache1.py" or "cache2.py" is present.
	  * Enter "python cache1.py" or "python cache2.py" (without quotes) to run single level and 2 level cache simulation respectively.
	  * Provide input in adequate format as stated above in Input section.
Method 2:    Using IDE
	  * Compile and run the python code.
	  * Provide input in adequate format as stated above in Input section.

**********************************************************************************************************************************************
