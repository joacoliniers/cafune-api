# ⚙️ Cafuné API - Motor Backend y Base de Datos

Bienvenido al repositorio backend de **Cafuné**.

Desarrollé este servidor para dar el salto de una arquitectura local (offline) a un ecosistema cliente-servidor robusto. El objetivo principal fue centralizar la información, garantizar la persistencia de los datos en la nube y preparar el negocio para una futura escalabilidad.

---

## 💻 Detalles Técnicos y Stack

<details>
<summary><b>📐 Tecnologías Utilizadas (Clic para desplegar)</b></summary>

* **Lenguaje:** Python 3
* **Framework:** FastAPI.
* **Base de Datos:** PostgreSQL, alojada y gestionada a través de **Supabase**.
* **Validación y Serialización:** Pydantic.
* **Despliegue:** Render (Hosteado en la nube).
</details>

<details>
<summary><b>🐛 Desafíos Técnicos Superados (Clic para desplegar)</b></summary>

* **Gestión Estricta de Nulos (Null Safety):** Uno de los desafíos más interesantes fue modelar la API para aceptar información física de forma parcial (ej. cargar las medidas de un solo dedo por sesión). Flexibilicé los esquemas de entrada y salida utilizando tipado `Optional` en Pydantic, asegurando que los campos vacíos provenientes de Android se interpreten como `NULL` en PostgreSQL y no como ceros por defecto, previniendo la corrupción estadística de los datos.
* **Actualizaciones Parciales (PATCH/UPDATE):** Implementé lógica de actualización dinámica utilizando parámetros como `exclude_unset=True` en la carga útil de JSON, garantizando que las peticiones parciales desde el cliente no sobreescriban con valores vacíos la información histórica de la base de datos.
</details>

---

Para ver cómo se consumen estos servicios desde la interfaz de usuario, podés visitar el repositorio de la aplicación nativa:
👉 **[Repositorio del Frontend (Android + Java)](https://github.com/joacoliniers/CafuneNails12)**
