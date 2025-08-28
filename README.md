# Failų paieška (Python)

Šis Python skriptas leidžia ieškoti failų ir katalogų pagal vardą ar jo dalį, pradedant nuo esamos direktorijos. Kiekvienos paieškos rezultatai įrašomi į log failą `search_log.txt`.


## Funkcionalumas

- Ieško failų ir katalogų pagal vardą ar dalį (`case-insensitive`).  
- Rodo informaciją apie failą/katalogą:  
  - Vardas (`name`)  
  - Pilnas kelias (`path`)  
  - Savininkas (`owner`)  
  - Sukūrimo data (`created`)  
  - Paskutinio prieigos data (`accessed`)  
- Katalogams nurodo vieno lygio turinį.  
- Kiekviena paieška įrašoma į log failą su laiko žyma.  
- Dvipusis skirtukas `####` atskiria paieškos rezultatus log faile.  



## Reikalavimai

- Python 3.x  
- Windows arba Linux operacinė sistema  
- Windows vartotojams: automatiškai nustato failo savininką naudojant Windows API  
- Linux vartotojams: naudojama `pwd` modulio informacija  



## Naudojimas

```bash
4u.py <file_or_directory_name_or_part>
```

### Pavyzdžiai

1. Ieškoti failų ar katalogų, kurių pavadinime yra `report`:

```bash
p4u.py report
```

2. Ieškoti katalogų su daliniu vardu `docs`:

```bash
4u.py docs
```


## Log failas

- Visi rezultatai saugomi faile `search_log.txt` esamoje direktorijoje.  
- Kiekvienas įrašas turi:  
  - Paieškos datą ir laiką  
  - Paieškos terminą  
  - Rezultatus (failas/katalogas, kelias, savininkas, sukūrimo data, katalogo turinys)  
- Dvipusis skirtukas `####` atskiria kiekvienos paieškos rezultatus:  

```
Call Date: 2025-08-28 15:45:23
Search Term: report
Results:
File:
Name: report.docx
Path: ./documents/report.docx
Owner: user
Created: 2025-08-15 12:30:01
####
Directory:
Path: ./documents/reports
Contents (one level):
  - summary.pdf
  - data.xlsx
Owner: user
Created: 2025-08-10 09:15:42
####
```
