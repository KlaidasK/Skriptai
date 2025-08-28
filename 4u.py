import os
import sys
import stat
import datetime
import getpass
import platform

LOG_FILE = "search_log.txt"  # Failas, kuriame saugomi paieškų logai
DELIMITER = "####"           # Skirtukas tarp rezultatų

def get_owner(path):
    try:
        if platform.system() == 'Windows':  # Naudoja Windows API kad gauti failo savininką
            import ctypes
            import ctypes.wintypes

            GetFileSecurity = ctypes.windll.advapi32.GetFileSecurityW
            GetSecurityDescriptorOwner = ctypes.windll.advapi32.GetSecurityDescriptorOwner
            LookupAccountSid = ctypes.windll.advapi32.LookupAccountSidW

            OWNER_SECURITY_INFORMATION = 1
            name = ctypes.create_unicode_buffer(1024)
            domain = ctypes.create_unicode_buffer(1024)
            sid_name_use = ctypes.wintypes.DWORD()
            sid = ctypes.create_string_buffer(1024)
            size = ctypes.wintypes.DWORD(1024)

            # Gauna Saugumo informaciją
            GetFileSecurity(path, OWNER_SECURITY_INFORMATION, sid, 1024, ctypes.byref(size))
            owner_sid = ctypes.c_void_p()
            GetSecurityDescriptorOwner(sid, ctypes.byref(owner_sid), ctypes.byref(ctypes.wintypes.BOOL()))

            # Verčia SID į naudotojo vardą
            LookupAccountSid(None, owner_sid, name, ctypes.byref(ctypes.wintypes.DWORD(1024)),
                             domain, ctypes.byref(ctypes.wintypes.DWORD(1024)), ctypes.byref(sid_name_use))

            return f"{domain.value}\\{name.value}"
        else:
            import pwd
            return pwd.getpwuid(os.stat(path).st_uid).pw_name
    except:
        return getpass.getuser()

def get_file_info(path):
    try:
        stats = os.stat(path)
        owner = get_owner(path)
        created = datetime.datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        accessed = datetime.datetime.fromtimestamp(stats.st_atime).strftime("%Y-%m-%d %H:%M:%S")
        
        # Grąžina informaciją apie failą ar katalogą
        return {
            "path": path,
            "name": os.path.basename(path),
            "owner": owner,
            "created": created,
            "accessed": accessed
        }
    except Exception as e:
        return {"error": str(e)}

def search(name_part):
    result_lines = []
    for root, dirs, files in os.walk(".", topdown=True): # Eina per visus katalogus ir failus pradedant nuo esamos direktorijos
        for name in dirs + files:
            if name_part.lower() in name.lower():
                full_path = os.path.join(root, name)
                info = get_file_info(full_path)
                if "error" in info:
                    continue
                # Jei tai failas
                if os.path.isfile(full_path):
                    result_lines.append("File:")
                    result_lines.append(f"Name: {info['name']}")
                    result_lines.append(f"Path: {info['path']}")
                    result_lines.append(f"Owner: {info['owner']}")
                    result_lines.append(f"Created: {info['created']}")
                # Jei tai katalogas
                elif os.path.isdir(full_path):
                    result_lines.append("Directory:")
                    result_lines.append(f"Path: {info['path']}")
                    try:
                        contents = os.listdir(full_path)
                        result_lines.append("Contents (one level):")
                        for item in contents:
                            result_lines.append(f"  - {item}")
                    except Exception as e:
                        result_lines.append(f"  Error reading contents: {e}")
                    result_lines.append(f"Owner: {info['owner']}")
                    result_lines.append(f"Created: {info['created']}")
                # Prideda skirtuką tarp rezultatų
                result_lines.append(DELIMITER)
    return result_lines

def log_search(search_term, results):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"Call Date: {datetime.datetime.now()}\n")  # Data/laikas
        f.write(f"Search Term: {search_term}\n")            # Paieškos žodis
        f.write("Results:\n")
        for line in results:
            f.write(line + "\n")                            # Visi rezultatai po vieną eilutę
        f.write(DELIMITER * 2 + "\n\n")                     # Dvigubas skirtukas pabaigoje


def main():
    if len(sys.argv) != 2:
        print("Usage: python search.py <file_or_directory_name_or_part>")
        sys.exit(1)

    search_term = sys.argv[1]                # Paima argumentą iš vartotojo
    results = search(search_term)            # Atlieka paiešką

    if results:
        for line in results:
            print(line)                      # Spausdina rezultatą vartotojui
    else:
        print("No matching files or directories found.")

    log_search(search_term, results if results else ["No matches found."])  # Įrašo į log'ą

if __name__ == "__main__":
    main()

