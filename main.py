import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models, schemas

# Cargamos las variables
load_dotenv()

# Leemos la llave desde el archivo .env
API_KEY = os.getenv("API_KEY") 
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def validar_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Te falta el pase VIP (API Key).",
        )
    return api_key

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

# Al agregar 'dependencies', TODAS las rutas quedan bloqueadas automáticamente
app = FastAPI(
    title="API de Cafuné", 
    dependencies=[Depends(validar_api_key)]
)

# ==========================================
# DEPENDENCIA: Manejador de la base de datos
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db # Entrega la conexión temporal
    finally:
        db.close() # La cierra automáticamente al terminar

# ==========================================
# ENDPOINTS: CLIENTAS
# ==========================================

@app.post("/clientas/", response_model=schemas.ClientaResponse)
def crear_clienta(clienta: schemas.ClientaCreate, db: Session = Depends(get_db)):
    # 1. Transformamos el JSON de Pydantic a un objeto de SQLAlchemy
    # El **clienta.model_dump() es un atajo para no escribir nombre=clienta.nombre, etc.
    nueva_clienta = models.Clienta(**clienta.model_dump())
    
    # 2. Lo agregamos a la base de datos
    db.add(nueva_clienta)
    db.commit() # Confirmamos el guardado
    db.refresh(nueva_clienta) # Recargamos para obtener el ID autogenerado
    
    # 3. Devolvemos la clienta creada
    return nueva_clienta

# GET: Obtener todas las clientas (Para llenar el Autocomplete)
@app.get("/clientas/", response_model=list[schemas.ClientaResponse])
def obtener_todas_las_clientas(db: Session = Depends(get_db)):
    return db.query(models.Clienta).all()

# GET: Obtener una clienta específica por ID (Para el Perfil)
@app.get("/clientas/{id_clienta}", response_model=schemas.ClientaResponse)
def obtener_clienta(id_clienta: int, db: Session = Depends(get_db)):
    clienta = db.query(models.Clienta).filter(models.Clienta.id_clienta == id_clienta).first()
    if not clienta:
        raise HTTPException(status_code=404, detail="Clienta no encontrada")
    return clienta

# PUT: Actualizar datos de una clienta
@app.put("/clientas/{id_clienta}", response_model=schemas.ClientaResponse)
def actualizar_clienta(id_clienta: int, clienta_actualizada: schemas.ClientaUpdate, db: Session = Depends(get_db)):
    clienta_db = db.query(models.Clienta).filter(models.Clienta.id_clienta == id_clienta).first()
    if not clienta_db:
        raise HTTPException(status_code=404, detail="Clienta no encontrada")
    
    datos_nuevos = clienta_actualizada.model_dump(exclude_unset=True)
    for clave, valor in datos_nuevos.items():
        setattr(clienta_db, clave, valor)
        
    db.commit()
    db.refresh(clienta_db)
    return clienta_db

# DELETE: Borrar una clienta (y en cascada sus medidas y turnos)
@app.delete("/clientas/{id_clienta}")
def borrar_clienta(id_clienta: int, db: Session = Depends(get_db)):
    clienta_db = db.query(models.Clienta).filter(models.Clienta.id_clienta == id_clienta).first()
    if not clienta_db:
        raise HTTPException(status_code=404, detail="Clienta no encontrada")
    
    db.delete(clienta_db)
    db.commit()
    return {"mensaje": "Clienta eliminada con éxito"}

# ==========================================
# ENDPOINTS: SESIONES
# ==========================================

# POST: Agendar un nuevo turno
@app.post("/sesiones/", response_model=schemas.SesionResponse)
def crear_sesion(sesion: schemas.SesionCreate, db: Session = Depends(get_db)):
    # Validamos que la clienta exista antes de asignarle un turno
    clienta = db.query(models.Clienta).filter(models.Clienta.id_clienta == sesion.id_clienta).first()
    if not clienta:
        raise HTTPException(status_code=404, detail="No se puede agendar: La clienta no existe")

    nueva_sesion = models.Sesion(**sesion.model_dump())
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    return nueva_sesion

