from pydantic import BaseModel
from typing import Optional

# 1. Esquema de ENTRADA (Lo que manda el celular al crear)
class ClientaCreate(BaseModel):
    nombre: str
    tipo_unia: str
    es_grasosa: bool
    notas: Optional[str] = None  # Si no manda nada, por defecto es None (nulo)

# 2. Esquema de SALIDA (Lo que el servidor le responde al celular)
class ClientaResponse(BaseModel):
    id_clienta: int              # Acá SÍ incluimos el ID porque ya existe en la base
    nombre: str
    tipo_unia: str
    es_grasosa: bool
    notas: Optional[str] = None

    medidas: Optional[MedidaSoftGelResponse] = None

    # Configuración mágica para que Pydantic pueda leer directamente 
    # los objetos que le devuelve SQLAlchemy
    class Config:
        from_attributes = True

class ClientaUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo_unia: Optional[str] = None
    es_grasosa: Optional[bool] = None
    notas: Optional[str] = None



# 3. Esquema de ENTRADA (Lo que manda el celular al agendar un turno)
class SesionCreate(BaseModel):
    id_clienta: int
    fecha_hora: int           
    duracion_minutos: int
    tipo_servicio: str
    monto_cobrado: float
    material_para_remocion: bool 
    notas_sesion: Optional[str] = None 
    estado: str

# 4. Esquema de SALIDA (Lo que el servidor le responde al celular)
class SesionResponse(BaseModel):
    id_sesion: int            # El ID único del turno generado por la BD
    id_clienta: int
    fecha_hora: int
    duracion_minutos: int
    tipo_servicio: str
    monto_cobrado: float
    material_para_remocion: bool
    notas_sesion: Optional[str] = None
    estado: str

    class Config:
        from_attributes = True

class SesionUpdate(BaseModel):
    fecha_hora: Optional[int] = None
    duracion_minutos: Optional[int] = None
    tipo_servicio: Optional[str] = None
    monto_cobrado: Optional[float] = None
    material_para_remocion: Optional[bool] = None
    notas_sesion: Optional[str] = None
    estado: Optional[str] = None

# 5. Esquema de ENTRADA (Lo que manda la app para guardar medidas)
class MedidaSoftGelCreate(BaseModel):
    id_clienta: int
    izq_pulgar: int
    izq_indice: int
    izq_medio: int
    izq_anular: int
    izq_menique: int
    der_pulgar: int
    der_indice: int
    der_medio: int
    der_anular: int
    der_menique: int

# 6. Esquema de SALIDA (Lo que el servidor devuelve)
class MedidaSoftGelResponse(BaseModel):
    id_clienta: int
    izq_pulgar: int
    izq_indice: int
    izq_medio: int
    izq_anular: int
    izq_menique: int
    der_pulgar: int
    der_indice: int
    der_medio: int
    der_anular: int
    der_menique: int

    class Config:
        from_attributes = True

class MedidaSoftGelUpdate(BaseModel):  
    izq_pulgar: Optional[int] = None
    izq_indice: Optional[int] = None
    izq_medio: Optional[int] = None
    izq_anular: Optional[int] = None
    izq_menique: Optional[int] = None
    der_pulgar: Optional[int] = None
    der_indice: Optional[int] = None
    der_medio: Optional[int] = None
    der_anular: Optional[int] = None
    der_menique: Optional[int] = None