import psycopg2 as pg
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


try:
    conn = pg.connect(
        "host=127.0.0.1 dbname=library user=postgres password=postgres")
    cur = conn.cursor()
except:
	conn = pg.connect("host=127.0.0.1 user=postgres password=postgres")
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
	cur.execute(sql.SQL("CREATE DATABASE LIBRARY"))
	conn.commit()
	conn.close()
	conn = pg.connect(
        "host=127.0.0.1 dbname=library user=postgres password=postgres")
	cur = conn.cursor()

cur.execute("""
-- TABLES
CREATE TABLE IF NOT EXISTS BOOK (
    ISBN INT NOT NULL,
    Title VARCHAR(25) NOT NULL,
	Description VARCHAR(256) NOT NULL,
	Original_language VARCHAR(25) NOT NULL,
	Version_number INT NOT NULL,
	Release_date date NOT NULL,
	Publisher VARCHAR(25) NOT NULL,
	Amount INT NOT NULL,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (ISBN)
);

CREATE TABLE IF NOT EXISTS WRITER (
	Writer_id SERIAL,
	First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (Writer_id)
);

CREATE TABLE IF NOT EXISTS BOOK_WRITER (
	_id SERIAL,
	ISBN INT REFERENCES BOOK ON UPDATE CASCADE ON DELETE CASCADE,
	Writer_id INT REFERENCES WRITER ON UPDATE CASCADE ON DELETE CASCADE,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS BOOK_GENRE (
	_id SERIAL,
	ISBN INT REFERENCES BOOK ON UPDATE CASCADE ON DELETE CASCADE,
	Genre VARCHAR(25) NOT NULL,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS TRANSLATOR (
	Translator_id SERIAL,
	First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (Translator_id)
);

CREATE TABLE IF NOT EXISTS BOOK_translator (
	_id SERIAL,
	ISBN INT REFERENCES BOOK ON UPDATE CASCADE ON DELETE CASCADE,
	Translator_id INT REFERENCES TRANSLATOR ON UPDATE CASCADE ON DELETE CASCADE,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS MEMBERS (
    Member_id SERIAL,
    First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	Birth_date date NOT NULL,
	Registration_date date NOT NULL,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (Member_id)
);

CREATE TABLE IF NOT EXISTS ADDRESS (
	Zip_code INT NOT NULL,
	Country VARCHAR(25) NOT NULL,
	City VARCHAR(25) NOT NULL,
	Street VARCHAR(25) NOT NULL,
	House_number INT NOT NULL,
	Apt_number INT NOT NULL,
	Area_code INT NOT NULL,
	Phone_number INT NOT NULL,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (Zip_code)
);

CREATE TABLE IF NOT EXISTS MEMBERS_ADDRESS (
	_id SERIAL,
	Member_id INT REFERENCES MEMBERS ON UPDATE CASCADE ON DELETE CASCADE,
	Zip_code INT REFERENCES ADDRESS ON UPDATE CASCADE ON DELETE CASCADE,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS MEMBERS_PHONE (
	_id SERIAL,
	Member_id INT REFERENCES MEMBERS ON UPDATE CASCADE ON DELETE CASCADE,
	Mobile_code INT NOT NULL,
	Mobile_number INT NOT NULL,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS MEMBERS_BORROW (
	Borrow_id SERIAL,
	Member_id INT REFERENCES MEMBERS ON UPDATE CASCADE ON DELETE CASCADE,
	ISBN INT REFERENCES BOOK ON UPDATE CASCADE ON DELETE CASCADE,
	Expiration_date date NOT NULL,
	created_at DATE DEFAULT NOW(),
	PRIMARY KEY (Borrow_id)
);

-- DELETE TABLES
CREATE TABLE IF NOT EXISTS DELETED_BOOK (
    ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
    Title VARCHAR(25) NOT NULL,
	Description VARCHAR(256) NOT NULL,
	Original_language VARCHAR(25) NOT NULL,
	Version_number INT NOT NULL,
	Release_date date NOT NULL,
	Publisher VARCHAR(25) NOT NULL,
	Amount INT NOT NULL,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (ISBN)
);

CREATE TABLE IF NOT EXISTS DELETED_WRITER (
	Writer_id INT REFERENCES WRITER ON UPDATE NO ACTION ON DELETE NO ACTION,
	First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (Writer_id)
);

CREATE TABLE IF NOT EXISTS DELETED_BOOK_WRITER (
	_id INT REFERENCES BOOK_WRITER ON UPDATE NO ACTION ON DELETE NO ACTION,
	ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
	Writer_id INT REFERENCES WRITER ON UPDATE NO ACTION ON DELETE NO ACTION,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS DELETED_BOOK_GENRE (
	_id INT REFERENCES BOOK_GENRE ON UPDATE NO ACTION ON DELETE NO ACTION,
	ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
	Genre VARCHAR(25) NOT NULL,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS DELETED_TRANSLATOR (
	Translator_id INT REFERENCES TRANSLATOR ON UPDATE NO ACTION ON DELETE NO ACTION,
	First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (Translator_id)
);

CREATE TABLE IF NOT EXISTS DELETED_BOOK_translator (
	_id INT REFERENCES BOOK_translator ON UPDATE NO ACTION ON DELETE NO ACTION,
	ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
	Translator_id INT REFERENCES TRANSLATOR ON UPDATE NO ACTION ON DELETE NO ACTION,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS DELETED_MEMBERS (
    Member_id INT REFERENCES MEMBERS ON UPDATE NO ACTION ON DELETE NO ACTION,
    First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	Birth_date date NOT NULL,
	Registration_date date NOT NULL,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (Member_id)
);

CREATE TABLE IF NOT EXISTS DELETED_ADDRESS (
	Zip_code INT REFERENCES ADDRESS ON UPDATE NO ACTION ON DELETE NO ACTION,
	Country VARCHAR(25) NOT NULL,
	City VARCHAR(25) NOT NULL,
	Street VARCHAR(25) NOT NULL,
	House_number INT NOT NULL,
	Apt_number INT NOT NULL,
	Area_code INT NOT NULL,
	Phone_number INT NOT NULL,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (Zip_code)
);

CREATE TABLE IF NOT EXISTS DELETED_MEMBERS_ADDRESS (
	_id INT REFERENCES MEMBERS_ADDRESS ON UPDATE NO ACTION ON DELETE NO ACTION,
	Member_id INT REFERENCES MEMBERS ON UPDATE NO ACTION ON DELETE NO ACTION,
	Zip_code INT REFERENCES ADDRESS ON UPDATE NO ACTION ON DELETE NO ACTION,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS DELETED_MEMBERS_PHONE (
	_id INT REFERENCES MEMBERS_PHONE ON UPDATE NO ACTION ON DELETE NO ACTION,
	Member_id INT REFERENCES MEMBERS ON UPDATE NO ACTION ON DELETE NO ACTION,
	Mobile_code INT NOT NULL,
	Mobile_number INT NOT NULL,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS DELETED_MEMBERS_BORROW (
	Borrow_id INT REFERENCES MEMBERS_BORROW ON UPDATE NO ACTION ON DELETE NO ACTION,
	Member_id INT REFERENCES MEMBERS ON UPDATE NO ACTION ON DELETE NO ACTION,
	ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
	Expiration_date date NOT NULL,
	created_at DATE NOT NULL,
	deleted_at DATE DEFAULT NOW(),
	PRIMARY KEY (Borrow_id)
);

-- UPDATE TABLES
CREATE TABLE IF NOT EXISTS UPDATED_BOOK (
    ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
    Title VARCHAR(25) NOT NULL,
	Description VARCHAR(256) NOT NULL,
	Original_language VARCHAR(25) NOT NULL,
	Version_number INT NOT NULL,
	Release_date date NOT NULL,
	Publisher VARCHAR(25) NOT NULL,
	Amount INT NOT NULL,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (ISBN, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_WRITER (
	Writer_id INT REFERENCES WRITER ON UPDATE NO ACTION ON DELETE NO ACTION,
	First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (Writer_id, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_BOOK_WRITER (
	_id INT REFERENCES BOOK_WRITER ON UPDATE NO ACTION ON DELETE NO ACTION,
	ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
	Writer_id INT REFERENCES WRITER ON UPDATE NO ACTION ON DELETE NO ACTION,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (_id, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_BOOK_GENRE (
	_id INT REFERENCES BOOK_GENRE ON UPDATE NO ACTION ON DELETE NO ACTION,
	ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
	Genre VARCHAR(25) NOT NULL,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (_id, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_TRANSLATOR (
	Translator_id INT REFERENCES TRANSLATOR ON UPDATE NO ACTION ON DELETE NO ACTION,
	First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (Translator_id, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_BOOK_translator (
	_id INT REFERENCES BOOK_translator ON UPDATE NO ACTION ON DELETE NO ACTION,
	ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
	Translator_id INT REFERENCES TRANSLATOR ON UPDATE NO ACTION ON DELETE NO ACTION,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (_id, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_MEMBERS (
    Member_id INT REFERENCES MEMBERS ON UPDATE NO ACTION ON DELETE NO ACTION,
    First_name VARCHAR(25) NOT NULL,
	Mid_name VARCHAR(25),
	Last_name VARCHAR(25) NOT NULL,
	Birth_date date NOT NULL,
	Registration_date date NOT NULL,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (Member_id, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_ADDRESS (
	Zip_code INT REFERENCES ADDRESS ON UPDATE NO ACTION ON DELETE NO ACTION,
	Country VARCHAR(25) NOT NULL,
	City VARCHAR(25) NOT NULL,
	Street VARCHAR(25) NOT NULL,
	House_number INT NOT NULL,
	Apt_number INT NOT NULL,
	Area_code INT NOT NULL,
	Phone_number INT NOT NULL,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (Zip_code, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_MEMBERS_ADDRESS (
	_id INT REFERENCES MEMBERS_ADDRESS ON UPDATE NO ACTION ON DELETE NO ACTION,
	Member_id INT REFERENCES MEMBERS ON UPDATE NO ACTION ON DELETE NO ACTION,
	Zip_code INT REFERENCES ADDRESS ON UPDATE NO ACTION ON DELETE NO ACTION,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (_id, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_MEMBERS_PHONE (
	_id INT REFERENCES MEMBERS_PHONE ON UPDATE NO ACTION ON DELETE NO ACTION,
	Member_id INT REFERENCES MEMBERS ON UPDATE NO ACTION ON DELETE NO ACTION,
	Mobile_code INT NOT NULL,
	Mobile_number INT NOT NULL,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (_id, updated_at)
);

CREATE TABLE IF NOT EXISTS UPDATED_MEMBERS_BORROW (
	Borrow_id INT REFERENCES MEMBERS_BORROW ON UPDATE NO ACTION ON DELETE NO ACTION,
	Member_id INT REFERENCES MEMBERS ON UPDATE NO ACTION ON DELETE NO ACTION,
	ISBN INT REFERENCES BOOK ON UPDATE NO ACTION ON DELETE NO ACTION,
	Expiration_date date NOT NULL,
	created_at DATE NOT NULL,
	updated_at DATE DEFAULT NOW(), 
	PRIMARY KEY (Borrow_id, updated_at)
);

-- UPDATE TRIGGERS
CREATE OR REPLACE FUNCTION BOOK_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_BOOK(ISBN, Title, Description, Original_language,
            Version_number, Release_date, Publisher, Amount, created_at) 
		VALUES(old.ISBN, old.Title, old.Description, old.Original_language,
            old.Version_number, old.Release_date, old.Publisher, old.Amount, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER BOOK_update_time
	BEFORE update 
	ON BOOK
	FOR EACH ROW
	EXECUTE PROCEDURE BOOK_update_time();

CREATE OR REPLACE FUNCTION WRITER_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_WRITER(Writer_id, First_name, Mid_name, Last_name, created_at) 
		VALUES(old.Writer_id, old.First_name, old.Mid_name, old.Last_name, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER WRITER_update_time
	BEFORE update 
	ON WRITER
	FOR EACH ROW
	EXECUTE PROCEDURE WRITER_update_time();
	
CREATE OR REPLACE FUNCTION BOOK_WRITER_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_BOOK_WRITER(_id, Writer_id, ISBN, created_at) 
		VALUES(old._id, old.Writer_id, old.ISBN, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER BOOK_WRITER_update_time
	BEFORE update 
	ON BOOK_WRITER
	FOR EACH ROW
	EXECUTE PROCEDURE BOOK_WRITER_update_time();
	
CREATE OR REPLACE FUNCTION BOOK_GENRE_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_BOOK_GENRE(_id, Genre, ISBN, created_at) 
		VALUES(old._id, old.Genre, old.ISBN, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER BOOK_GENRE_update_time
	BEFORE update 
	ON BOOK_GENRE
	FOR EACH ROW
	EXECUTE PROCEDURE BOOK_GENRE_update_time();
	
CREATE OR REPLACE FUNCTION TRANSLATOR_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_TRANSLATOR(Translator_id, First_name, Mid_name, Last_name, created_at) 
		VALUES(old.Translator_id, old.First_name, old.Mid_name, old.Last_name, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER TRANSLATOR_update_time
	BEFORE update 
	ON TRANSLATOR
	FOR EACH ROW
	EXECUTE PROCEDURE TRANSLATOR_update_time();
	
CREATE OR REPLACE FUNCTION BOOK_TRANSLATOR_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_BOOK_TRANSLATOR(_id, Translator_id, ISBN, created_at) 
		VALUES(old._id, old.Translator_id, old.ISBN, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER BOOK_TRANSLATOR_update_time
	BEFORE update 
	ON BOOK_TRANSLATOR
	FOR EACH ROW
	EXECUTE PROCEDURE BOOK_TRANSLATOR_update_time();
	
CREATE OR REPLACE FUNCTION MEMBERS_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_MEMBERS(Member_id, First_name, Mid_name, Last_name,
            Birth_date, Registration_date, created_at) 
		VALUES(old.Member_id, old.First_name, old.Mid_name, old.Last_name,
            old.Birth_date, old.Registration_date, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER MEMBERS_update_time
	BEFORE update 
	ON MEMBERS
	FOR EACH ROW
	EXECUTE PROCEDURE MEMBERS_update_time();
	
CREATE OR REPLACE FUNCTION ADDRESS_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_ADDRESS(Zip_code, Country, City, Street, House_number,
			Apt_number, Area_code, Phone_number, created_at) 
		VALUES(old.Zip_code, old.Country, old.City, old.Street, old.House_number,
			old.Apt_number, old.Area_code, old.Phone_number, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER ADDRESS_update_time
	BEFORE update 
	ON ADDRESS
	FOR EACH ROW
	EXECUTE PROCEDURE ADDRESS_update_time();
	
CREATE OR REPLACE FUNCTION MEMBERS_ADDRESS_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_MEMBERS_ADDRESS(_id, Member_id, Zip_code, created_at) 
		VALUES(old._id, old.Member_id, old.Zip_code, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER MEMBERS_ADDRESS_update_time
	BEFORE update 
	ON MEMBERS_ADDRESS
	FOR EACH ROW
	EXECUTE PROCEDURE MEMBERS_ADDRESS_update_time();
	
CREATE OR REPLACE FUNCTION MEMBERS_PHONE_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_MEMBERS_PHONE(_id, Member_id, mobile_code, mobile_number, created_at) 
		VALUES(old._id, old.Member_id, old.mobile_code, old.mobile_number, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER MEMBERS_PHONE_update_time
	BEFORE update 
	ON MEMBERS_PHONE
	FOR EACH ROW
	EXECUTE PROCEDURE MEMBERS_PHONE_update_time();
	
CREATE OR REPLACE FUNCTION MEMBERS_BORROW_update_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO updateD_MEMBERS_BORROW(borrow_id, Member_id, ISBN, Expiration_date, created_at) 
		VALUES(old.borrow_id, old.Member_id, old.ISBN, old.Expiration_date, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER MEMBERS_BORROW_update_time
	BEFORE update 
	ON MEMBERS_BORROW
	FOR EACH ROW
	EXECUTE PROCEDURE MEMBERS_BORROW_update_time();

-- DELETE TRIGGERS
CREATE OR REPLACE FUNCTION BOOK_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_BOOK(ISBN, Title, Description, Original_language,
            Version_number, Release_date, Publisher, Amount, created_at) 
		VALUES(old.ISBN, old.Title, old.Description, old.Original_language,
            old.Version_number, old.Release_date, old.Publisher, old.Amount, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER BOOK_delete_time
	BEFORE DELETE 
	ON BOOK
	FOR EACH ROW
	EXECUTE PROCEDURE BOOK_delete_time();

CREATE OR REPLACE FUNCTION WRITER_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_WRITER(Writer_id, First_name, Mid_name, Last_name, created_at) 
		VALUES(old.Writer_id, old.First_name, old.Mid_name, old.Last_name, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER WRITER_delete_time
	BEFORE DELETE 
	ON WRITER
	FOR EACH ROW
	EXECUTE PROCEDURE WRITER_delete_time();
	
CREATE OR REPLACE FUNCTION BOOK_WRITER_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_BOOK_WRITER(_id, Writer_id, ISBN, created_at) 
		VALUES(old._id, old.Writer_id, old.ISBN, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER BOOK_WRITER_delete_time
	BEFORE DELETE 
	ON BOOK_WRITER
	FOR EACH ROW
	EXECUTE PROCEDURE BOOK_WRITER_delete_time();
	
CREATE OR REPLACE FUNCTION BOOK_GENRE_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_BOOK_GENRE(_id, Genre, ISBN, created_at) 
		VALUES(old._id, old.Genre, old.ISBN, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER BOOK_GENRE_delete_time
	BEFORE DELETE 
	ON BOOK_GENRE
	FOR EACH ROW
	EXECUTE PROCEDURE BOOK_GENRE_delete_time();
	
CREATE OR REPLACE FUNCTION TRANSLATOR_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_TRANSLATOR(Translator_id, First_name, Mid_name, Last_name, created_at) 
		VALUES(old.Translator_id, old.First_name, old.Mid_name, old.Last_name, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER TRANSLATOR_delete_time
	BEFORE DELETE 
	ON TRANSLATOR
	FOR EACH ROW
	EXECUTE PROCEDURE TRANSLATOR_delete_time();
	
CREATE OR REPLACE FUNCTION BOOK_TRANSLATOR_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_BOOK_TRANSLATOR(_id, Translator_id, ISBN, created_at) 
		VALUES(old._id, old.Translator_id, old.ISBN, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER BOOK_TRANSLATOR_delete_time
	BEFORE DELETE 
	ON BOOK_TRANSLATOR
	FOR EACH ROW
	EXECUTE PROCEDURE BOOK_TRANSLATOR_delete_time();
	
CREATE OR REPLACE FUNCTION MEMBERS_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_MEMBERS(Member_id, First_name, Mid_name, Last_name,
            Birth_date, Registration_date, created_at) 
		VALUES(old.Member_id, old.First_name, old.Mid_name, old.Last_name,
            old.Birth_date, old.Registration_date, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER MEMBERS_delete_time
	BEFORE DELETE 
	ON MEMBERS
	FOR EACH ROW
	EXECUTE PROCEDURE MEMBERS_delete_time();
	
CREATE OR REPLACE FUNCTION ADDRESS_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_ADDRESS(Zip_code, Country, City, Street, House_number,
			Apt_number, Area_code, Phone_number, created_at) 
		VALUES(old.Zip_code, old.Country, old.City, old.Street, old.House_number,
			old.Apt_number, old.Area_code, old.Phone_number, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER ADDRESS_delete_time
	BEFORE DELETE 
	ON ADDRESS
	FOR EACH ROW
	EXECUTE PROCEDURE ADDRESS_delete_time();
	
CREATE OR REPLACE FUNCTION MEMBERS_ADDRESS_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_MEMBERS_ADDRESS(_id, Member_id, Zip_code, created_at) 
		VALUES(old._id, old.Member_id, old.Zip_code, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER MEMBERS_ADDRESS_delete_time
	BEFORE DELETE 
	ON MEMBERS_ADDRESS
	FOR EACH ROW
	EXECUTE PROCEDURE MEMBERS_ADDRESS_delete_time();
	
CREATE OR REPLACE FUNCTION MEMBERS_PHONE_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_MEMBERS_PHONE(_id, Member_id, mobile_code, mobile_number, created_at) 
		VALUES(old._id, old.Member_id, old.mobile_code, old.mobile_number, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER MEMBERS_PHONE_delete_time
	BEFORE DELETE 
	ON MEMBERS_PHONE
	FOR EACH ROW
	EXECUTE PROCEDURE MEMBERS_PHONE_delete_time();
	
CREATE OR REPLACE FUNCTION MEMBERS_BORROW_delete_time()
	RETURNS TRIGGER AS
 $$
	BEGIN
		INSERT INTO DELETED_MEMBERS_BORROW(borrow_id, Member_id, ISBN, Expiration_date, created_at) 
		VALUES(old.borrow_id, old.Member_id, old.ISBN, old.Expiration_date, old.created_at);
		RETURN NULL;
	END
 $$
 LANGUAGE 'plpgsql';

CREATE TRIGGER MEMBERS_BORROW_delete_time
	BEFORE DELETE 
	ON MEMBERS_BORROW
	FOR EACH ROW
	EXECUTE PROCEDURE MEMBERS_BORROW_delete_time();
""")

conn.commit()
conn.close()
