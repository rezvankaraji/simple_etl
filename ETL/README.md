Prerequisites
 install psycopg2

-------------------

create_library.py :
 Creates tables and triggers of the source database (based on the given data model and sql file)

create_warehouse.py :
 Creates tables of the warehouse database (based on the given data model and sql file)

etl.py :
 Contains ETL logic to transfer data from library to warehouse

-------------------

Before etl run:

 If a record is being deleted from table_name table, the values of that record with the date of deletion 
    will be inserted into corresponding deleted_table_name table
 If a record is being updated in table_name table, the values of that old version 
    with the date of update will be inserted into corresponding updated_table_name table

-------------------

Within etl run:

 update:
    Based on updated_at value, every record in updated_table_name will be extracted from library and their value with the date of transfer 
        will be inserted into similar table in warehouse
    Using the primary_key of the record, last version of each data will be extracted from library and placed in warehouse 
        (delete the old and insert the new)
    After commiting the insertion, the record will be deleted from updated_table_name in library.

 delete:
    Based on deleted_at value, every record in deleted_table_name will be extracted from library and their value with the date of transfer 
        will be inserted into similar table in warehouse
    Using the primary_key of the record, it will be removed from table_name in warehouse
    After commiting the changes in warehouse, the record will be deleted from deleted_table_name in library.

 insert:
    Based on created_at value, the new records will be extracted from library and their value with the date of transfer 
        will be inserted into similar table in warehouse

--------------------

After etl run:

    Records in main tables will be untouched.
    update and delete tables will be empty and are ready to log new changes

--------------------

Rezvan karaji - 9613021