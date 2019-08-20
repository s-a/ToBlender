bl_info = {
    "name": "2Blender",
    "author": "Stephan Ahlf",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "World > Watch",
    "description": "Watch files for code changes to reload.",
    "warning": "",
    "wiki_url": "",
    "category": "Tools",
}

import bpy
import socket as socket
import sys
import os

import threading
import time

import addon_utils

class ToBlender(object):
    """ Threading example class

    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor

        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.running = True
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                            # Daemonize thread
        self.thread.start()                                  # Start the execution

    def processRemoteCommand(self, cmd):
        exists = os.path.isfile(cmd)
        if exists:
            print ('try execute "' + cmd + '"')
            exec(compile(open(cmd).read(), cmd, 'exec'))
            return True
        else:
            addonName = cmd
            print ('try restart "' + addonName + '"')
            addon_utils.disable(addonName)
            addon_utils.enable(addonName)
            return True

        print ('no command given')
        return False

    def run(self):
        """ Method that runs forever """
        # Create a TCP/IP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 3001)
        self.socket.settimeout(1)
        print ('starting up on %s port %s' % self.server_address)
        self.socket.bind(self.server_address)

        # Listen for incoming connections
        self.socket.listen(1)

        print ('waiting for a connection that informs about code changes...')
        while self.running:    
            try:
                connection, client_address = self.socket.accept()
            except socket.timeout:
                if (self.running):
                    continue
                else:
                    break

            print (client_address)
            try:
                print ('client connected:', client_address)
                while self.running:
                    try:
                        data = connection.recv(4096)
                        dataString = data.decode("utf-8")
                        if(dataString != None and dataString != ""):
                            print ('received command "%s"' % data)
                            self.processRemoteCommand(dataString)
                        connection.sendall(("processed \"" + dataString  + "\"").encode())
                    except Exception as e: 
                        try:
                            connection.sendall(str(e).encode())
                            print(e)
                        except:
                            pass
                        break
            finally:
                connection.close()            
                time.sleep(self.interval)
        print ('server stopped')
            
    def stop(self):
        self.running = False

    def __del__(self):
        self.stop()

server = None

def register():  
    global server
    server = ToBlender()

def unregister():
    global server
    print('stopping server...')
    server.stop()
    del server

if __name__ == "__main__":
    register()