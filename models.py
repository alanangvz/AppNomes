import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

nome_db = 'database.db'


#ALCHEMY
db_url = f"sqlite:///{nome_db}"
engine = create_engine(db_url)
Base = declarative_base()

class Pessoas(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)

Base.metadata.create_all(engine)

def db_filtro_alchemy():
    Session = sessionmaker(bind=engine)
    session = Session()
    response = session.query(Pessoas).all()
    session.close()
    return response

#SQLITE
def db_execute(query, params=[]):
    con = sqlite3.connect(nome_db)
    cursor = con.cursor()
    cursor.execute(query, params)
    con.commit()
    con.close()

def db_filtro_sqlite(query, params=[]):
    con = sqlite3.connect(nome_db)
    cursor = con.cursor()
    cursor.execute(query, params)
    response = cursor.fetchall()
    con.close()
    return response



