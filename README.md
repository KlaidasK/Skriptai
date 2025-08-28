# Vartotojų procesų žurnalas
Šis PowerShell skriptas surenka visus vartotojų procesus sistemoje ir generuoja atskirus log failus kiekvienam vartotojui. Log failai atidaromi „Notepad“ programoje.  



## Funkcionalumas

- Suranda visus procesus sistemoje.  
- Filtruoja procesus pagal tikrus vartotojus (`C:\Users\`).  
- Sukuria atskirus log failus kiekvienam vartotojui su šia informacija:  
  - Procesų pavadinimai (`Name`)  
  - Procesų ID (`PID`)  
  - Procesų sukūrimo data (`CreationDate`)  
  - Pilnas proceso kelias (`ExecutablePath`)  
- Automatiškai atidaro log failus su Notepad.  
- Po peržiūros uždaro Notepad langus, kuriuos atidarė skriptas.  



## Naudojimas

```powershell
.\2u.ps1 [-Username <vartotojo_vardas>]
```

### Parametrai

- **`-Username`** *(neprivalomas)* – filtruoti procesus tik nurodytam vartotojui.  
  Jei nenurodytas, logai generuojami visiems tikriems vartotojams.  



## Pavyzdžiai

1. Surasti procesus visiems vartotojams:

```powershell
.\2u.ps1
```

2. Surasti procesus tik vartotojui `john`:

```powershell
.\2u.ps1 -Username john
```

---

## Log failų pavadinimo formatas

```
<vartotojas>-process-log-YYYY-MM-DD-HHmmss.txt
```

Pavyzdys: `john-process-log-2025-08-28-153045.txt`

---


## Pastabos

- Failai kuriami toje pačioje direktorijoje, kur paleistas skriptas.  
- Log failai automatiškai atidaromi Notepad, po peržiūros juos galima uždaryti.  
- Parametras `-Username` yra neprivalomas, jei jo nenurodysi – bus sugeneruoti visi vartotojai.  
