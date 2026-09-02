# 🔒 Guía: Repositorio Privado para Sincronizar Skills y Servidores MCP

Esta guía te muestra cómo conectar tu **repositorio privado personal** para mantener exactamente las mismas Skills, Plugins, Reglas y **Servidores MCP** sincronizados entre todos tus equipos de cómputo.

---

## 🛠️ 1. ¿Es posible transferir los servidores MCP (Model Context Protocol)?

**¡Sí, 100% posible y ya está integrado!**

### ¿Dónde y cómo se guardan los MCP en Antigravity?
Antigravity almacena los servidores MCP globales en el archivo:
- **Windows**: `C:\Users\<TuUsuario>\.gemini\config\mcp_config.json`
- **macOS / Linux**: `~/.gemini/config/mcp_config.json`

Tu archivo [`mcp_config.json`](file:///e:/IA/Desarrollos/Traductor/MyAntigravitySkills/mcp_config.json) define todos los servidores de herramientas (ej: `notebooks`, `visualization`, bases de datos, APIs personalizadas, etc.).

Al sincronizar este archivo a través de tu repositorio privado, **todos tus servidores MCP quedan automáticamente configurados en tus otros computadores**.

---

## 📁 2. Carpeta de tu Repositorio Privado Lista Localmente

Ya he creado y poblado la carpeta con todo tu ecosistema actual en:  
[`e:\IA\Desarrollos\Traductor\MyAntigravitySkills`](file:///e:/IA/Desarrollos/Traductor/MyAntigravitySkills)

### Contenido Inicial Preparado:
- ⚡ **`skills/`**: Tus 41 Skills globales.
- 🔌 **`plugins/`**: Tus 6 Plugins (Science con 37 sub-skills, Android CLI, DevTools, etc.).
- 🛠️ **`mcp_config.json`**: Tu configuración de servidores MCP.
- 📜 **`global_workflows/`**: Flujos de trabajo globales.
- 🚀 **`sync.bat` y `sync.sh`**: Sincronizadores automáticos de 1-clic.

---

## 🌐 3. Pasos para Crear y Vincular tu Repositorio Privado en GitHub

### Paso 1: Crear el Repositorio Privado en GitHub
1. Abre tu navegador y ve a [GitHub - New Repository](https://github.com/new).
2. **Repository name**: `MyAntigravitySkills` (o el nombre que prefieras).
3. **Description**: `Personal vault for Antigravity skills and MCP configs`.
4. **Visibility**: Selecciona **🔒 Private** (Privado, para proteger tus prompts y configuraciones).
5. Deja las casillas de README, .gitignore y License **desmarcadas**.
6. Haz clic en **Create repository**.

---

### Paso 2: Subir tus Skills y MCP a tu Repositorio Privado

Abre tu terminal en PowerShell y ejecuta:

```powershell
cd E:\IA\Desarrollos\Traductor\MyAntigravitySkills

# 1. Vincular el repositorio remoto privado
git remote add origin https://github.com/eduandry/MyAntigravitySkills.git

# 2. Subir todo a la rama main
git push -u origin main
```

---

## 💻 4. Cómo Sincronizar en tu Segundo Computador (Laptop / Oficina)

En cualquier otro computador donde uses Antigravity:

1. **Clona tu repositorio privado**:
   ```powershell
   git clone https://github.com/eduandry/MyAntigravitySkills.git
   cd MyAntigravitySkills
   ```

2. **Ejecuta la sincronización**:
   - En **Windows**: Haz doble clic en [`sync.bat`](file:///e:/IA/Desarrollos/Traductor/MyAntigravitySkills/sync.bat) o ejecuta `.\sync.bat`.
   - En **macOS / Linux**: Ejecuta `./sync.sh`.

### ¿Qué ocurre de forma automática?
- **Instalación local instantánea**: Se copian todas las 41 skills, 6 plugins y `mcp_config.json` en el `~/.gemini/config/` de esa máquina.
- **Sincronización Bidireccional continua**:
  - Si modificas una skill en la laptop, `sync.bat` la sube a GitHub.
  - Al volver a tu PC de escritorio y ejecutar `sync.bat`, descargará los cambios automáticamente.
