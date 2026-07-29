# Walkthrough & Guida Utente: LeadScout PRO

Abbiamo sviluppato ed eseguito con successo **LeadScout**, un software completo con Dashboard Web per automatizzare la ricerca di clienti locali che non hanno un sito web o che hanno un sito con un **design datato/obsoleto** o senza certificato di sicurezza HTTPS.

---

## 🚀 Come Accedere al Programma

Il server locale è **già attivo e funzionante** sul tuo computer al seguente indirizzo:

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

*(Puoi aprire questo link in qualsiasi browser come Chrome, Edge o Firefox).*

---

## 🔥 Funzionalità Implementate

### 1. Motore di Ricerca Ibrido a Copertura Totale (PagineGialle + OpenStreetMap)
- **Filtro Rigoroso della Città (Anti-Comuni Limitrofi)**: Esclude rigorosamente i risultati appartenenti a paesi o frazioni confinanti (es. *Montepulciano, Cetona, Sarteano*) che le directory inserivano sotto "Nei dintorni". Ora compaiono **solo ed esclusivamente** le attività fisicamente presenti nel comune cercato.
- **Filtro Rigoroso della Categoria (Zero Falsi Positivi)**: Quando cerchi *"Parrucchieri"*, il sistema convalida ogni singolo risultato verificando la presenza di parole chiave pertinenti. Vengono eliminati del tutto idraulici, elettricisti o altre professioni non correlate.
- **Recupero di Tutti i Negozi Reali**: Rileva le 11 attività reali e storiche di Chianciano Terme (*Un Diavolo per Capello, Barbiere Franco Brilli, Coiffeur Sandro, Equipe 2000, Fuori di Testa, Punto Donna, Hair Studio, ecc.*).
- **Link Google Maps diretti ad Alta Precisione**: Genera `https://www.google.com/maps/search/?api=1&query=[Nome] + [Indirizzo Via] + [Città]` per aprire al primo click la scheda esatta dell'attività su Google Maps.

### 2. Mini-CRM & Pipeline di Vendita Integrata (Salvataggio Persistente)
- **Gestione Stato Trattativa per Ogni Lead**: Per ciascuna attività puoi impostare e cambiare in tempo reale lo stato della trattativa:
  - 🔴 *Da Contattare*
  - 🟡 *Messaggio Inviato*
  - 🔵 *In Trattativa / Appuntamento*
  - 🟢 *Cliente Acquisito!*
  - ❌ *Non Interessato*
- **Registro Note Personali (Promemoria)**: Cliccando sull'icona 📝 puoi inserire e salvare note sul cliente (*es. "Titolare si chiama Elena, richiamare giovedì"*). Le note e gli stati vengono **salvati in automatico** sul tuo computer nel file `data/crm_leads.json`.
- **Scheda "I Miei Lead Saved (CRM)"**: Un nuovo tab dedicato in alto ti permette di consultare in qualsiasi momento tutti i clienti salvati e lo stato della tua pipeline di vendita.

### 3. Rilevamento Canali Social (Instagram & Facebook)
- **Scansione Profili Social**: Durante l'audit, il programma individua i link ufficiali ai profili **Instagram** e **Facebook** dell'attività.
- **Identificazione Target d'Oro**: Trovare un'attività con Instagram/Facebook attivi ma **senza sito web** segnala un cliente ideale, che già investe nella comunicazione e ha budget disponibile.

### 4. Invio Diretto a 1-Click su WhatsApp Web ed Email
- Nel modale di Pitch, cliccando su **"💬 Apri subito WhatsApp Web"**, il browser apre immediatamente la chat di WhatsApp Web con il messaggio personalizzato già pre-compilato.
- Cliccando su **"✉️ Apri Client Email"**, viene aperto il tuo programma di posta con l'oggetto e il corpo dell'email già pronti per l'invio.

### 3. Generatore di Pitch Personalizzato (1-Click Copy)
Cliccando sul pulsante **⚡ Pitch** accanto a qualsiasi attività, LeadScout analizza i problemi specifici di quel negozio e genera all'istante:
- **WhatsApp Pitch**: Messaggio informale e diretto pronto per l'invio rapido da smartphone.
- **Cold Email Pitch**: Email strutturata con l'indicazione precisa delle criticità rilevate nel loro sito.
- **Script Telefonico**: Guida passo-passo da seguire per una chiamata a freddo ad alta conversione.

### 4. Esportazione dei Lead in CSV
- È possibile esportare tutti i risultati trovati (con telefoni, email, siti web, punteggi e problemi rilevati) in un file **CSV compatibile con Excel**.

---

## 🛠️ Come Avviare LeadScout in Futuro

Se in futuro riavvii il computer, ti basterà aprire il terminale nella cartella `muccia` ed eseguire:

```bash
python app.py
```

E poi aprire nel browser l'indirizzo `http://127.0.0.1:5000`.

---

## 📁 File del Progetto Creati

- [app.py](file:///c:/Users/admloc/Desktop/muccia/app.py) (Server Flask e Gestione API)
- [overpass_client.py](file:///c:/Users/admloc/Desktop/muccia/overpass_client.py) (Estrattore OpenStreetMap)
- [web_auditor.py](file:///c:/Users/admloc/Desktop/muccia/web_auditor.py) (Scanners ed Audit del design obsoleto)
- [pitch_generator.py](file:///c:/Users/admloc/Desktop/muccia/pitch_generator.py) (Generatore di messaggi di vendita)
- [templates/index.html](file:///c:/Users/admloc/Desktop/muccia/templates/index.html) (Interfaccia Dashboard Web)
- [static/css/style.css](file:///c:/Users/admloc/Desktop/muccia/static/css/style.css) (Design Dark Mode & Glassmorphism)
- [static/js/main.js](file:///c:/Users/admloc/Desktop/muccia/static/js/main.js) (Logica frontend e chiamate AJAX)
