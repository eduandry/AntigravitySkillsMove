# Prompt e Instrucciones para Configurar el Otro Antigravity (Cuenta Empresa)

Copia y pega el siguiente bloque de texto en el chat del **otro Antigravity**. El asistente ejecutará y configurará automáticamente todo el entorno SSH y Git en esa máquina/ventana sin bloqueos interactivos.

---

```markdown
Por favor configura este entorno para conectarse a GitHub con mi cuenta de empresa mediante SSH.

Realiza los siguientes pasos de forma automática:

1. **Crear directorio SSH y agregar GitHub a known_hosts (para evitar errores de Host key verification)**:
   Ejecuta en PowerShell:
   ```powershell
   if (!(Test-Path "$HOME\.ssh")) { New-Item -ItemType Directory -Path "$HOME\.ssh" -Force }
   ssh-keyscan -t ed25519,rsa github.com | Out-File -Encoding ascii -Append "$HOME\.ssh\known_hosts"
   ```

2. **Generar la clave SSH para la cuenta de empresa** (si no existe aún):
   ```powershell
   if (!(Test-Path "$HOME\.ssh\id_ed25519_empresa")) {
       ssh-keygen -t ed25519 -C "tu_correo_empresa@empresa.com" -f "$HOME\.ssh\id_ed25519_empresa" -N '""'
   }
   ```

3. **Configurar el archivo `~/.ssh/config`**:
   Asegúrate de que contenga la configuración con `StrictHostKeyChecking accept-new` para que nunca se bloquee en prompts interactivos:
   ```ssh
   Host github.com
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_ed25519_empresa
       StrictHostKeyChecking accept-new
       IdentitiesOnly yes

   Host github.com-empresa
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_ed25519_empresa
       StrictHostKeyChecking accept-new
       IdentitiesOnly yes
   ```

4. **Mostrar y copiar la clave pública**:
   Ejecuta:
   ```powershell
   Get-Content "$HOME\.ssh\id_ed25519_empresa.pub"
   ```
   Indícame el contenido de la clave pública para agregarla a https://github.com/settings/keys en mi cuenta de GitHub de la empresa.

5. **Configurar la identidad del repositorio actual**:
   Una vez agregada la clave, configura en este repositorio local:
   - `git config user.name "Tu Nombre / Empresa"`
   - `git config user.email "tu_correo_empresa@empresa.com"`
   - Actualizar el remote con la URL real de SSH del repositorio de la empresa.

6. **Validar la conexión**:
   Ejecutar `ssh -T git@github.com` y confirmar que responde exitosamente.
```

---

## 🛠️ Explicación de por qué falló el comando anterior

El error que viste:
```text
The authenticity of host 'github.com' can't be established.
Host key verification failed. (yes/no/[fingerprint])?
```

Ocurre porque SSH en Windows nunca antes se había conectado a GitHub y pide confirmación manual interactiva (`yes`). Como la consola de Antigravity no es interactiva para este prompt, el comando se cancela automáticamente.

**La solución definitiva** es registrar la huella de GitHub de antemano ejecutando:
```powershell
ssh-keyscan -t ed25519,rsa github.com | Out-File -Encoding ascii -Append "$HOME\.ssh\known_hosts"
```
Y agregando `StrictHostKeyChecking accept-new` en el archivo `~/.ssh/config`.
