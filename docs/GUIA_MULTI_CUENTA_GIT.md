# Guía: Cómo Usar Múltiples Cuentas de Git en Antigravity

Esta guía explica cómo configurar dos o más cuentas de GitHub/Git en tu máquina para que Antigravity (y la terminal) sincronicen automáticamente cada repositorio con la cuenta correcta sin conflictos de credenciales.

---

## 🎯 Las 2 Estrategias Recomendadas

| Estrategia | Cuándo usarla | Ventaja |
| :--- | :--- | :--- |
| **Opción A: Claves SSH con `~/.ssh/config` (Recomendada)** | Ideal para separar cuentas de forma 100% confiable y sin pedir contraseñas. | Funciona siempre, no depende de tokens temporales. |
| **Opción B: Rutas condicionales (`includeIf` en `.gitconfig`)** | Ideal si organizas tus proyectos en carpetas separadas (ej. `E:/IA/Personal/` y `E:/IA/Trabajo/`). | Automático según la carpeta donde esté el proyecto. |

---

## 🚀 Opción A: Configuración Multi-Cuenta mediante SSH (Paso a Paso)

### 1. Generar una clave SSH para cada cuenta
Abre PowerShell o tu terminal y genera una clave para cada cuenta:

```powershell
# Clave para la Cuenta 1 (Personal)
ssh-keygen -t ed25519 -C "correo_personal@ejemplo.com" -f "$HOME\.ssh\id_ed25519_personal"

# Clave para la Cuenta 2 (Trabajo / Secundaria)
ssh-keygen -t ed25519 -C "correo_trabajo@ejemplo.com" -f "$HOME\.ssh\id_ed25519_trabajo"
```
*(Presiona Enter cuando te pida passphrase para dejarla vacía, o asigna una contraseña si prefieres).*

---

### 2. Agregar las claves públicas a cada cuenta de GitHub
1. Copia el contenido de la clave pública 1:
   ```powershell
   Get-Content "$HOME\.ssh\id_ed25519_personal.pub" | Set-Clipboard
   ```
   Ve a **GitHub (Cuenta 1)** > **Settings** > **SSH and GPG keys** > **New SSH key** y pégala.

2. Copia el contenido de la clave pública 2:
   ```powershell
   Get-Content "$HOME\.ssh\id_ed25519_trabajo.pub" | Set-Clipboard
   ```
   Ve a **GitHub (Cuenta 2)** > **Settings** > **SSH and GPG keys** > **New SSH key** y pégala.

---

### 3. Configurar el archivo `~/.ssh/config`
Crea o edita el archivo `C:\Users\TU_USUARIO\.ssh\config` (en PowerShell: `notepad $HOME\.ssh\config`) con el siguiente contenido:

```ssh
# ==========================================
# Cuenta 1: Personal
# ==========================================
Host github.com-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes

# ==========================================
# Cuenta 2: Trabajo / Secundaria
# ==========================================
Host github.com-trabajo
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_trabajo
    IdentitiesOnly yes
```

---

### 4. Configurar el repositorio para usar la cuenta correcta

En lugar de usar la URL estándar `git@github.com:...`, usa el alias que definiste en el archivo config (`github.com-personal` o `github.com-trabajo`).

#### Para un repositorio existente:
```bash
# Si es para la Cuenta Personal:
git remote set-url origin git@github.com-personal:usuario_personal/mi-repo.git

# Si es para la Cuenta de Trabajo:
git remote set-url origin git@github.com-trabajo:usuario_trabajo/mi-repo-empresa.git
```

#### Para clonar un nuevo repositorio:
```bash
git clone git@github.com-personal:usuario_personal/mi-repo.git
```

#### Configurar nombre y correo del autor dentro de cada repo:
Dentro de la carpeta del proyecto:
```bash
git config user.name "Tu Nombre Personal"
git config user.email "correo_personal@ejemplo.com"
```

---

## 📂 Opción B: Automatización por Carpetas con `includeIf`

Si guardas tus repositorios organizados por carpetas:
- `E:/IA/Personales/` (todos usan Cuenta 1)
- `E:/IA/Empresariales/` (todos usan Cuenta 2)

Puedes configurar tu archivo global `~/.gitconfig`:

```ini
[user]
    name = Tu Nombre General
    email = correo_predeterminado@ejemplo.com

# Si el repo está dentro de E:/IA/Personales/
[includeIf "gitdir/i:E:/IA/Personales/"]
    path = ~/.gitconfig-personal

# Si el repo está dentro de E:/IA/Empresariales/
[includeIf "gitdir/i:E:/IA/Empresariales/"]
    path = ~/.gitconfig-trabajo
```

Y creas los archivos complementarios:

**`~/.gitconfig-personal`**:
```ini
[user]
    name = Usuario Personal
    email = correo_personal@ejemplo.com
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_personal
```

**`~/.gitconfig-trabajo`**:
```ini
[user]
    name = Usuario Trabajo
    email = correo_trabajo@ejemplo.com
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_trabajo
```

---

## 🔑 Opción C: Usando HTTPS y Tokens (PAT)

Si prefieres usar HTTPS en lugar de SSH, puedes incrustar el token de acceso personal directamente en la URL del remote del repositorio:

```bash
# Configurar remote con Token específico:
git remote set-url origin https://TOKEN_CUENTA_1@github.com/usuario1/mi-repo.git
```

---

## ✅ Comprobar la conexión

Prueba que cada alias responde a la cuenta correcta desde tu consola:
```bash
ssh -T git@github.com-personal
# Deberá responder: Hi usuario_personal! You've successfully authenticated...

ssh -T git@github.com-trabajo
# Deberá responder: Hi usuario_trabajo! You've successfully authenticated...
```
