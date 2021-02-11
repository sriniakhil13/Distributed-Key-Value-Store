import socket
from store_data import DataStore
import json,time
from _thread import *

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Please unzip DKV folder and run 'python3 servernode.py' for each node. You need unzip the folder to multiple locations to run multiple nodes")
port_for_this_node = input("Enter port to run this node: ")
serv.bind(('0.0.0.0', int(port_for_this_node)))
serv.listen(5)
other_nodes_ip = []
other_nodes_ports = []
x = input("Number of other nodes you want to run: ")
for i in range(0,int(x)):
    other_nodes_ip.append('0.0.0.0')
    port_temp = input("Enter port of other Node: ")
    other_nodes_ports.append(int(port_temp))

def client_request(conn):
    from_client = ''
    while True:    
        data = conn.recv(4096)
        if not data: break
        from_client += data.decode()
        print(from_client)
        to_send_other_nodes = "SERVER " + from_client
        if from_client.find('SERVER') != -1:
            command_recvd = from_client.split(" ")
            command = command_recvd[1]
            key = command_recvd[2]
            if command != 'GET':
                value = command_recvd[3]
        else:
            command_recvd = from_client.split(" ")
            command = command_recvd[0]
            key = command_recvd[1]
            if command != 'GET':
                value = command_recvd[2]
        response = ''
        dic_list = []
        if command == "SET":
            obj = DataStore()
            response = str(obj.set(key, value))
            print(response)
        if command == "GET":
            obj = DataStore()
            response = str(obj._get(key))
            try:
                dic_list.append(json.loads(response.replace("'", "\"")))
            except:
                print("No record found")
            print(response)
        if command == "EXPIRE":
            obj = DataStore()
            response = str(obj.expire(key, value))
            print(response)

        if from_client.find('SERVER') == -1:
            print("Entered into broadcast area")

            for i in range(0, len(other_nodes_ip)):
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((other_nodes_ip[i], int(other_nodes_ports[i])))
                    client.send(to_send_other_nodes.encode('utf-8'))
                    from_node = client.recv(4096)
                    print("Broadcast node response", from_node)
                    from_node = from_node.decode('utf-8')

                    if command == 'GET':
                        try:
                            from_node = json.loads(from_node.replace("'", "\""))
                            dic_list.append(from_node)
                        except:
                            print("No value found may be")

                    client.close()
                except:
                    print("Node down !")
            sorted(dic_list, key=lambda i: i["record_modified_time"])
            if len(dic_list) > 0:
                if dic_list[0]['expire_time'] == '' or dic_list[0]['expire_time'] > str(round(time.time())):
                    response = dic_list[0]["value"]
                else:
                    response = "Expired !!"
        response = response.encode('utf-8')
        print("finalprint", response)

        conn.send(response)
    conn.close()
    print('client disconnected')
while True:
    conn, addr = serv.accept()
    print(addr)
    host = addr[0]
    port = addr[1]
    start_new_thread(client_request, (conn,))
