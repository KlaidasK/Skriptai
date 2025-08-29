import os
import shutil
from pathlib import Path
from datetime import datetime
import zipfile
import time

# Kategorijos pagal failo tipa
CATEGORIES = {
    'Dokumentai': ['.pdf', '.docx', '.txt', '.md'],
    'Paveiksleliai': ['.jpg', '.jpeg', '.png', '.gif'],
    'Vaizdo_irasai': ['.mp4', '.mov', '.avi'],
    'Muzika': ['.mp3', '.wav', '.flac'],
    'Archyvai': ['.zip', '.rar', '.7z'],
    'Kodas': ['.py', '.js', '.html', '.css', '.java'],
    'Lenteles': ['.xls', '.xlsx', '.csv'],
}

IMPORTANT_FILES = ['Svarbu.txt', 'Projektas.docx']

LOG_FILE = "log.txt"
ERROR_LOG_FILE = "errors.txt"

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def log_error(message):
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")


def remove_files_by(name=None, extension=None, date=None, folder='.'):
    count = 0
    # Pereiname per visus failus ir aplankus rekursyviai
    for file in Path(folder).rglob('*'):
        if file.is_file():
            # Patikrinti, ar failas yra svarbus, jei taip, praleisti
            if file.name in IMPORTANT_FILES:
                continue
            # Patikrinimai pagal pavadinimą, plėtinį ir datą
            if (name and name in file.name) or (extension and file.suffix == extension) or \
               (date and datetime.fromtimestamp(file.stat().st_mtime).date() == date):
                try:
                    file.unlink()  # Pašalinti failą
                    count += 1
                    print(f"Pasalinta faila: {file}")  # Log įrašas
                except Exception as e:
                    print(f"Nepavyko istrinti {file}: {e}")  # Klaidos pranešimas
    print(f"Pasalinta failu: {count}")  # Bendras pašalintų failų skaičius


def preview_deletable_files(name=None, extension=None, date=None, folder='.'):
    print("Galimi pasalinimui failai:")
    # Pereiname per visus failus ir aplankus rekursyviai
    for file in Path(folder).rglob('*'):
        if file.is_file():
            # Patikrinimai pagal pavadinimą, plėtinį ir datą
            if (name and name in file.name) or (extension and file.suffix == extension) or \
               (date and datetime.fromtimestamp(file.stat().st_mtime).date() == date):
                print(f"- {file.name}")  # Rodo failą, kuris gali būti pašalintas


def sort_files_by_category(folder='.'):
    folder = Path(folder)
    for file in folder.iterdir():
        if file.is_file():
            moved = False
            for category, extensions in CATEGORIES.items():
                if file.suffix.lower() in extensions:
                    category_path = folder / category
                    category_path.mkdir(exist_ok=True)
                    shutil.move(str(file), str(category_path / file.name))
                    moved = True
                    log(f"Failas {file} perkeliamas i {category}")
                    break
            if not moved:
                other_path = folder / 'Kiti'
                other_path.mkdir(exist_ok=True)
                shutil.move(str(file), str(other_path / file.name))


def rename_files(folder='.', prefix='renamed_', start_index=1):
    folder = Path(folder)
    i = start_index
    for file in folder.glob('*'):
        if file.is_file():
            new_name = f"{prefix}{i}{file.suffix}"
            try:
                file.rename(folder / new_name)
                log(f"Renamed {file.name} -> {new_name}")
                i += 1
            except Exception as e:
                log_error(f"Nepavyko pervadinti {file.name}: {e}")


def count_files_per_category(folder='.'):
    folder = Path(folder)
    print("Failu kiekis kiekvienoje kategorijoje:")
    for category in list(CATEGORIES.keys()) + ['Kiti']:
        cat_folder = folder / category
        if cat_folder.exists():
            count = len(list(cat_folder.glob('*')))
            print(f"{category}: {count}")
        else:
            print(f"{category}: 0")


def remove_empty_dirs(folder='.'):
    folder = Path(folder)
    removed = 0
    for sub in folder.rglob('*'):
        if sub.is_dir() and not any(sub.iterdir()):
            sub.rmdir()
            removed += 1
            log(f"Pasalintas tuscias aplankas: {sub}")
    print(f"Pasalinta tusciu aplanku: {removed}")


def analyze_files_by_size(folder='.', top_n=5):
    folder = Path(folder)
    files = [f for f in folder.rglob('*') if f.is_file()]
    files.sort(key=lambda f: f.stat().st_size, reverse=True)
    print(f"Top {top_n} didziausi failai:")
    for f in files[:top_n]:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"{f.name} — {size_mb:.2f} MB")


def remove_files_smaller_than(folder='.', min_mb=1):
    count = 0
    folder = Path(folder)
    for file in folder.rglob('*'):
        if file.is_file() and file.stat().st_size < min_mb * 1024 * 1024:
            try:
                file.unlink()
                count += 1
                log(f"Removed small file: {file}")
            except Exception as e:
                log_error(f"Error deleting {file}: {e}")
    print(f"Pasalinta mazesniu nei {min_mb}MB failu: {count}")


def auto_subcategorize(folder='.'):
    folder = Path(folder)
    for category in CATEGORIES.keys():
        cat_folder = folder / category
        if cat_folder.exists():
            for file in cat_folder.glob('*'):
                if file.is_file():
                    subfolder_name = file.name[0].upper()
                    subfolder = cat_folder / subfolder_name
                    subfolder.mkdir(exist_ok=True)
                    shutil.move(str(file), str(subfolder / file.name))


