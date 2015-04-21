apps
====

#How to sync the files in different machine
	rsync -rpvz .  hduser@hadoop:~/Downloads/apps/


my apps , python etc code

------------------------------------------------------------------
DIRECTED GRAPH
-----------------------------------------------------------------

How to install and use GCC g++ v4.7 and C++11 on Ubuntu 12.04 (beta) . This is required to compile directed_graph.cpp
>> http://charette.no-ip.com:81/programming/2011-12-24_GCCv47/

Analysis : This problem is related to directed graph algo ( nodes with Ids and edges with equal distance ) and this can be converted into as finding the longest distance in the directed graph which covers all the node and graph is not cyclic though cyclic condition has been taken care. This problem is NP hard problem some thing like [ Travelling sales man problem].
Assumption : Program output will display the all possible subset of the list that is for the given sample in the mail and the I have also provided a screen shot of the same.

P3 , P1 , P2
P1 , P2
P3 , P2


How to compile?
The code <<attached file directed_graph_v6.cpp>> is compatible with c++11 and below is the compiler details I have used.
#g++-4.7 (Ubuntu/Linaro 4.7.3-2ubuntu1~12.04) 4.7.3
#Copyright (C) 2012 Free Software Foundation, Inc.
#This is free software; see the source for copying conditions.  There is NO
#warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

command prompt> /usr/bin/g++-4.7 -std=c++11 --std=c++11 directed_graph_v6.cpp ;

How to Run?
Compile the code as mentioned above and run the executable file a.out which was created by compiling the code . Sample of run is provided in screen shot. Provide the inputs like sample 1 and sample 2. If user has provided all the inputs then type done . Sample of a run has been shown in the screen shot.

Unit test cases?
SAMPLE 1
1 won against 2
2 lost to 3
3 won against 1

SAMPLE2
p1 won against p2
p2 lost to p3
p3 won against p1


