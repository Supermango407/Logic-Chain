import mysql.connector

opinions = {}
statments = {}
reasons = {}

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Logic_Chain"
)
cursor = mydb.cursor(buffered=True)

cursor.execute("SELECT `id`, `table_name` FROM `reason_types`") 
reason_types = [i[1] for i in cursor.fetchall()]


class Opinion(object):

    def __init__(self, text:list, pros:list, cons:list):
        self.text = text
        self.pros = []
        self.cons = []

        for pro in pros:
            self.pros.append(reasons[pro])

        for con in cons:
            self.cons.append(reasons[con])
        

def load():
    global statments
    global reasons
    global opinions

    # load statments
    sql = f"SELECT `id`, `text` FROM `statments`;"
    cursor.execute(sql) 
    table = cursor.fetchall()
    for row in table:
        statments[row[0]] = row[1]
    
    # load reasons
    sql = f"SELECT `id`, `type`, `reason_id` FROM `reasons`;"
    cursor.execute(sql) 
    table = cursor.fetchall()
    for row in table:
        reasons[row[0]] = (reason_types[row[1]], row[2])
    
    # load opinion data
    opinion_ids = []
    opinion_text = []
    opinion_pros = []
    opinion_cons = []
    sql = f"SELECT `id`, `text`, `pros`, `cons` FROM `opinions`;"
    cursor.execute(sql) 
    table = cursor.fetchall()
    for row in table:
        opinion_ids.append(row[0])
        opinion_text.append(row[1])
        
        opinion_pros.append([int(i) for i in row[2].split(',')])
        opinion_cons.append([int(i) for i in row[3].split(',')])

    # save opinions
    for i, opinion_id in enumerate(opinion_ids):
        opinions[opinion_id] = Opinion(opinion_text[i], opinion_pros[i], opinion_cons[i])

