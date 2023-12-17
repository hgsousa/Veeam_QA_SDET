
## Rules of test:

```python

A program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder.

1) Synchronization must be one-way: after the synchronization content of the replica folder 
should be modified to exactly match content of the sourcefolder;

2) Synchronization should be performed periodically.

3) File creation/copying/removal operations should be logged to a file and to the console output;

4) Folder paths, synchronization interval and log file path should be provided using the command line arguments;

5) It is undesirable to use third-party libraries that implement folder synchronization;

6) It is allowed (and recommended) to use external libraries implementing other well-known algorithms. 

```

## Use script
```python

Path to source folder and Path to replica folder should exist 
Synchronization time is in seconds
Path to log file is needed

