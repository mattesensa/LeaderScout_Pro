# 📦 Guida alla Distribuzione & Build Eseguibili (Windows & macOS)

Questo progetto include tutto il necessario per impacchettare **LeadScout PRO** in un **eseguibile desktop standalone**, che funziona senza bisogno di installare Python sul computer finale.

---

## 🚀 Come Funziona l'Eseguibile

Quando l'utente avvia l'eseguibile (`LeadScoutPRO.exe` su Windows o `LeadScoutPRO.app` / binario su macOS):
1. Avvia in background il server locale sulla porta `5000`.
2. Apre **in automatico** il browser predefinito all'indirizzo `http://127.0.0.1:5000`.
3. Tutti i dati salvati nel CRM rimangono salvati nella cartella `data/crm_leads.json` (su macOS nella cartella `~/LeadScoutData/data`).

---

## 🛠️ Come Compilare l'Eseguibile

### Opzione 1: Compilazione Locale (Windows)
Se sei su Windows, puoi compilare direttamente eseguendo nel terminale:

```bash
python build_executable.py
```

Al termine troverai il pacchetto pronto ed impacchettato in `.zip` nella cartella:
👉 `dist/LeadScoutPRO_Windows.zip`

---

### Opzione 2: Compilazione Cross-Platform per macOS & Windows via GitHub Actions (Automatica)
PyInstaller genera eseguibili per il sistema operativo su cui viene lanciato. 
Per ottenere l'eseguibile nativo per **macOS** (`.app` o binario Mac) anche se ti trovi su un PC Windows, abbiamo configurato **GitHub Actions**:

1. Carica/Fai il push del codice sul tuo repository GitHub.
2. Vai nella scheda **Actions** del tuo repository su GitHub.
3. Seleziona **Build Cross-Platform Executables (Windows & macOS)** e clicca **Run workflow**.
4. GitHub compilerà automaticamente l'applicazione sui propri server sia per **Windows** che per **macOS** (Intel & Apple Silicon M1/M2/M3).
5. Potrai scaricare il file `.zip` pronto sia per Mac che per Windows direttamente dagli artifact della build!

---

## 📁 Struttura dei File di Build

- `desktop_launcher.py`: Launcher che avvia il server Flask e apre la finestra del browser.
- `leadscout.spec`: File di configurazione PyInstaller (include HTML, CSS, JS e risorse).
- `build_executable.py`: Script 1-click per pulire le cartelle temporanee e creare lo ZIP di rilascio.
- `.github/workflows/build_executables.yml`: Workflow per compilare automaticamente su GitHub per Mac e Windows.
