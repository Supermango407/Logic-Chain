import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Logic_Chain"
)
cursor = mydb.cursor(buffered=True)


class Opinion(object):
    opinions = {}

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
