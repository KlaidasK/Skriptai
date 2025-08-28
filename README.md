# Vartotojų procesų žurnalas (Linux Bash)

Šis Bash skriptas surenka procesų informaciją Linux sistemoje kiekvienam realiam vartotojui ir sukuria log failus su procesų duomenimis.  


## Funkcionalumas

- Suranda visus procesus sistemoje (`ps -eo user:20,pid,comm,%cpu,%mem`).  
- Filtruoja tikrus vartotojus (`UID >= 1000` ir shell `bash` arba `sh`).  
- Sukuria log failus kiekvienam vartotojui su šiomis informacija:  
  - Procesų pavadinimas (`comm`)  
  - PID  
  - CPU naudojimas (%)  
  - Atminties naudojimas (%)  
- Galima pasirinkti konkretų vartotoją loginiam filtruoti.  
- Automatiškai sukuria katalogą su laiko žymekliu log failams.  
- Po peržiūros galima ištrinti visus log failus.  


## Naudojimas

```bash
./3u.sh [username]
```

### Parametrai

- **`username`** *(neprivalomas)* – filtruoti procesus tik nurodytam vartotojui.  
  Jei nenurodytas, log failai sukuriami visiems realiems vartotojams.  


## Pavyzdžiai

1. Surasti procesus visiems vartotojams:

```bash
./3u.sh
```

2. Surasti procesus tik vartotojui `john`:

```bash
./3u.sh john
```


## Log failų formatas

- Kiekvienam vartotojui sukuriamas atskiras log failas:  

```
<username>-process-log-YYYY-MM-DD-HHmmSS.log
```

- Pavyzdys: `john-process-log-2025-08-28-153045.log`  
- Log faile yra:  
  - Username  
  - Date ir Time  
  - Procesų sąrašas su PID, CPU ir atminties naudojimu  


## Pastabos

- Log failai laikinai saugomi su katalogo pavadinimu pagal datą ir laiką.  
- Paspaudus Enter visi log failai automatiškai ištrinami.  
- Jei nenurodytas vartotojas, sukuriami log failai visiems realiems vartotojams.  
