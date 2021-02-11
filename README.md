# Distributed-Key-Value-Store

## How to use:

```
copy DKV folder to multiple locations ( no of nodes you want to run = no of locations you copy ) 
Go into DKV folder at each location
Run python3 servernode.py
It will ask port number to run this node 
Then enter how many nodes you want to run (excluding this node )
Enter ports of those nodes
```
### Example:

```
If i want to run 3 nodes suppose
Copy DKV folder at 3 places in local system
Go into first DKV directory
Then run python3 servernode.py
Enter 7000 port
Next Enter 2 nodes ( we want to run more 2 nodes excluding this )
Now enter port 8000
next enter port 9000 for last node

Go into second DKV directory
Then run python3 servernode.py
Enter 8000 port
Next Enter 2 nodes ( we want to run more 2 nodes excluding this )
Now enter port 7000 (this node is above node which is already running)
next enter port 9000 for last node

Repeat for next node as well

```

