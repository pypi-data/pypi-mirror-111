from socket import gethostname
import os
#Copyright © 2021 Jaden Ong. All rights reserved
#Version 1.3
print(__file__)
print(os.getcwd())
class CalDB:
    def __init__(self,sysName):
        self.name = sysName
    def start(self,name):
        self.dbname = name
        try:
            open(f"{self.dbname}.cal","r")
        except FileNotFoundError:
            with open(f'{self.dbname}.cal','w') as f:
                f.write(f'''#!Cal++ Version 3.2 - CalDB Version 1.2
#!{self.dbname} - {gethostname()}''')
                
    def read(self):
        with open(f'{self.dbname}.cal','r') as f:
            text = []
            for line in f:
                if line.startswith('#!'):
                    pass
                else:
                    text.append(line)
            text = ''.join(text)
            return text
    def write(self,key,value,dataType="str"):
        #do something to check if key already exists
        with open(f'{self.dbname}.cal','a') as f:
            if dataType == "str":
                writtenValue = "\"" + value + "\""
            elif dataType == "int":
                writtenValue = int(value)
            else:
                writtenValue = "\"" + value + "\""
            f.write(f',\n{key} = {writtenValue}')
    def kill(self,key):
        with open(f'{self.dbname}.cal','r') as f:
            text = []
            for line in f:
                if line.startswith(key):
                    pass
                else:
                    text.append(line)
            text = ''.join(text)
            with open(f'{self.dbname}.cal','w') as f:
                f.write(text)
    
    class array:
        def json(name):
            data = array.json(name)
            return data
            

class array:
    def json(name):
        name = name.replace("\n","")
        name = name.split(",",-1)
        data = {}
        for item in name:
            item = item.replace('"','')
            item = item.replace('=','')
            item = item.split(" ",2)
            data[item[0]] = item[2]
            
        return data



