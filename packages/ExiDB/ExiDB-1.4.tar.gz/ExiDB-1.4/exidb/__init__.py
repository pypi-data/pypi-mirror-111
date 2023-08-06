"""ExiDB is a package that maybe help you at your database basically it NOSQL
based on JSON it have Query that can find you the thing that you need by search by it name"""

from .tool import *
import json
from jsonpath import JSONPath

class ExiDB:
    def __init__(self,filepath,indent=0) -> None:
        self.filepath = filepath
        self.indent = indent
        self.json_file = json.load(open(self.filepath,'r'))

    def insert(self,mapList:str,value:dict) -> None:
        "That will insert the value inside the JSON file"
        setInDict(self.filepath,mapList,value,self.indent)

    def add(self,mapList:str,value) -> None:
        "That will add the value inside the JSON file"
        setInDict(self.filepath,mapList,value,self.indent)

    def edit(self,mapList:str,value) -> None:
        "That will edit the value inside the JSON file"
        setInDict(self.filepath,mapList,value,self.indent)
    
    def append(self,mapList,value) -> None:
        appendInDict(self.filepath,mapList,value,self.indent)

    def delete(self,mapList:str) -> None:
        "That will delete the value inside the JSON file"
        delInDict(self.filepath,mapList,self.indent)

    def purge(self) -> None:
        "That will purge all the JSON file"
        delInDict(self.json_file,"All",self.indent)

    def get(self,mapList:str):
        "That will return DATA"
        return getFromDict(self.json_file,mapList)

    def all(self):
        "That will return FILE Dict"
        return self.json_file

class QueryDB:
    def __init__(self,filepath):
        self.filepath = filepath
        self.json_file = json.load(open(self.filepath,'r'))

    def search(self,mapList):
        return JSONPath(f"$..{mapList}").parse(self.json_file)

    def JSONPathRaw(self,raw):
        return JSONPath(f"{raw}").parse(self.json_file)