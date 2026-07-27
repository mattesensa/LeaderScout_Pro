def generate_pitch(business_name, city, phone, email, website, audit_data):
    """
    Generates personalized pitch scripts (WhatsApp, Email, Phone) based on the audit results.
    """
    has_website = audit_data.get("has_website", False)
    issues = audit_data.get("issues", [])
    issues_str = "\n".join([f"• {issue}" for issue in issues[:3]]) if issues else "• Grafica da rinnovare per attrarre nuovi clienti su mobile"

    # --- WHATSAPP PITCH ---
    if not has_website:
        wa_pitch = (
            f"Ciao! 👋 Ho visto che avete un'ottima attività ({business_name} a {city}), "
            f"ma su Google e Maps non risulta ancora un sito web ufficiale.\n\n"
            f"Oggi oltre il 70% delle persone cerca su smartphone prima di scegliere dove andare. "
            f"Siamo un team locale di sviluppatori web e stiamo preparando una bozza/anteprima gratuita del sito per {business_name}.\n\n"
            f"Ti andrebbe di darci un'occhiata senza alcun impegno? 🚀"
        )
    else:
        wa_pitch = (
            f"Ciao! 👋 Ho notato il sito di {business_name} ({website}).\n\n"
            f"Facendo un'analisi rapida per le attività di {city}, ho notato alcune cose che potrebbero farvi perdere clienti da smartphone:\n"
            f"{issues_str}\n\n"
            f"Stiamo realizzando dei restyling moderni e veloci per i negozi della zona. "
            f"Vi andrebbe di vedere una dimostrazione gratuita di come diventerbbe con una grafica aggiornata e moderna? 🎨"
        )

    # --- EMAIL PITCH ---
    if not has_website:
        email_subject = f"Proposta anteprima sito web per {business_name} ({city})"
        email_body = f"""Gentile team di {business_name},

Vi scrivo perché ho notato la vostra attività a {city}. Notando l'assenza di un sito web ufficiale collegato alla scheda Google, volevo farvi presente che molti potenziali clienti della zona vi stanno cercando online ma finiscono sui siti dei concorrenti.

Con il nostro team realizziamo siti web veloci, moderni e ottimizzati per smartphone specifici per la vostra categoria.

Cosa potremmo realizzare per voi:
• Presenza ufficiale su Google con menù/catalogo/servizi ben visibili
• Sistema di contatto rapido (tasto diretto WhatsApp / Chiamata / Mappa)
• Grafica d'impatto pensata per convertire i visitatori in clienti reali

Saremmo felici di mostrarvi una bozza grafica preliminare totalmente gratuita e senza alcun impegno.

Quando avreste 5 minuti per una rapida chiacchierata o una chiamata?

Cordiali saluti,
Il Team Web Dev
"""
    else:
        email_subject = f"Suggerimenti ottimizzazione e restyling per {website}"
        email_body = f"""Gentile team di {business_name},

Navigando su {website}, abbiamo riscontrato che la vostra presenza a {city} ha un ottimo potenziale, ma il sito attuale presenta alcuni aspetti critici che potrebbero penalizzarvi sui motori di ricerca e da mobile:

{issues_str}

Al giorno d'oggi, un sito datato o non ottimizzato per gli smartphone riduce la fiducia dei clienti e abbassa le conversioni.

Siamo uno studio specializzato nel restyling rapido di siti aziendali. Trasformiamo vecchi siti in piattaforme moderne, velocissime e perfettamente responsive.

Vi andrebbe se vi inviassimo un breve video-audit gratuito (60 secondi) con 3 consigli pratici per rimodernare il vostro sito?

In attesa di un vostro riscontro, vi auguro buon lavoro.

Cordiali saluti,
Il Team Web Dev
"""

    # --- PHONE SCRIPT ---
    phone_script = f"""1. PRESENTAZIONE: "Buongiorno, parlo con il responsabile di {business_name}?"
2. GANCIO: "Sono [Nome] di uno studio web locale. Vi chiamo perché stavo analizzando le attività di {city}..."
3. PROBLEMA: {"'...e ho notato che non avete ancora un sito web ufficiale su Google per ricevere clienti.'" if not has_website else "'...e ho notato che il vostro sito web ha qualche anno e da cellulare riscontra qualche rallentamento/problema di grafica.'"}
4. PROPOSTA: "Stiamo preparando un'anteprima gratuita di come apparirebbe il vostro nuovo sito moderno. Possiamo inviarvela su WhatsApp o via mail?"
5. CHIUSURA: "A quale numero/email posso inviarvi il link dell'anteprima?"
"""

    return {
        "whatsapp": wa_pitch,
        "email_subject": email_subject,
        "email_body": email_body,
        "phone_script": phone_script
    }
