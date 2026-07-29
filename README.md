# 🚀 LeadScout PRO - Prospezione Commerciale & Audit Siti Web Locali

**LeadScout PRO** è un software completo che automatizza la ricerca di clienti e attività commerciali sul territorio. Analizza la presenza online delle attività (sito web mancante, non sicuro HTTPS, grafica datata o non responsive), genera pitch commerciali personalizzati e permette di gestire i lead tramite un CRM integrato.

---

## 🌟 Funzionalità Principali

- 🔍 **Ricerca Territoriale Ibrida**: Trova le attività commerciali in qualsiasi città o comune con filtri rigorosi per evitare risultati nei comuni limitrofi.
- ⚡ **Audit Automatico Siti Web**:
  - Verifica la presenza del sito web.
  - Controlla la sicurezza (HTTPS vs HTTP).
  - Analizza il design responsive per dispositivi mobili.
  - Identifica siti datati/inattivi e trova automaticamente le email di contatto.
- 🎯 **Opportunity Score**: Calcola un punteggio da 0 a 100 per identificare i clienti con il più alto potenziale di vendita.
- 📝 **Pitch Generator**: Genera automaticamente bozze di email o messaggi commerciali su misura per l'attività selezionata.
- 📊 **CRM Integrato**: Salva e aggiorna lo stato dei lead (*Nuovo*, *Contattato*, *In Trattativa*, *Cliente*, *Non Interessato*) con note personalizzate.

---

## 💻 Come Usare l'Applicazione

Puoi utilizzare **LeadScout PRO** su **Windows** e su **macOS** scegliendo la modalità più adatta a te:

### 🍏 Su macOS (Apple Mac)

#### Opzione 1: Avvio Rapido (con Python) — *Consigliata*
1. Scarica o clona questo repository su Mac.
2. Fai **doppio clic** sul file `start_mac.command`.
3. Il programma verificherà le dipendenze e aprirà automaticamente il browser su `http://127.0.0.1:5000`.

> **Nota per macOS**: La prima volta che apri `start_mac.command`, fai **Tasto Destro** (o `Ctrl` + Clic) sul file e seleziona **Apri** per autorizzare l'esecuzione da parte di macOS.

#### Opzione 2: Eseguibile Standalone Mac (Senza Python)
1. Vai nella sezione **Actions** del repository GitHub.
2. Scarica il file `LeadScoutPRO-macOS.zip` dagli **Artifacts**.
3. Estrarre il file ZIP e fare doppio clic sull'applicazione.

---

### 🪟 Su Windows

#### Opzione 1: Eseguibile Standalone `.exe`
1. Scarica o estrai il pacchetto `dist/LeadScoutPRO_Windows.zip` (o scaricalo dagli **Artifacts** di GitHub Actions).
2. Fa doppio clic su **`LeadScoutPRO.exe`**.
3. Si aprirà la console di supporto e il tuo browser predefinito si aprirà automaticamente su `http://127.0.0.1:5000`.

#### Opzione 2: Da Terminale (Python)
1. Apri il prompt dei comandi nella cartella del progetto.
2. Esegui:
   ```bash
   pip install -r requirements.txt
   python desktop_launcher.py
   ```

---

## 🛠️ Per gli Sviluppatori: Compilazione Eseguibili

Per generare i pacchetti eseguibili standalone per Windows e Mac:

### Compilazione Locale (Windows)
```bash
python build_executable.py
```
Il pacchetto `.zip` finale verrà creato in `dist/LeadScoutPRO_Windows.zip`.

### Compilazione Automatica Cross-Platform (GitHub Actions)
Il repository include il workflow `.github/workflows/build_executables.yml`.
Ogni volta che fai un `push` o avvii manualmente il workflow da GitHub Actions, i server di GitHub compileranno automaticamente gli eseguibili sia per **Windows** che per **macOS**.

---

## 📁 Struttura del Progetto

- `app.py`: Server Flask e API principali.
- `desktop_launcher.py`: Launcher desktop con apertura automatica del browser.
- `start_mac.command`: Script 1-click di avvio rapido per utenti macOS.
- `web_auditor.py`: Motore di scansione e analisi siti web.
- `overpass_client.py`: Integrazione OpenStreetMap e directory per la prospezione.
- `crm_store.py`: Gestore del database CRM locale (`data/crm_leads.json`).
- `pitch_generator.py`: Generatore di proposte commerciali.
- `build_executable.py`: Builder PyInstaller.
