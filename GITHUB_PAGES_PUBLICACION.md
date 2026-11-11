# Cómo publicar ImpulsoLab solamente con GitHub

**No necesitas Streamlit Cloud, Render, Vercel, ni instalar Python en un servidor.** Usa la versión `docs/` ya incluida en el proyecto.

## Paso 1: crear el repositorio

1. Entra a <https://github.com/new> e inicia sesión.
2. En **Repository name** escribe `ImpulsoLab`.
3. Selecciona **Public** (en GitHub Free, Pages se habilita para repositorios públicos).
4. Presiona **Create repository**. Puedes dejar desmarcado el README inicial.

## Paso 2: subir los archivos

1. Descomprime `ImpulsoLab_Proyecto_Completo_GitHub_Pages.zip`.
2. **Abre** la carpeta `ImpulsoLab` dentro del ZIP descomprimido.
3. En GitHub usa **Add file → Upload files**.
4. Arrastra **todo el contenido de esa carpeta** al navegador, incluidos los archivos y las carpetas (`docs/`, `physicslab/`, `tests/`, `.github/`, etc.). No arrastres el ZIP sin descomprimir.
5. Confirma con **Commit changes**.

En la raíz de GitHub deben verse al menos:

```
ImpulsoLab/ (raíz del repositorio)
├── README.md
├── app.py
├── main.py
├── requirements.txt
├── physicslab/
├── tests/
└── docs/
    ├── index.html
    ├── app.js
    ├── physics.js
    ├── styles.css
    ├── favicon.svg
    └── tests/
```

## Paso 3: activar GitHub Pages

1. Dentro de tu repositorio, pulsa **Settings**.
2. En el menú izquierdo abre **Pages**.
3. En **Build and deployment**, selecciona **Deploy from a branch** como Source.
4. En Branch selecciona **`main`** y en el selector de carpeta **`/docs`**.
5. Pulsa **Save**.
6. Luego de que termine la compilación, pulsa **Visit site** en esa misma pantalla.

El sitio debería abrirse en:

`https://TU_USUARIO.github.io/ImpulsoLab/`

Reemplaza `TU_USUARIO` con tu nombre real de usuario de GitHub. Si cambias el nombre del repositorio, cambia también ese segmento de la URL. Los cambios pueden demorar algunos minutos en reflejarse.

## ¿Por qué hay dos aplicaciones?

- `main.py` y `app.py`: versiones **Python** para demostrar en un computador o desplegar en un servidor Python. GitHub Pages **no ejecuta** estos archivos.
- `docs/index.html`, `docs/app.js`, `docs/physics.js`: versión equivalente **web estática** con cálculos JavaScript, animaciones y controles que funciona directamente desde GitHub Pages.
- El **historial web** funciona con `localStorage` y se mantiene en el mismo navegador. No se sincroniza con otros dispositivos ni con el historial SQLite que genera Python. Los estudiantes pueden exportar JSON para conservar sus resultados.

## Solución de problemas

- **404:** confirma que `docs/index.html` esté directamente dentro de `docs/` **en la raíz del repositorio**, y que la fuente sea `main /docs`.
- **Se ve el README, no la app:** entraste en la URL del repositorio (`github.com/...`) y no en la del sitio (`TU_USUARIO.github.io/ImpulsoLab/`).
- **Se ve la página pero no funciona Simular:** verifica que `docs/app.js` y `docs/physics.js` se hayan subido al mismo nivel que `docs/index.html`.
- **En otra computadora no aparece el historial:** es normal; GitHub Pages no tiene base de datos. Usa **Exportar historial JSON** para conservar el archivo.
- **No aparece la opción `/docs`:** verifica que el directorio `docs/` ya exista en `main` y contenga `index.html`.

Documentación oficial: <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>
