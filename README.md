# Asyncronous-Rsync
Sending multiple files asynchronously using rsync.  


The program gets the source files and directories separated by spaces, a destination and a bandwidth limit.  
how to run example:  
python3 sender_multiprocessing.py "my dir 1/hello1.txt" "my dir 1/hello2.txt" "my dir 1/hellos" "my dir 2" 512  
In this example two files and a directory from "my dir 1" source directory are sent to "my dir 2" directory with a bandwidth limit of 512 kb/sec.  

There is a test that creates temporary source and destination directories, and two files of 5mb and 10mb at the source directory.  
The test sends them using the code from sender_multiprocessing.py, and checks if they were sent in parallel and arrived complete.  
It also shows which tests passed.  
How to test:  
python3 test_rsync_multiprocessing.py  

