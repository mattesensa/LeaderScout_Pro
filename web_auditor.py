import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.parse
from datetime import datetime

CURRENT_YEAR = datetime.now().year

def audit_website(url_input):
    """
    Audits a website for key lead-generation criteria:
    - Missing website
    - Insecure HTTP
    - Non-responsive layout
    - Outdated HTML tags / old design / old copyright
    - Slow speed / connectivity errors
    - Scraped email addresses
    """
    if not url_input or not isinstance(url_input, str) or url_input.strip() == "":
        return {
            "has_website": False,
            "url": "",
            "opportunity_score": 100,
            "opportunity_level": "CRITICAL",
            "status_label": "🔴 Nessun Sito Web",
            "is_http_only": False,
            "is_responsive": False,
            "is_outdated_design": False,
            "load_time_sec": 0,
            "issues": [
                "Nessun sito web presente su Google/OSM",
                "L'attività perde clienti che cercano online su Google"
            ],
            "emails_found": []
        }

    url = url_input.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    issues = []
    opportunity_score = 30
    is_http_only = False
    is_responsive = True
    is_outdated_design = False
    emails_found = []
    facebook_url = ""
    instagram_url = ""
    load_time = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    start_time = time.time()
    response = None
    final_url = url
    status_code = None

    try:
        response = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
        load_time = round(time.time() - start_time, 2)
        status_code = response.status_code
        final_url = response.url
    except requests.exceptions.SSLError:
        # Fallback to HTTP if HTTPS fails
        if url.startswith("https://"):
            http_url = url.replace("https://", "http://")
            try:
                start_time = time.time()
                response = requests.get(http_url, headers=headers, timeout=8, allow_redirects=True)
                load_time = round(time.time() - start_time, 2)
                status_code = response.status_code
                final_url = response.url
                is_http_only = True
                issues.append("Certificato SSL mancante o non valido (Errore HTTPS)")
                opportunity_score += 35
            except Exception:
                pass
        if not response:
            return {
                "has_website": True,
                "url": url,
                "opportunity_score": 90,
                "opportunity_level": "CRITICAL",
                "status_label": "🔴 Errore Connessione / SSL Errato",
                "is_http_only": True,
                "is_responsive": False,
                "is_outdated_design": True,
                "load_time_sec": 0,
                "issues": ["Impossibile stabilire una connessione sicura (SSL Errato / Sito offline)"],
                "emails_found": []
            }
    except Exception as e:
        return {
            "has_website": True,
            "url": url,
            "opportunity_score": 90,
            "opportunity_level": "CRITICAL",
            "status_label": "🔴 Sito Non Raggiungibile",
            "is_http_only": True,
            "is_responsive": False,
            "is_outdated_design": True,
            "load_time_sec": 0,
            "issues": [f"Sito non raggiungibile o dominio scaduto ({str(e)[:40]})"],
            "emails_found": []
        }

    # Check HTTP vs HTTPS
    if final_url.startswith("http://") and not final_url.startswith("https://"):
        is_http_only = True
        issues.append("Sito su HTTP non sicuro (Google segnala 'Non sicuro' nel browser)")
        opportunity_score += 25

    if status_code and status_code >= 400:
        issues.append(f"Il sito restituisce un errore HTTP {status_code} (Pagina non trovata o Errore Server)")
        opportunity_score += 40

    if load_time > 3.0:
        issues.append(f"Caricamento molto lento ({load_time}s)")
        opportunity_score += 15

    # HTML Analysis using BeautifulSoup
    html_content = response.text if response else ""
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Email Scraping
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    raw_emails = set(re.findall(email_pattern, html_content))
    # Filter out common false positives (images, fonts, example.com)
    for em in raw_emails:
        em_lower = em.lower()
        if not any(bad in em_lower for bad in [".png", ".jpg", "example.com", "domain.com", "sentry", "bootstrap", "wix"]):
            emails_found.append(em)

    # 2. Viewport / Mobile responsiveness check
    viewport_tag = soup.find("meta", attrs={"name": re.compile(r"viewport", re.I)})
    if not viewport_tag:
        is_responsive = False
        issues.append("Manca la configurazione Mobile Responsive (Non ottimizzato per Smartphone)")
        opportunity_score += 25

    # 3. Outdated / Old-style design indicators
    outdated_signals = []

    # a. Deprecated HTML tags
    deprecated_tags = ["font", "center", "marquee", "frameset", "frame", "basefont", "applet"]
    found_deprecated = [tag for tag in deprecated_tags if soup.find(tag)]
    if found_deprecated:
        outdated_signals.append(f"Uso di tag HTML obsoleti ({', '.join(found_deprecated)})")

    # b. Table-based layout check
    tables = soup.find_all("table")
    if len(tables) > 2:
        # Check if tables contain layout structural elements
        for t in tables:
            if t.get("width") or t.get("bgcolor") or t.get("cellspacing"):
                outdated_signals.append("Struttura del sito basata su vecchie tabelle HTML")
                break

    # c. Copyright year scan in footer or text
    page_text = soup.get_text()
    copyright_matches = re.findall(r'(?:copyright|©|\(c\))\s*(?:20\d\d|19\d\d)', page_text, re.I)
    old_years = []
    for match in copyright_matches:
        year_num = int(re.search(r'\d{4}', match).group())
        if year_num < (CURRENT_YEAR - 3):
            old_years.append(year_num)
    if old_years:
        oldest = min(old_years)
        outdated_signals.append(f"Copyright/Aggiornamento datato (Anno {oldest})")

    # d. Deprecated script / jQuery 1.x or Flash
    scripts = soup.find_all("script", src=True)
    for sc in scripts:
        src = sc["src"].lower()
        if "jquery-1." in src or "jquery.min.js?ver=1." in src or "jquery-2." in src:
            outdated_signals.append("Librerie JavaScript molto vecchie (jQuery 1.x/2.x del 2012-2015)")
            break
        if ".swf" in src:
            outdated_signals.append("Uso di elementi Adobe Flash (non più supportati)")
            break

    # e. Missing OpenGraph & Favicon
    og_title = soup.find("meta", property="og:title")
    favicon = soup.find("link", rel=re.compile(r"icon", re.I))
    if not og_title and not favicon:
        outdated_signals.append("Mancanza di Meta Tag moderni e Favicon per social e Google")

    # 4. Social Links Scraping (Instagram & Facebook)
    fb_link = soup.find("a", href=re.compile(r"facebook\.com", re.I))
    ig_link = soup.find("a", href=re.compile(r"instagram\.com", re.I))
    if fb_link and fb_link.get("href"):
        facebook_url = fb_link["href"]
    if ig_link and ig_link.get("href"):
        instagram_url = ig_link["href"]

    if outdated_signals:
        is_outdated_design = True
        issues.extend(outdated_signals)
        opportunity_score += 25

    # Clamp score between 1 and 100
    opportunity_score = min(max(opportunity_score, 15), 100)

    # Determine status level
    if opportunity_score >= 80:
        opportunity_level = "CRITICAL"
        status_label = "🔴 Alta Opportunità (Sito Obsoleto / Problematico)"
    elif opportunity_score >= 55:
        opportunity_level = "HIGH"
        status_label = "🟡 Media Opportunità (Design Datato / Non Responsive)"
    elif opportunity_score >= 40:
        opportunity_level = "MEDIUM"
        status_label = "🟡 Da Rimodernare"
    else:
        opportunity_level = "LOW"
        status_label = "🟢 Sito Moderno"

    return {
        "has_website": True,
        "url": final_url,
        "opportunity_score": opportunity_score,
        "opportunity_level": opportunity_level,
        "status_label": status_label,
        "is_http_only": is_http_only,
        "is_responsive": is_responsive,
        "is_outdated_design": is_outdated_design,
        "load_time_sec": load_time,
        "issues": issues,
        "emails_found": list(set(emails_found))[:3],
        "facebook_url": facebook_url,
        "instagram_url": instagram_url
    }
