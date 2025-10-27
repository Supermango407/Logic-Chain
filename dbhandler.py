from __future__ import annotations
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Logic_Chain"
)
cursor = mydb.cursor(buffered=True)


class Directory(object):
    directories:dict[int, Directory] = {}
    top_directories:dict[int, Directory] = {}

    def __init__(self, name:str):
        self.name:str = name
        self.children:list[Directory | Opinion] = []
    
    def add_child(self, child:Directory) -> None:
        """adds `child` to `self.children`."""
        self.children.append(child)


class Opinion(object):
    opinions:dict[int, Opinion] = {}

    def __init__(self, text:str, name:str=""):
        self.text = text
        self.name = name
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


def load():
    global opinions
    Opinion.opinions.clear()

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

    # create opinions
    sql = f"SELECT `id`, `directory`, `name`, `text`, `pros`, `cons` FROM `opinions`;"
    cursor.execute(sql) 
    table = cursor.fetchall()
    
    ids = []
    pros = {}
    cons = {}
    for row in table:
        ids.append(row[0])
        opinion:Opinion = Opinion(row[3], row[2])
        Opinion.opinions[row[0]] = opinion
        if row[4]:
            pros[row[0]] = row[4].split(',')
        else:
            pros[row[0]] = []
        
        if row[5]:
            cons[row[0]] = row[5].split(',')
        else:
            cons[row[0]] = []

        if row[1] != 0:
            Directory.directories[row[1]].children.append(opinion)

    for i in ids:
        Opinion.opinions[i].set_links(pros[i], cons[i])

