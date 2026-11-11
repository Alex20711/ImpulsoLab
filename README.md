# ImpulsoLab · Disparo, retroceso e impactos en Python

**Laboratorio educativo interactivo de mecánica clásica unidimensional**. Permite investigar el lanzamiento idealizado de un proyectil por un arma de fuego y su posterior interacción con una barrera fija o un blanco móvil, utilizando **momento lineal, impulso, fuerza promedio, energía cinética, conservación del momento y coeficiente de restitución**.

![Cabecera del laboratorio](assets/banner.svg)

Incluye **consola modular**, **interfaz web en Streamlit**, **gráficos interactivos y reproducibles en Plotly**, **historial por estudiante**, **pruebas automáticas** y **ejemplos listos para ejecutar**. Está pensado para una demostración académica; no calcula rendimiento real de armas ni perforación.

## Publicar GRATIS con **solo GitHub** (recomendado)

Esta edición ahora incorpora **`docs/`**, una versión web autónoma de ImpulsoLab que funciona con **HTML, CSS y JavaScript** en GitHub Pages. Conserva también **la implementación académica en Python** (consola, motor físico y la alternativa Streamlit) en el mismo repositorio. GitHub Pages **no ejecuta Python en el servidor**: la versión en línea recalcula las mismas ecuaciones mediante JavaScript directamente en el navegador.

