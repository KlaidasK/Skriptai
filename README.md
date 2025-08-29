# Failų Tvarkyklė (Python)

Ši programa yra interaktyvi **failų tvarkyklė**, skirta automatizuotam darbui su failais. Ji gali rūšiuoti, pervadinti, šalinti, analizuoti ir archyvuoti failus pagal nurodytus kriterijus. Taip pat pateikiami log’ai.


## Funkcionalumas

Programa leidžia atlikti šiuos veiksmus:

1. **Pašalinti failus pagal pavadinimą, tipą arba datą**
2. **Rūšiuoti failus pagal kategorijas** (Dokumentai, Paveikslėliai, Vaizdo įrašai, Muzika, Archyvai, Kodas, Lentelės, Kiti)
3. **Skaičiuoti failų kiekį kiekvienoje kategorijoje**
4. **Pašalinti tuščius aplankus**
5. **Rodyti didžiausius failus pagal dydį**
6. **Suskaidyti failus į subkategorijas pagal pirmą raidę**
7. **Sukurti visų failų archyvą (.zip)**
8. **Vykdyti viską automatiškai vienu metu**
9. **Peržiūrėti galimus pašalinti failus prieš trinant**
10. **Pervadinti visus failus pagal pasirinktą šabloną**
11. **Pašalinti failus, mažesnius nei nurodytas MB dydis**
12. **Apskaičiuoti kategorijų bendras apimtis MB**
13. **Keisti darbo aplanką**
14. **Išeiti iš programos**

## Failų kategorijos

| Kategorija     | Pletiniai                                                                 |
|----------------|---------------------------------------------------------------------------|
| Dokumentai     | `.pdf`, `.docx`, `.txt`, `.md`                                           |
| Paveikslėliai  | `.jpg`, `.jpeg`, `.png`, `.gif`                                          |
| Vaizdo įrašai  | `.mp4`, `.mov`, `.avi`                                                   |
| Muzika         | `.mp3`, `.wav`, `.flac`                                                  |
| Archyvai       | `.zip`, `.rar`, `.7z`                                                    |
| Kodas          | `.py`, `.js`, `.html`, `.css`, `.java`                                   |
| Lentelės       | `.xls`, `.xlsx`, `.csv`                                                  |
| Kiti           | Visi kiti failai, kurie nepatenka į aukščiau nurodytas kategorijas       |

**Svarbūs failai (`Svarbu.txt`, `Projektas.docx`) nėra trinami**, net jei atitinka pašalinimo kriterijus.


## Naudojimas

1. Atsisiųskite arba nukopijuokite `failu_tvarkykle.py` skriptą.
2. Paleiskite programą:

```bash
python failu_tvarkykle.py
```
3. Pasirinkite veiksmą iš meniu (1–14).

4. Sekite instrukcijas ekrane.

## Žurnalai (Log’ai)

log.txt – įprasti veiksmų įrašai (pvz., failų perkėlimas, pervadinimas).

errors.txt – klaidų pranešimai (pvz., jei nepavyksta pervadinti ar pašalinti failo).

## Automatinis režimas

Pasirinkus 8 meniu punktą, programa automatiškai:

Surūšiuoja failus pagal kategorijas

Suskaido į subkategorijas

Suskaičiuoja failus

Parodo didžiausius failus

Pašalina tuščius aplankus

Sukuria archyvą (archyvas.zip)
