import sqlite3

#database_name = "customers"
#conn = sqlite3.connect('{}.db'.format(database_name))
#c = conn.cursor()

def main():
    database_name = "customers"
    conn = sqlite3.connect('{}.db'.format(database_name))
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS customers(
        client_id text,
        iphone text,
        gb text,
        color text,
        location text
        )""")

def update_Iphone(id,phone):
    database_name = "customers"
    conn = sqlite3.connect('{}.db'.format(database_name))
    c = conn.cursor()
    c.execute(f'''UPDATE customers SET iphone = '{phone}' WHERE client_id ='{id}';''')
    conn.commit()
def update_gb(id,gb):
    database_name = "customers"
    conn = sqlite3.connect('{}.db'.format(database_name))
    c = conn.cursor()
    c.execute(f'''UPDATE customers SET gb = '{gb}' WHERE client_id ='{id}';''')
    conn.commit()
def update_color(id,color):
    database_name = "customers"
    conn = sqlite3.connect('{}.db'.format(database_name))
    c = conn.cursor()
    c.execute(f'''UPDATE customers SET color = '{color}' WHERE client_id ='{id}';''')
    conn.commit()
def update_location(id,loc):
    database_name = "customers"
    conn = sqlite3.connect('{}.db'.format(database_name))
    c = conn.cursor()
    c.execute(f"UPDATE customers SET location = '{loc}' WHERE client_id ='{id}';")
    conn.commit()

def insert_Data(id,iphone,color,location):
    database_name = "customers"
    conn = sqlite3.connect('{}.db'.format(database_name))
    c = conn.cursor()
    c.execute(f"INSERT INTO customers VALUES ('{id}', '{iphone}', '{color}', '{location}')")
    conn.commit()
    conn.close()

def search_data(field,id):
    database_name = "customers"
    conn = sqlite3.connect('{}.db'.format(database_name))
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE {} LIKE '%{}%'".format(field,id))
    conn.commit()
    data = c.fetchall()
    conn.close()
    if len(data) != 0:
        print("YES YES YES")
        return True
    else:
        conn.close()
        return False

def search_iphone(field,id):
    database_name = "customers"
    conn = sqlite3.connect('{}.db'.format(database_name))
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE {} LIKE '%{}%' AND WHERE 'iphone' LIKE '%%'".format(field,id))
    conn.commit()
    dat = c.fetchall()
    if len(dat) == 0:
        conn.close()
        return False
    else:
        return True

def read_phone(id):
    try:
        database_name = "customers"
        conn = sqlite3.connect('{}.db'.format(database_name))
        c = conn.cursor()
        c.execute("SELECT * FROM customers WHERE {} LIKE '%{}%'".format("client_id",id))
        data = c.fetchone()
        conn.commit()
        return data
    except:
        print("ERROR ERROR")

main()