1. **Descomprime** `ImpulsoLab_Proyecto_Completo_GitHub_Pages.zip` y abre la carpeta `ImpulsoLab`.
2. Entra a [github.com/new](https://github.com/new), escribe **`ImpulsoLab`** como nombre del repositorio, selecciona **Public** y crea el repositorio. Puedes dejar desmarcada la creación de README, ya que el proyecto lo incluye.
3. Dentro del repositorio, pulsa **Add file → Upload files** y **sube el CONTENIDO de la carpeta `ImpulsoLab`**, no el ZIP ni una carpeta contenedora adicional. Los archivos `README.md`, `main.py`, `app.py` y la carpeta `docs` deben aparecer en la **raíz del repositorio**. Pulsa **Commit changes**.
4. Ve a **Settings → Pages → Build and deployment → Source → Deploy from a branch**.
5. Escoge **`main`** y **`/docs`** y pulsa **Save**.
6. Cuando termine la publicación, el enlace será similar a **`https://TU_USUARIO.github.io/ImpulsoLab/`**. También podrás encontrarlo en **Settings → Pages → Visit site**.

**Funciona sin servicios externos ni instalar Python:** selección de tres escenarios, validación, cálculos, animación SVG, explicaciones, historial por identificación y exportación JSON. El historial de GitHub Pages se guarda **solo en el almacenamiento local del navegador** (no se comparte entre dispositivos). Si necesitas un historial centralizado y sincronizado necesitarás un backend externo: GitHub Pages solo ofrece alojamiento estático.

**Prueba de la versión web:** `node --test docs/tests/physics.test.cjs` (Node.js 18+). Si no tienes Node.js, abre directamente el sitio publicado, introduce valores y presiona «Simular experimento».

---

## 1. Ejecutar en tu computador

**Requisitos:** Python 3.10 o posterior, pip y navegador web moderno. Se recomienda un entorno virtual.

```bash
# Entrar a la carpeta del proyecto descargada y descomprimida.
cd ImpulsoLab

# Crear entorno virtual
python -m venv .venv

# Activarlo en Windows (PowerShell):
.venv\Scripts\Activate.ps1

# O activarlo en macOS / Linux:
source .venv/bin/activate

# Instalar bibliotecas
python -m pip install -r requirements.txt
```

Para ejecutar la **consola**:

```bash
python main.py
```

Se solicitarán identificación del estudiante y escenario. Después de una simulación se mostrará el informe completo y se guardará una **visualización HTML animada** en `salidas/figuras/`, que puede abrirse sin Internet. El menú permite volver a simular, cambiar de escenario o consultar registros sin reiniciar el proceso.

Para iniciar la **interfaz web** en tu computador:

```bash
python -m streamlit run app.py
```

Streamlit mostrará una dirección local como `http://localhost:8501`, que se abre en el navegador. La interfaz incluye selección de escenarios, parámetros, gráficas, resultados por cuerpo, justificaciones y pestaña de historial.

## 2. Alternativa: publicar la aplicación Python con Streamlit (opcional)

> **Este apartado NO hace falta para publicar exclusivamente en GitHub Pages.** GitHub Pages sirve la versión estática `docs/`; si quieres ejecutar el código original de la **interfaz Streamlit de Python**, sí necesitarás un servicio compatible con Python como Streamlit Community Cloud.

1. Crea en GitHub un repositorio nuevo, por ejemplo `impulso-lab`, y sube **el contenido de esta carpeta**. Asegúrate de que `app.py`, `requirements.txt`, `physicslab/` y `assets/` queden en la raíz.
2. Entra a **[share.streamlit.io](https://share.streamlit.io/)**, inicia sesión y escoge crear o desplegar una nueva aplicación desde GitHub.
3. Selecciona el repositorio, la rama `main` y escribe `app.py` como archivo de entrada.
4. Despliega la aplicación. Streamlit instalará las dependencias de `requirements.txt` y proporcionará una dirección pública.
5. Si quieres historial permanente en Internet, realiza también el apartado **3. Historial persistente** antes de publicar el proyecto definitivamente.

Si haces cambios en el repositorio, el hosting puede actualizar el despliegue. El archivo `.github/workflows/tests.yml` ejecuta pruebas automáticas en pushes y pull requests.

### Comandos opcionales para subirlo a GitHub

Si ya creaste un repositorio vacío, puedes usar Git desde la raíz del proyecto:

```bash
git init
git branch -M main
git add .
git commit -m "Versión inicial de ImpulsoLab"
git remote add origin https://github.com/TU_USUARIO/impulso-lab.git
git push -u origin main
```

Sustituye `TU_USUARIO` por tu usuario real y confirma el nombre del repositorio. También puedes usar **Add file → Upload files** directamente en GitHub.

## 3. Historial persistente para cada estudiante

### Consola y ejecución local

Por defecto se usa **SQLite** y los registros se guardan en `data/historial.sqlite3`. El archivo permanece entre ejecuciones locales y registra:

- identificación introducida;
- fecha/hora UTC y UUID de cada simulación;
- escenario y parámetros;
- resultados de disparo e impacto por cuerpo;
- momentos y energías iniciales/finales, impulso, fuerza y explicaciones físicas.

El menú **4** de la consola permite consultar el historial y reabrir gráficos. La pestaña **Historial** realiza esta consulta en la aplicación web.

### Publicación web con persistencia real (Supabase)

**El almacenamiento local de Streamlit Community Cloud es efímero:** una app puede reiniciarse, replicarse o volver a desplegarse, perdiendo su SQLite local. Para conservar el historial en línea usa una base de datos externa como Supabase. Se incluye un backend opcional que funciona sin dependencias adicionales.

1. Crea un proyecto en [supabase.com](https://supabase.com/).
2. Desde **SQL Editor**, ejecuta el contenido del archivo [`supabase/schema.sql`](supabase/schema.sql). Esto crea la tabla e índice y habilita Row Level Security sin acceso público anónimo directo.
3. En el panel de configuración de API de Supabase, copia la URL del proyecto y la **clave secreta de servidor `service_role`**. Nunca uses esa clave desde código de navegador, ni la incluyas en un commit.
4. En el panel de tu app de Streamlit Cloud, abre **App settings → Secrets** y guarda:

```toml
SUPABASE_URL = "https://TU_PROYECTO.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "TU_CLAVE_PRIVADA_DE_SERVIDOR"
```

5. Reinicia la aplicación si es necesario. En adelante, la app utilizará Supabase en lugar de SQLite local.

Para probar Supabase localmente crea `.streamlit/secrets.toml` con esos mismos valores (este archivo **está excluido por `.gitignore`**) o define ambas variables de entorno. Existe un ejemplo en `.streamlit/secrets.toml.example`.

**Privacidad e identificación:** esta versión usa la identificación escrita en el formulario para agrupar registros, **no proporciona autenticación**. Cualquiera que conozca el identificador de otro estudiante podría consultar sus simulaciones a través de la interfaz. Para un despliegue público se recomienda usar **alias o códigos no sensibles**. Para historiales privados reales habría que incorporar usuarios autenticados y controles de acceso por sesión (por ejemplo Supabase Auth + políticas RLS). No introducir números de documento de identidad ni secretos personales.

## 4. Los tres escenarios

En todos los casos se calculan **dos etapas diferentes**:

- **A. Disparo:** el arma y el proyectil se consideran inicialmente en reposo. La velocidad de salida introducida es la velocidad del proyectil **respecto del suelo**. El arma adquiere velocidad de retroceso para mantener cero el momento horizontal total. La energía cinética del conjunto aumenta por transformación de energía química.
- **B. Impacto:** el proyectil se considera separado del arma y llega al blanco sin variación de su rapidez (vuelo idealizado). Esta segunda etapa utiliza las leyes correspondientes al tipo de choque. El arma ya no participa en los cálculos del choque.

### Escenario 1: impacto individual contra barrera anclada

El proyectil impacta en una barrera fija e impenetrable. Se ingresa su velocidad final **≤ 0**: cero cuando se detiene, negativa cuando rebota. Se calculan el cambio de momento, impulso ejercido por la barrera, energía y, si se conoce `Δt`, fuerza promedio.

**Precisión importante:** el subsistema analizado contiene *solo el proyectil*; su momento **no se conserva** porque la barrera ejerce impulso externo. Para una descripción aislada completa habría que incluir barrera, soporte y Tierra. Un rebote ideal con la misma rapidez puede conservar la energía cinética del proyectil, aunque cambie su momento.

### Escenario 2: choque perfectamente elástico

Proyectil y blanco **libres para desplazarse** horizontalmente. Se introducen masas y velocidades iniciales. El programa calcula automáticamente **ambas velocidades finales** usando conservación del momento total y coeficiente de restitución `e = 1` (equivalente a conservación de energía cinética total para dos cuerpos en 1D). No se piden velocidades finales desconocidas.

### Escenario 3: choque inelástico

El mismo modelo de dos cuerpos libres, pero se introduce `0 ≤ e < 1`:

- `e = 0`: **perfectamente inelástico**. Los cuerpos comparten velocidad final y en esta simulación se consideran unidos.
- `0 < e < 1`: **parcialmente inelástico**. Se conserva el momento total, pero parte de la energía cinética se transforma en deformación, calor, sonido y otras formas. **La energía total no desaparece.**

### Ecuaciones utilizadas

| Magnitud | Ecuación | Unidad SI |
| --- | --- | --- |
| Momento de un cuerpo | `p = m·v` | kg·m/s |
| Impulso de la interacción | `J = p_final − p_inicial` | N·s |
| Energía cinética | `Ec = (1/2)·m·v²` | J |
| Fuerza promedio (si hay tiempo) | `F_prom = J / Δt` | N |
| Retroceso del arma | `v_arma = −(m_proyectil/m_arma)·v_proyectil` | m/s |
| Conservación en choque libre | `m1·u1 + m2·u2 = m1·v1 + m2·v2` | kg·m/s |
| Restitución | `e = (v2−v1)/(u1−u2)` | adimensional |
| Velocidad final 1 | `v1 = [(m1−e·m2)·u1 + (1+e)·m2·u2]/(m1+m2)` | m/s |
| Velocidad final 2 | `v2 = [(1+e)·m1·u1 + (m2−e·m1)·u2]/(m1+m2)` | m/s |

**Convención:** movimiento hacia la derecha positivo; hacia la izquierda negativo. La dirección y la rapidez no son sinónimos. Por ello se mantienen los signos en velocidad, momento, impulso y fuerza.

## 5. Ejemplos listos para ejecutar

Usa los siguientes casos en consola/web, o genera automáticamente **cuatro archivos JSON + cuatro HTML animados** con:

```bash
python -m examples.demo_scenarios
```

Los archivos aparecerán en `salidas/ejemplos/` y el HTML podrá abrirse sin red.

Se usan números **ilustrativos y no representativos de un arma real**: masa proyectil `0,02 kg`, masa arma `2 kg`, velocidad de salida `30 m/s`, duración de colisión `0,02 s`.

| Escenario | Otros parámetros | Resultado principal | ΔEc del impacto |
| --- | --- | --- | --- |
| 1. Barrera anclada | `v_proyectil final = 0` | `J_proyectil = −0,6 N·s`; `F_prom = −30 N` | `−9 J` |
| 2. Elástico | `m_blanco = 0,4 kg`, `u_blanco = 0` | `v_proyectil final = −27,142857 m/s`; `v_blanco final = +2,857143 m/s` | `0 J` |
| 3a. Inelástico completo | `m_blanco = 0,4 kg`, `e = 0` | `v_ambos final = +1,428571 m/s` | `−8,571429 J` |
| 3b. Inelástico parcial | `m_blanco = 0,4 kg`, `e = 0,35` | `v_proyectil final = −8,571429 m/s`; `v_blanco final = +1,928571 m/s` | `−7,521429 J` |

El retroceso del arma es `−0,3 m/s` en los cuatro casos. El momento total **arma+proyectil** después del disparo es aproximadamente cero. En los choques entre cuerpos libres, el momento total del par **proyectil+blanco** es `0,6 kg·m/s` tanto antes como después.

## 6. Comprobar la instalación y ejecutar pruebas

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Las pruebas cubren masas y velocidades conocidas, choque de masas iguales, rebote en pared, casos inelásticos con y sin unión, restitución, ausencia de tiempo de contacto, parámetros inválidos, **200 colisiones aleatorias** con verificación de conservación, almacenamiento SQLite y generación de HTML.

## 7. Arquitectura del proyecto

```text
ImpulsoLab/
├── app.py                         # Interfaz web Streamlit
├── main.py                        # Punto de entrada de consola
├── requirements.txt               # Dependencias
├── requirements-dev.txt           # Dependencias de tests
├── README.md                      # Instrucciones y fundamentos
├── LICENSE
├── assets/
│   └── banner.svg                 # Ilustración vectorial original
├── physicslab/
│   ├── __init__.py
│   ├── models.py                   # Estructuras de datos y serialización
│   ├── calculations.py             # Motor físico y validación
│   ├── cli.py                      # Menús y presentación en consola
│   ├── reporting.py                # Ecuaciones y explicaciones automáticas
│   ├── visualization.py            # Diagramas Plotly y animación
│   └── storage.py                  # SQLite o Supabase
├── examples/
│   ├── demo_scenarios.py           # Cuatro casos reproducibles
│   └── resultados/                # Cuatro JSON de resultados de ejemplo
├── tests/                          # Pruebas unitarias
├── supabase/
│   └── schema.sql                  # Tabla remota opcional
├── .streamlit/
│   ├── config.toml                 # Colores y tema web
│   └── secrets.toml.example        # Guía de variables secretas
└── .github/workflows/
    └── tests.yml                   # Pruebas automáticas en GitHub
```

**Extender el laboratorio:** agregar nuevos escenarios a `Scenario` en `models.py`, su validación y fórmula en `calculations.py`, etiquetas/explicaciones en `reporting.py` y la selección visual en `app.py` y `cli.py`. Los modelos y el historial son independientes de la interfaz, y los gráficos pueden reemplazarse sin cambiar el cálculo físico.

## 8. Alcance físico y límites importantes

- **Modelo 1D idealizado** de choques centrales. No incluye dirección vertical, gravedad durante vuelo, efectos aerodinámicos, rotación, giro o dispersión.
- No predice **penetración, daño ni lesiones**, ni efectos reales de armas. Los parámetros de demostración son deliberadamente ilustrativos.
- El dibujo muestra **tres estados conceptuales**: previo al disparo, vuelo e inmediatamente después del impacto. **No es una trayectoria calculada en un tiempo real**, ni usa escala de distancias. Las flechas muestran signos de velocidad y sus valores numéricos, no longitudes proporcionales a la rapidez.
- El tiempo suministrado es **duración del contacto del impacto**, no tiempo de aceleración en el disparo. Sin `Δt`, el programa no inventa fuerzas medias.
- En el choque libre se ignoran fuerzas e impulsos externos horizontales. Si hay fricción o un soporte externo, las ecuaciones deben adaptarse.
- El modelo de restitución representa velocidades de separación; no resuelve deformación del material ni el perfil temporal de la fuerza.
- Se rechazan velocidades cercanas al régimen relativista y datos no finitos. La validación impide masas no positivas y colisiones donde el proyectil nunca alcanzaría al blanco dentro del esquema elegido.
- **No confundir** energía cinética con energía total: la primera puede cambiar mientras la energía total se conserva al incluir otras formas de energía.

## 9. Solución de problemas

**`ModuleNotFoundError: streamlit` o `plotly`:** comprueba que activaste el entorno virtual y ejecutaste `python -m pip install -r requirements.txt`.

**La consola no abre automáticamente el HTML:** los gráficos se guardan igualmente en `salidas/figuras/` y puedes abrirlos manualmente en cualquier navegador.

**Los valores del blanco no generan impacto:** comprueba que el proyectil parte a la izquierda y tiene mayor velocidad horizontal que el blanco (`u_proyectil > u_blanco`).

**Desaparece el historial web:** configura Supabase según el apartado 3. GitHub y Streamlit Cloud no sirven de base de datos persistente por sí solos.

**`git push` rechaza autenticación:** utiliza GitHub Desktop o los métodos vigentes de inicio de sesión de GitHub, no una contraseña de cuenta escrita directamente en la terminal.

---

**Uso previsto:** enseñanza, análisis matemático y divulgación de mecánica clásica. Código disponible bajo licencia MIT.
