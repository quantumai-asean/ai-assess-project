import psycopg
import toml

class DB_INIT_ENGINE:
    def __init__(self, confs = "../configs.toml"):
        confs = toml.load(confs) 
        self.host = confs['database']['server']['host']
        self.port = confs['database']['server']['port']
        self.user = confs['database']['server']['user']
        self.db = confs['database']['server']['dbname']
        self.pw = confs['database']['server']['password']
    
    def create_usertable(self):
        try:
            with psycopg.connect(f"host={self.host} port={self.port} dbname={self.db} user={self.user} password={self.pw}") as conn:
                with conn.cursor() as cur:
                    # use extension to create UUID on insert
                    create_ownertable_str = """CREATE TABLE userlogin (                                                     
                                name varchar(50) NOT NULL CHECK (name <> '') UNIQUE,
                                email varchar(50) NOT NULL CHECK (email <> '' AND email = lower(email)) UNIQUE,
                                id SERIAL PRIMARY KEY,
                                password varchar(64) NOT NULL,
                                country varchar(3) NOT NULL,
                                url varchar(50)
                            )"""
                    cur.execute(create_ownertable_str)
                    add_uniq_constraint_str = "CREATE UNIQUE INDEX owner_name_uniqueness ON userlogin (LOWER(name))"
                    cur.execute(add_uniq_constraint_str)


                    # Make the changes to the database persistent
                conn.commit()
        except Exception as e:
            print(e)
            pass

    def create_modelcardtable(self):
        try:
            with psycopg.connect(f"host={self.host} port={self.port} dbname={self.db} user={self.user} password={self.pw}") as conn:
                with conn.cursor() as cur:
                    # use extension to create UUID on insert
                    create_ownertable_str = """CREATE TABLE modelcard (                                                     
                                name varchar(30) NOT NULL CHECK (name <> ''),
                                version varchar(30) NOT NULL CHECK (name <> ''),
                                email varchar(50) NOT NULL CHECK (email <> '' AND email = lower(email)),
                                id SERIAL PRIMARY KEY,
                                modelcard_data jsonb,
                                comments varchar(80),
                                generated_at timestamptz DEFAULT current_timestamp
                            )"""
                    cur.execute(create_ownertable_str)

                    # Make the changes to the database persistent
                conn.commit()
        except Exception as e:
            print(e)
            pass

