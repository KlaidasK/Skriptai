# Failų sąrašo BAT skriptas

Šis BAT skriptas skirtas surasti visus nurodyto tipo failus pasirinktoje direktorijoje ir sugeneruoti jų sąrašą su pilnais keliais. Rezultatas trumpam įrašomas į `file_log.txt` failą, kuris atidaromas „Notepad“ programoje, o po uždarymo automatiškai ištrinamas.



## Naudojimas

```bat
bash.bat [katalogas] [plėtinys]
```

### Parametrai

* **katalogas** *(neprivalomas)* – kelias iki katalogo, kuriame ieškoti failų.  
  Jei nenurodytas, naudojamas naudotojo profilis (`%USERPROFILE%`).
* **plėtinys** *(neprivalomas)* – kokius failus ieškoti (pvz., `.bat`, `.txt`, `.log`).  
  Jei nenurodytas, numatytasis yra `.bat`.

---

## Pavyzdžiai

1. Surasti visus `.bat` failus naudotojo kataloge:

   ```bat
   bash.bat
   ```

2. Surasti visus `.txt` failus kataloge `D:\Dokumentai`:

   ```bat
   bash.bat "D:\Dokumentai" .txt
   ```

---

## Ką skriptas daro

1. Nustato katalogą ir failų plėtinį (pagal numatytuosius arba nurodytus parametrus).
2. Sukuria laikiną `file_log.txt` failą `%TEMP%` kataloge.
3. Į jį įrašo dabartinę datą ir laiką.
4. Surenka visus atitinkančius failus rekursyviai (įskaitant poaplankius).
5. Įrašo failo pavadinimą ir pilną kelią.
6. Atidaro `file_log.txt` „Notepad“ lange.
7. Po uždarymo automatiškai ištrina log failą.

