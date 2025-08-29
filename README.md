# PHP procesų ataskaitos

PHP skriptas, kuris Linux sistemoje surenka procesų informaciją naudodamas `ps` ir išsaugo rezultatą pasirinktu formatu: **txt**, **csv** arba **html**. Sukūręs log failą, skriptas laukia, kol paspausite Enter, ir tuomet jį ištrina.

## Funkcionalumas

- Gaunami procesų duomenys per:
  ```
  ps -eo user,pid,%cpu,%mem,vsz,rss,tty,stat,start,time,cmd --no-headers
  ```
- Palaikomi **trys formatai**: `txt` (numatytasis), `csv`, `html`.
- **Filtravimas pagal naudotoją** (neprivalomas).
- HTML formate sugeneruojama paprasta lentelė.
- Įrašomas log failas (`process_log.<format>`), po Enter paspaudimo — pašalinamas.


## Naudojimas

```bash
5.php [format] [username]
```

### Parametrai

- `format` *(neprivalomas)*: `txt` | `csv` | `html`  
  (numatytasis: `txt`)
- `username` *(neprivalomas)*: filtruoti procesus tik tam naudotojui  
  (pvz., `jonas`; paieška dalinė, **case-insensitive**)


## Pavyzdžiai

Visi procesai į `.txt` (numatytasis):
```bash
5.php
```

Visi procesai į `.csv`:
```bash
5.php csv
```

Tik naudotojo **jonas** procesai į `.html`:
```bash
5.php html jonas
```


## Išvestis

Sukuriamas failas tame pačiame kataloge:
- `process_log.txt` **arba** `process_log.csv` **arba** `process_log.html`

Programa išves:
```
Log failas sukurtas: /kelias/iki/process_log.<format>
Paspausk Enter, kad ištrintum log failą ir baigtum darbą...
```
Paspaudus **Enter**, failas bus ištrintas:
```
Log failas ištrintas. Baigiama.
```


## Reikalavimai

- **Linux** sistema su `ps` (paketas `procps`)
- **PHP CLI** (pvz., `php8.2-cli`)


## Pastabos ir patarimai

- Jei gaunate klaidą apie įrašymo teises, paleiskite kataloge, kuriame turite teisę kurti failus, arba naudokite `sudo` (jei būtina).
- Filtravimas pagal naudotoją yra **dalinis**: `jon` atitiks ir `jonas`, ir `jones`.
- Jei norite **neištrinti** log failo po peržiūros, pašalinkite dalį su `fgets(STDIN)` ir `unlink($filename)`.

