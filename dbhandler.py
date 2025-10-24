from __future__ import annotations
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Logic_Chain"
)
cursor = mydb.cursor(buffered=True)


class Opinion(object):
    opinions:dict[int, Opinion] = {}

    def __init__(self, text:list):
        self.text = text
        self.pros:list[Opinion] = []
        self.cons:list[Opinion] = []
    
    def set_links(self, pros:dict[str], cons:dict[str]):
        """set the pros and cons of Opinion"""
        if pros:
            for pro in pros:
                self.pros.append(Opinion.opinions[int(pro)])
        if cons:
            for con in cons:
                self.cons.append(Opinion.opinions[int(con)])
        

    def is_statment(self) -> bool:
        """will be True if there are not pros or cons."""
        return len(self.cons) == 0 and len(self.pros) == 0


class Directory(object):
    directories:dict[int, Directory] = {}
    top_directories:dict[int, Directory] = {}

    def __init__(self, name:str):
        self.name:str = name
        self.children:list[Directory] = []
    
    def add_child(self, child:Directory) -> None:
        """adds `child` to `self.children`."""
        self.children.append(child)


def load():
    global opinions
    Opinion.opinions.clear()

    # create opinions
    sql = f"SELECT `id`, `text`, `pros`, `cons` FROM `opinions`;"
    cursor.execute(sql) 
    table = cursor.fetchall()
    
    ids = []
    pros = {}
    cons = {}
    for row in table:
        ids.append(row[0])
        Opinion.opinions[row[0]] = Opinion(row[1])
        if row[2]:
            pros[row[0]] = row[2].split(',')
        else:
            pros[row[0]] = []
        
        if row[3]:
            cons[row[0]] = row[3].split(',')
        else:
            cons[row[0]] = []

    for i in ids:
        Opinion.opinions[i].set_links(pros[i], cons[i])

    # create Directories
    sql = f"SELECT `id`, `name`, `parrent` FROM `directories`;"
    cursor.execute(sql) 
    table = cursor.fetchall()

    for row in table:
        id:int = row[0]
        name:str = row[1]
        parrent_id:int = row[2]

        directory:Directory = Directory(name)
        Directory.directories[id] = directory

        # add to `top_directorys` if top level directory
        if parrent_id == 0:
            Directory.top_directories[row[0]] = directory
        else:
            Directory.directories[parrent_id].add_child(directory)

