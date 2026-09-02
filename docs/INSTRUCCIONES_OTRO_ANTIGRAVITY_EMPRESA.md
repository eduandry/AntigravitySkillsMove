# Instrucciones para Configurar el Repositorio de Empresa en Antigravity

Dado que tu máquina ya tiene ambas cuentas autenticadas:
- **Cuenta Personal:** `github.com-personal` (Usuario: `eduandry`)
- **Cuenta Empresa:** `github.com-trabajo` (Usuario: `tecnologiamzl`)

---

## 📋 Prompt para pasarle al otro Antigravity (Repositorio de Empresa)

Copia y pega este texto directamente en el chat del otro Antigravity donde esté abierto el proyecto de tu empresa:

```markdown
Por favor configura este repositorio para que trabaje exclusivamente con la cuenta de GitHub de la empresa (alias: github.com-trabajo / usuario: tecnologiamzl).

Realiza las siguientes acciones:

1. **Configurar el autor del repositorio local**:
   - `git config user.name "tecnologiamzl"` (o tu nombre empresarial)
   - `git config user.email "tu_correo_empresa@gelco.com.co"`

2. **Configurar el Remote URL de Git usando el alias de empresa**:
   - Reemplaza `https://github.com/tecnologiamzl/NOMBRE_REPO.git` o `git@github.com:...` por:
     `git remote set-url origin git@github.com-trabajo:tecnologiamzl/NOMBRE_REPO.git`
   *(Asegúrate de mantener el nombre real del repositorio actual)*.

3. **Verificar la conexión**:
   - Ejecuta `git remote -v` para confirmar que apunta a `github.com-trabajo`.
   - Ejecuta `git status` y `git fetch origin` para verificar la sincronización con la cuenta de empresa.
```

---

## 🛠️ Comandos Rápidos si prefieres ejecutarlos tú mismo en la terminal del otro Antigravity:

Solo ejecuta estos comandos dentro de la carpeta del proyecto de empresa:

```bash
# 1. Asignar el remote a la cuenta de empresa (reemplaza REPOSITORIO por el nombre real de tu repo)
git remote set-url origin git@github.com-trabajo:tecnologiamzl/REPOSITORIO.git

# 2. Asignar tu correo/nombre de empresa para este repositorio
git config user.name "tecnologiamzl"
git config user.email "tu_correo_empresa@empresa.com"

# 3. Comprobar que está listo y sincronizado
git fetch origin
git status
```