def create_archive_copy(folder='.', archive_name='archyvas.zip'):
    archive_path = Path(folder) / archive_name
    with zipfile.ZipFile(archive_path, 'w') as archive:
        for dirpath, _, filenames in os.walk(folder):
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                if archive_name not in f:
                    archive.write(filepath, os.path.relpath(filepath, folder))
    print(f"Sukurta archyvo kopija: {archive_path}")


def get_category(file_extension):
    """Grąžina failo kategoriją pagal plėtinį"""
    for category, extensions in CATEGORIES.items():
        if file_extension in extensions:
            return category
    return "Kiti"  # Jei plėtinys nepriklauso jokiai kategorijai

def category_sizes(folder):
    """Skaičiuoja kiekvienos kategorijos dydį ir rodo tik esamas kategorijas"""
    category_sizes = {category: 0 for category in CATEGORIES.keys()}
    category_sizes["Kiti"] = 0  # Kategorija "Kiti"

    # Pereiti per visus failus aplanke
    for file in Path(folder).rglob('*'):
        if file.is_file():
            file_size = file.stat().st_size / (1024 * 1024)  # Konvertuoti į MB
            category = get_category(file.suffix.lower())
            category_sizes[category] += file_size
    
    # Atspausdinti tik tas kategorijas, kurios turi failų
    for category, size in category_sizes.items():
        if size > 0:
            print(f"{category}: {size:.2f} MB")


def is_important(file_path):
    return Path(file_path).name in IMPORTANT_FILES


def print_menu():
    print("\n=== Failu tvarkykle ===")
    print("1. Pasalinti failus pagal pavadinima, tipa arba data")
    print("2. Rusiuoti failus pagal kategorijas")
    print("3. Rodyti failu kieki kategorijose")
    print("4. Pasalinti tuscius aplankus")
    print("5. Analizuoti failus pagal dydi")
    print("6. Suskirstyti i subkategorijas (pagal pirma raide)")
    print("7. Sukurti archyva")
    print("8. Vykdyti viska automatiskai")
    print("9. Perziureti galimus pasalinti failus")
    print("10. Pervadinti visus failus")
    print("11. Pasalinti failus mazesnius nei nurodyta MB")
    print("12. Kategoriju bendros apimtys")
    print("13. Pakeisti aplanką")
    print("14. Iseiti")


def run_auto(folder):
    print("Pradedamas automatizuotas tvarkymas...")
    sort_files_by_category(folder)
    auto_subcategorize(folder)
    count_files_per_category(folder)
    analyze_files_by_size(folder)
    remove_empty_dirs(folder)
    create_archive_copy(folder)
    print("Baigta.")


def get_folder():
    folder = input("Iveskite aplanko kelia (pvz., C:/Users/Vartotojas/Darbai): ").strip()
    if not folder:
        return '.'
    return folder

def change_folder():
    """Keičia aplanko kelią pagal vartotojo įvestį."""
    folder = input("Įveskite naują aplanko kelią: ").strip()
    
    # Patikrinti, ar aplankas egzistuoja
    if not Path(folder).exists():
        print("Aplankas neegzistuoja. Prašome įvesti teisingą kelią.")
        return None
    else:
        print(f"Aplankas nustatytas: {folder}")
        return folder


#  PALEIDIMAS

def main():
    print("Sveiki! Cia - jusu asmenine failu tvarkykle.")
    folder = get_folder()

    while True:
        print_menu()
        choice = input("Pasirinkite veiksma (1-13): ").strip()

        if choice == '1':
            print("Pasalinimo rezimas:")
            name = input("Failo pavadinimas (arba Enter): ").strip() or None
            ext = input("Failo pletinys (pvz. .tmp) (arba Enter): ").strip() or None
            date_str = input("Data YYYY-MM-DD (arba Enter): ").strip()
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
            remove_files_by(name=name, extension=ext, date=date, folder=folder)

        elif choice == '2':
            sort_files_by_category(folder)

        elif choice == '3':
            count_files_per_category(folder)

        elif choice == '4':
            remove_empty_dirs(folder)

        elif choice == '5':
            top = input("Kiek didziausiu failu rodyti? [5]: ").strip()
            analyze_files_by_size(folder, top_n=int(top) if top.isdigit() else 5)

        elif choice == '6':
            auto_subcategorize(folder)

        elif choice == '7':
            name = input("Archyvo pavadinimas [.zip]: ").strip() or "archyvas.zip"
            create_archive_copy(folder, archive_name=name)

        elif choice == '8':
            run_auto(folder)

        elif choice == '9':
            name = input("Failo pavadinimas (arba Enter): ").strip() or None
            ext = input("Failo pletinys (arba Enter): ").strip() or None
            date_str = input("Data YYYY-MM-DD (arba Enter): ").strip()
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
            preview_deletable_files(name=name, extension=ext, date=date, folder=folder)

        elif choice == '10':
            prefix = input("Pervadinti failus su prefixu: ").strip() or 'renamed_'
            start = input("Nuo kurio indekso pradeti? (pvz. 1): ").strip()
            rename_files(folder, prefix=prefix, start_index=int(start) if start.isdigit() else 1)

        elif choice == '11':
            min_mb = input("Koks minimalus failo dydis MB? [1]: ").strip()
            remove_files_smaller_than(folder, min_mb=int(min_mb) if min_mb.isdigit() else 1)

        elif choice == '12':
            category_sizes(folder)

        elif choice == '13':
            # Leisti vartotojui pakeisti aplanką
            folder = change_folder()
            if folder is None:
                print("Bandykite dar kartą su teisingu keliu.")
            else:
                print(f"Aplanko kelias pakeistas į: {folder}")

        elif choice == '14':
            print("Iseinate. Iki!")
            break



if __name__ == "__main__":
    main()
