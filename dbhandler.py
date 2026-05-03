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

    def __init__(self, id:int, name:str):
        self.id:int = id
        self.name:str = name
        self.children_directories:list[Directory] = []
        self.children_opinions:list[Opinion] = []
    
    def add_directory(self, directory:Directory) -> None:
        """adds `directory` to `self.children`."""
        self.children_directories.append(directory)

    def add_opinion(self, opinion:Opinion) -> None:
        """adds `opinion` to `self.children`."""
        self.children_opinions.append(opinion)


class Opinion(object):
    opinions:dict[int, Opinion] = {}

    def __init__(self, id:int, text:str, name:str=""):
        self.id:int = id
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

    def is_statement(self) -> bool:
        """will be True if there are not pros or cons."""
        return len(self.cons) == 0 and len(self.pros) == 0


def load():
    Opinion.opinions.clear()

    # create Directories
    sql = f"SELECT `id`, `name`, `parent` FROM `directories`;"
    cursor.execute(sql) 
    table = cursor.fetchall()

    for row in table:
        id:int = row[0]
        name:str = row[1]
        parent_id:int = row[2]

        directory:Directory = Directory(id, name)
        Directory.directories[id] = directory

        # add to `top_directories` if top level directory
        if parent_id == 0:
            Directory.top_directories[row[0]] = directory
        else:
            Directory.directories[parent_id].add_directory(directory)

    # create opinions
    sql = f"SELECT `id`, `directory`, `name`, `text`, `pros`, `cons` FROM `opinions`;"
    cursor.execute(sql) 
    table = cursor.fetchall()
    
    ids = []
    pros = {}
    cons = {}
    for row in table:
        ids.append(row[0])
        opinion:Opinion = Opinion(row[0], row[3], row[2])
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
            Directory.directories[row[1]].add_opinion(opinion)

    for i in ids:
        Opinion.opinions[i].set_links(pros[i], cons[i])


def create_directory(name:str, parent_id:int=0) -> None:
    """creates a directory in the database."""
    sql = f"INSERT INTO `directories` (`name`, `parent`) VALUES ('{name}', {parent_id});"
    cursor.execute(sql)

    sql = f"SELECT `id` FROM `directories` WHERE `name`='{name}' AND `parent`={parent_id};"
    cursor.execute(sql)
    id = cursor.fetchone()[0]
    
    directory:Directory = Directory(id, name)
    Directory.directories[id] = directory
    Directory.directories[parent_id].add_directory(directory)


def create_opinion(text:str, name:str, directory_id:int=0) -> None:
    """creates an opinion in the database."""
    sql = f"INSERT INTO `opinions` (`text`, `name`, `directory`) VALUES ('{text}', '{name}', {directory_id});"
    cursor.execute(sql)
    
    sql = f"SELECT `id` FROM `opinions` WHERE `text`='{text}' AND `name`='{name}' AND `directory`={directory_id};"
    cursor.execute(sql)
    id = cursor.fetchone()[0]
    print(id)
    
    opinion:Opinion = Opinion(id, text, name)
    Opinion.opinions[id] = opinion
    Directory.directories[directory_id].add_opinion(opinion)


def edit_opinion_text(opinion_id:int, new_text:str) -> None:
    """edits the text of an opinion in the database."""
    print(new_text)
    sql = f"UPDATE `opinions` SET `text`='{new_text}' WHERE `id`={opinion_id};"
    cursor.execute(sql)
    Opinion.opinions[opinion_id].text = new_text

