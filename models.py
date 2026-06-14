from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

class Clienta(Base):
    __tablename__ = "clientas"
    id_clienta = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    tipo_unia = Column(String)
    es_grasosa = Column(Boolean)
    notas = Column(String)

    medidas = relationship("MedidaSoftGel", back_populates="clienta", cascade="all, delete-orphan", uselist=False)
    sesiones = relationship("Sesion", back_populates="clienta", cascade="all, delete-orphan")

class MedidaSoftGel(Base):
    __tablename__ = "medidas"
    id_clienta = Column(Integer, ForeignKey("clientas.id_clienta", ondelete="CASCADE"), primary_key=True)
    izq_pulgar = Column(Integer)
    izq_indice = Column(Integer)
    izq_medio = Column(Integer)
    izq_anular = Column(Integer)
    izq_menique = Column(Integer)
    der_pulgar = Column(Integer)
    der_indice = Column(Integer)
    der_medio = Column(Integer)
    der_anular = Column(Integer)
    der_menique = Column(Integer)

    clienta = relationship("Clienta", back_populates="medidas")

class Sesion(Base):
    __tablename__ = "sesiones" 
    id_sesion = Column(Integer, primary_key=True, autoincrement=True)
    id_clienta = Column(Integer, ForeignKey("clientas.id_clienta", ondelete="CASCADE"))
    fecha_hora = Column(BigInteger) 
    duracion_minutos = Column(Integer)
    tipo_servicio = Column(String)
    monto_cobrado = Column(Float)
    material_remocion = Column(Boolean)
    notas = Column(String)
    estado = Column(String)

    clienta = relationship("Clienta", back_populates="sesiones")

