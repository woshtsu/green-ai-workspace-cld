# Arnés de verificación visual del frontend
Sirve `software/frontend` con una sesión de Supabase SIMULADA (sin login real) y reenvía `/api/*` a los servicios públicos de Render (datos simulados reales, sin JWT).
```bash
python herramientas_IA/arnes_frontend/harness.py software/frontend 18999
# abrir http://127.0.0.1:18999/dashboard.html (también network.html y flows.html)
```
Solo para pruebas locales. Requiere los servicios `*-dev` de Render despiertos (URLs en `docs/evidencias/render-desarrollo-20261107.md`). No sustituye la prueba con sesión real.
