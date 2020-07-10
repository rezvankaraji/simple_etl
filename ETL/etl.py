import psycopg2 as pg
import datetime

#connect to databases
src_conn = pg.connect(
    "host=127.0.0.1 dbname=library user=postgres password=postgres")
dst_conn = pg.connect(
    "host=127.0.0.1 dbname=warehouse user=postgres password=postgres")
src_cur = src_conn.cursor()
dst_cur = dst_conn.cursor()

#get source database tables and their primery keys
src_cur.execute("""
    SELECT c.table_name, c.column_name
    FROM information_schema.table_constraints tc 
        JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
        JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
        AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
    WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = c.table_name
    ORDER BY c.table_name, c.ordinal_position ASC
    """)

src_tables = src_cur.fetchall()
# for x in src_tables : x[0] = table_name  x[1] = primary_key

names = []
tables = []
for x in src_tables:
    if not x[0] in names:
        tables.append(x)
        names.append(x[0])

#refactor record
def refactor(record):
    
    for y in record:
        if y is None:
            i = record.index(y)
            record = list(record)
            record[i] = ''
            record = tuple(record)
        if isinstance(y, datetime.date):
            i = record.index(y)
            record = list(record)
            record[i] = '%s' % (str(y))
            record = tuple(record)
    
    return record
    
for table in tables:
    # table := (table_name, primary_key)
 
    table_name = table[0]
    primary_key = table[1]

    #update old records
    if table_name[0:7] == "updated" :
        src_cur.execute("SELECT * FROM %s" % (table_name))
        src_query = src_cur.fetchall()

        updated = []
        for record in src_query:

            record = refactor(record)

            if not record[0] in updated:
                dst_cur.execute("DELETE FROM %s WHERE %s = %s ;" % (table_name[8:], primary_key, record[0]))
                src_cur.execute("SELECT * FROM %s WHERE %s = %s " % (table_name[8:], primary_key, record[0]))
                query = src_cur.fetchall()
                refactor(query)

                dst_cur.execute("INSERT INTO %s VALUES %s;" % (table_name[8:], query))
                updated.append(record[0])

            dst_cur.execute("INSERT INTO %s VALUES %s;" % (table_name, record))
            dst_conn.commit()

            #delete the record from source database
            src_cur.execute("DELETE FROM %s WHERE %s = %s ;" % (table_name, primary_key, record[0]))
            src_conn.commit()
            
    #delete records
    elif table_name[0:7] == "deleted":
        src_cur.execute("SELECT * FROM %s" % (table_name))
        src_query = src_cur.fetchall()

        for record in src_query:

            record = refactor(record)

            dst_cur.execute("DELETE FROM %s WHERE %s = %s ;" % (table_name[8:], primary_key, record[0]))
            dst_cur.execute("INSERT INTO %s VALUES %s;" % (table_name, record))
            dst_conn.commit()

            #delete the record from source database
            src_cur.execute("DELETE FROM %s WHERE %s = %s ;" % (table_name, primary_key, record[0]))
            src_conn.commit()
        
    #insert new records
    else :
        dst_cur.execute("SELECT MAX(transfered_at) FROM %s" % (table_name))
        last_transfer = dst_cur.fetchone()
        last_transfer = str(last_transfer[0])
        if last_transfer == 'None':
            last_transfer = str(datetime.datetime.now())

        src_cur.execute("SELECT * FROM %s WHERE created_at > '%s' " % (table_name, last_transfer))
        src_query = src_cur.fetchall()

        for record in src_query:

            record = refactor(record)

            dst_cur.execute("INSERT INTO %s VALUES %s;" % (table_name, record))
            dst_conn.commit()


#close connections
dst_conn.close()
src_conn.close()