# GET: Obtener turnos (Con filtro opcional de fechas en milisegundos)
@app.get("/sesiones/", response_model=list[schemas.SesionResponse])
def obtener_sesiones(inicio: int = None, fin: int = None, db: Session = Depends(get_db)):
    consulta = db.query(models.Sesion)
    
    # Si Android manda el inicioDelDia y finDelDia, filtramos la base de datos
    if inicio is not None and fin is not None:
        consulta = consulta.filter(models.Sesion.fecha_hora >= inicio, models.Sesion.fecha_hora <= fin)
    
    # Ordenamos por hora para que el calendario los muestre prolijos
    return consulta.order_by(models.Sesion.fecha_hora.asc()).all()

# DELETE: Cancelar/Borrar un turno
@app.delete("/sesiones/{id_sesion}")
def borrar_sesion(id_sesion: int, db: Session = Depends(get_db)):
    sesion_db = db.query(models.Sesion).filter(models.Sesion.id_sesion == id_sesion).first()
    if not sesion_db:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    db.delete(sesion_db)
    db.commit()
    return {"mensaje": "Turno eliminado con éxito"}

@app.put("/sesiones/{id_sesion}", response_model=schemas.SesionResponse)
def actualizar_sesion(id_sesion: int, sesion_actualizada: schemas.SesionUpdate, db: Session = Depends(get_db)):
    
    # 1. Buscamos el turno viejo en la base de datos
    sesion_db = db.query(models.Sesion).filter(models.Sesion.id_sesion == id_sesion).first()
    
    # 2. Control de errores: Si mandan un ID que no existe, cortamos todo y devolvemos 404
    if not sesion_db:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    # 3. Extraemos SOLO los datos que el celular efectivamente mandó
    # El 'exclude_unset=True' es mágico: ignora todo lo que sea nulo en el esquema
    datos_nuevos = sesion_actualizada.model_dump(exclude_unset=True)
    
    # 4. Actualizamos el objeto de la base de datos campo por campo
    for clave, valor in datos_nuevos.items():
        setattr(sesion_db, clave, valor)
        
    # 5. Confirmamos el guardado
    db.commit()
    db.refresh(sesion_db)
    
    return sesion_db
# ==========================================
# ENDPOINTS: MEDIDAS SOFT GEL
# ==========================================

# POST: Cargar las medidas por primera vez
@app.post("/medidas/", response_model=schemas.MedidaSoftGelResponse)
def crear_medidas(medida: schemas.MedidaSoftGelCreate, db: Session = Depends(get_db)):
    # Verificamos si ya tiene medidas cargadas para no duplicar (Relación 1 a 1)
    medida_existente = db.query(models.MedidaSoftGel).filter(models.MedidaSoftGel.id_clienta == medida.id_clienta).first()
    if medida_existente:
        raise HTTPException(status_code=400, detail="Esta clienta ya tiene medidas. Usá PUT para actualizarlas.")

    nueva_medida = models.MedidaSoftGel(**medida.model_dump())
    db.add(nueva_medida)
    db.commit()
    db.refresh(nueva_medida)
    return nueva_medida

# PUT: Actualizar las medidas de una clienta
@app.put("/medidas/{id_clienta}", response_model=schemas.MedidaSoftGelResponse)
def actualizar_medidas(id_clienta: int, medida_actualizada: schemas.MedidaSoftGelUpdate, db: Session = Depends(get_db)):
    medida_db = db.query(models.MedidaSoftGel).filter(models.MedidaSoftGel.id_clienta == id_clienta).first()
    if not medida_db:
        raise HTTPException(status_code=404, detail="Medidas no encontradas para esta clienta")
    
    datos_nuevos = medida_actualizada.model_dump(exclude_unset=True)
    for clave, valor in datos_nuevos.items():
        setattr(medida_db, clave, valor)
        
    db.commit()
    db.refresh(medida_db)
    return medida_db

