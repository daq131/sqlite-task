import sqlite3
from sqlite3 import Error

# łączenie z bazą
def create_connection(db_file):
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)
   return conn

# obiekt połączenia do bazy danych
def execute_sql(conn, sql):
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)
# dodawanie danych
def add_agent(conn, agent):
    sql = '''INSERT or REPLACE into agents(id, a_name, a_city)
    VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, agent)
    conn.commit()
    return cur.lastrowid

def add_customer(conn, customer):
    sql = ''' INSERT or REPLACE INTO customers(agents_id, c_name, c_city)
    VALUES(?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid

def select_all(conn, table):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return rows

def select_where(conn, table, **query):
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows

def update(conn, table, id, **kwargs):
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id,)

    sql = f''' UPDATE {table}
                SET {parameters}
                WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationalError as e:
        print(e)

def delete_where(conn, table, **kwargs):
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

def delete_all(conn, table):
   sql = f'DELETE FROM {table}'
   cur = conn.cursor()
   cur.execute(sql)
   conn.commit()
   print("Deleted")

if __name__ == '__main__':
    # tworzymy tabele
    create_agents_sql = """
    -- projects table
    CREATE TABLE IF NOT EXISTS agents(
       id INTEGER PRIMARY KEY,
       a_name VARCHAR(40) NOT NULL,
       a_city VARCHAR(25) NOT NULL
    );
   """
    create_customers_sql = """
   CREATE TABLE IF NOT EXISTS customers(
       id integer PRIMARY KEY,
       agents_id INTEGER NOT NULL,
       c_name VARCHAR(40) NOT NULL,
       c_city CHAR(35) NOT NULL,
       FOREIGN KEY (agents_id) REFERENCES agents (id)
   );
   """
    db_file = "task2.db"

    conn = create_connection(db_file)


    if conn is not None:
        execute_sql(conn, create_agents_sql)
        execute_sql(conn, create_customers_sql)

        agent = (1, "Bond", "Orlean")
        agent2 = (2, "Borat", "Texas")
        # ag_id = add_agent(conn, agent)
        # a_id = add_agent(conn, agent2)
        update(conn, "customers", 2, c_city = "New York")

        customer = (1, "Mike", "Orlando")
        customer2 = (2, "Cris", "Texas")
        customer3 = (2, "Jake", "New York")
        # ct_id = add_customer(conn, customer)
        # c_id = add_customer(conn, customer2)
        # cs_id = add_customer(conn, customer3)
        delete_where(conn, "customers", id = 3)
        # print("Zaczynam:")
        # print(select_all(conn, "agents"))
        # print(select_all(conn, "customers"))
        # print("Kończę")
        # print(select_where(conn, "customers", c_city="Orlando"))
        # print(select_where(conn, "customers", c_city="New York"))
        # print(select_where(conn, "agents", a_name="Bond"))
        # cur = conn.execute("SELECT * FROM agents")
        # cur = conn.execute("SELECT * FROM customers")

        conn.close()


