from pydantic import BaseModel
from typing import Optional

# 1. Esquema de ENTRADA
class ClientaCreate(BaseModel):
    nombre: str
    tipo_unia: str
    es_grasosa: bool
    notas: Optional[str] = None 

# 2. Esquema de SALIDA
class ClientaResponse(BaseModel):
    id_clienta: int             
    nombre: str
    tipo_unia: str
    es_grasosa: bool
    notas: Optional[str] = None

    medidas: Optional[MedidaSoftGelResponse] = None

    class Config:
        from_attributes = True

class ClientaUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo_unia: Optional[str] = None
    es_grasosa: Optional[bool] = None
    notas: Optional[str] = None



# 3. Esquema de ENTRADA
class SesionCreate(BaseModel):
    id_clienta: int
    fecha_hora: int           
    duracion_minutos: int
    tipo_servicio: str
    monto_cobrado: float
    material_remocion: bool
    notas: Optional[str] = None
    estado: str

# 4. Esquema de SALIDA
class SesionResponse(BaseModel):
    id_sesion: int           
    id_clienta: int
    fecha_hora: int
    duracion_minutos: int
    tipo_servicio: str
    monto_cobrado: float
    material_remocion: bool
    notas: Optional[str] = None
    estado: str

    class Config:
        from_attributes = True

class SesionUpdate(BaseModel):
    fecha_hora: Optional[int] = None
    duracion_minutos: Optional[int] = None
    tipo_servicio: Optional[str] = None
    monto_cobrado: Optional[float] = None
    material_remocion: Optional[bool] = None
    notas: Optional[str] = None
    estado: Optional[str] = None

# 5. Esquema de ENTRADA
class MedidaSoftGelCreate(BaseModel):
    id_clienta: int
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

# 6. Esquema de SALIDA
class MedidaSoftGelResponse(BaseModel):
    id_clienta: int
    
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