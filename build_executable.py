import os
import sys
import subprocess
import shutil

# Force stdout/stderr UTF-8 encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("==================================================")
    print(" [LeadScout PRO] - Builder Eseguibile Standalone")
    print("==================================================")

    # 1. Install pyinstaller if not present
    try:
        import PyInstaller
        print("[+] PyInstaller trovato.")
    except ImportError:
        print("[*] Installazione di PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Clean previous build artifact directories
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f"[*] Pulizia della cartella {folder}...")
            shutil.rmtree(folder)

    # 3. Run PyInstaller build
    print("\n[*] Compilazione in corso con PyInstaller...")
    cmd = [sys.executable, "-m", "PyInstaller", "leadscout.spec", "--clean"]
    res = subprocess.run(cmd)

    if res.returncode == 0:
        print("\n[SUCCESS] Compilazione completata con successo!")
        print(f"[+] L'eseguibile si trova in: {os.path.abspath('dist')}")
        
        # Package ZIP (creato all'esterno di dist per evitare la ricorsione infinita)
        dist_dir = os.path.abspath("dist")
        system_name = "Windows" if sys.platform == "win32" else ("macOS" if sys.platform == "darwin" else "Linux")
        zip_name = f"LeadScoutPRO_{system_name}"
        temp_zip_base = os.path.abspath(zip_name)
        
        if os.path.exists(f"{temp_zip_base}.zip"):
            os.remove(f"{temp_zip_base}.zip")

        created_zip = shutil.make_archive(temp_zip_base, 'zip', dist_dir)
        
        # Sposta lo ZIP dentro dist solo a creazione ultimata
        final_zip_path = os.path.join(dist_dir, f"{zip_name}.zip")
        shutil.move(created_zip, final_zip_path)
        print(f"[+] Pacchetto ZIP creato: {final_zip_path}")
    else:
        print("\n[ERROR] Errore durante la compilazione.")

if __name__ == "__main__":
    run()
