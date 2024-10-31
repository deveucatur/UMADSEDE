from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

engine = create_engine('sqlite:///adolescentes.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
from database import Base

class Pessoa(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    data_nascimento = Column(Date)
    telefone = Column(String)
    batizado_aguas = Column(Boolean)
    batizado_espirito = Column(Boolean)
    status = Column(String)
    tipo = Column(String)  # 'Jovem' ou 'Adolescente'
    observacao = Column(Text)


class Evento(Base):
    __tablename__ = 'eventos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    data = Column(Date)
    encerrado = Column(Boolean, default=False)
    tipo = Column(String)  # 'Jovens', 'Adolescentes' ou 'Ambos'
    
class Visitante(Base):
    __tablename__ = 'visitantes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    telefone = Column(String)
    convidado_por = Column(Integer, ForeignKey('pessoas.id'))
    evento_id = Column(Integer, ForeignKey('eventos.id'))

    convidado = relationship('Pessoa', foreign_keys=[convidado_por])
    evento = relationship('Evento')


class Presenca(Base):
    __tablename__ = 'presencas'
    id = Column(Integer, primary_key=True)
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
    evento_id = Column(Integer, ForeignKey('eventos.id'))
    presente = Column(Boolean)

    pessoa = relationship('Pessoa')
    evento = relationship('Evento')

Base.metadata.create_all(engine)
