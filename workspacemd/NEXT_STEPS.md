# Próximos Pasos (NEXT_STEPS) - AntigravitySkillsMove

## Hoja de Ruta Sugerida:
1. **Publicación en PyPI**:
   - Compilar paquete wheel y subir a PyPI con `twine` para habilitar `pip install antigravity-skills-move`.
2. **Encriptación de Paquetes con Contraseña**:
   - Añadir opción `--encrypt` con AES/ZipCrypto para proteger bundles compartidos por mensajería pública.
3. **Hub / Catálogo Comunitario de Skills**:
   - Integración con un índice JSON público de skills curadas por la comunidad para instalación rápida (`antigravity-skills-move install <skill-name>`).
4. **Interfaz Gráfica Opcional (Web Dashboard)**:
   - Panel web visual ligero (`--web-ui`) para gestionar skills arrastrando y soltando archivos.
