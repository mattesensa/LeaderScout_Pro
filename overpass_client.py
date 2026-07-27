import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
]

CATEGORY_OSM_MAPPING = {
    "ristoranti": '["amenity"~"restaurant|fast_food|pizzeria|trattoria|osteria"]',
    "pizzerie": '["amenity"~"pizzeria"]',
    "bar": '["amenity"~"bar|cafe|pub"]',
    "parrucchieri": '["shop"~"hairdresser|barber"]',
    "estetica": '["shop"~"beauty|massage|spa"]',
    "dentisti": '["amenity"~"dentist|doctors"]',
    "abbigliamento": '["shop"~"clothes|fashion|boutique|shoes"]',
    "artigiani": '["craft"~"plumber|electrician|painter|carpenter"]',
    "meccanici": '["shop"~"car_repair|car|motorcycle"]',
    "hotel": '["tourism"~"hotel|guest_house|hostel|bed_and_breakfast"]',
    "tutti": '[~"amenity|shop|craft|tourism"~".*"]'
}

PG_CATEGORY_MAPPING = {
    "ristoranti": ["ristoranti", "pizzerie"],
    "pizzerie": ["pizzerie"],
    "bar": ["bar-caffe"],
    "parrucchieri": ["parrucchieri"],
    "estetica": ["centri-estetici"],
    "dentisti": ["dentisti"],
    "abbigliamento": ["abbigliamento-negozi"],
    "artigiani": ["idraulici", "elettricisti"],
    "meccanici": ["autofficine-centri-assistenza"],
    "hotel": ["alberghi"],
    "tutti": ["parrucchieri", "ristoranti", "bar-caffe", "centri-estetici", "alberghi", "abbigliamento-negozi", "autofficine-centri-assistenza"]
}

CATEGORY_KEYWORDS = {
    "parrucchieri": ["parrucchiere", "parrucchiera", "parrucchieri", "barbiere", "barberia", "coiffeur", "hair", "acconciature", "capelli", "stylist"],
    "ristoranti": ["ristorante", "pizzeria", "trattoria", "osteria", "fast food", "braceria", "tavola calda", "gastronomia", "food", "ristorazione"],
    "pizzerie": ["pizzeria", "pizze", "pizza"],
    "bar": ["bar", "caffè", "caffe", "pub", "birreria", "caffetteria", "chiosco"],
    "estetica": ["estetica", "estetico", "estetista", "massaggi", "spa", "benessere", "solarium", "beauty"],
    "dentisti": ["dentista", "dentistico", "odontoiatrico", "medico", "dottore", "studio medico"],
    "abbigliamento": ["abbigliamento", "boutique", "moda", "scarpe", "calzature", "outlet", "vestiti"],
    "artigiani": ["idraulico", "elettricista", "timbri", "falegname", "imbianchino", "fabbro", "caldaie", "artigiano"],
    "meccanici": ["meccanico", "carrozzeria", "autofficina", "gommista", "auto", "moto", "officina"],
    "hotel": ["hotel", "albergo", "b&b", "bed", "affittacamere", "residence", "agriturismo", "guest house"],
    "tutti": []
}

TAG_TRANSLATIONS = {
    "hairdresser": "Parrucchiere",
    "barber": "Barbiere / Barberia",
    "restaurant": "Ristorante",
    "pizzeria": "Pizzeria",
    "trattoria": "Trattoria / Osteria",
    "osteria": "Trattoria / Osteria",
    "bar": "Bar / Caffè",
    "cafe": "Caffetteria",
    "pub": "Pub / Birreria",
    "fast_food": "Fast Food / Takeaway",
    "beauty": "Centro Estetico",
    "massage": "Centro Massaggi / SPA",
    "spa": "Centro Benessere",
    "dentist": "Studio Dentistico",
    "doctors": "Studio Medico",
    "clothes": "Negozi di Abbigliamento",
    "fashion": "Boutique Moda",
    "shoes": "Calzature",
    "car_repair": "Meccanico / Carrozzeria",
    "plumber": "Idraulico",
    "electrician": "Elettricista",
    "hotel": "Hotel / Albergo",
    "guest_house": "Affittacamere",
    "bed_and_breakfast": "B&B"
}

GENERIC_AND_BRAND_NAMES = {
    "kérastase", "kerastase", "l'oréal", "loreal", "wella", "schwarzkopf", "matrix", "redken", "davines",
    "dhl", "sda", "tnt", "ups", "fedex", "gls", "brt", "amazon counter", "amazon locker",
    "western union", "moneygram", "ria money transfer", "sisal", "lottomatica", "mooney",
    "punti poste", "poste italiane", "tobacconist", "tobacconists",
    "barbiere", "parrucchiere", "parrucchiera", "parrucchieri", "salone", "salone da barba",
    "pizzeria", "ristorante", "trattoria", "osteria", "bar", "caffè", "caffe", "pub",
    "supermercato", "alimentari", "edicola", "tabacchi", "tabaccheria", "gelateria",
    "pasticceria", "panificio", "macelleria", "pescheria", "fruttivendolo", "farmacia",
    "parafarmacia", "lavanderia", "carrozzeria", "officina", "meccanico", "gommista",
    "fioraio", "fiorista", "chiosco", "distributore", "autolavaggio", "bancomat", "atm"
}

def clean_name(name):
    if not name:
        return ""
    cleaned = re.sub(r'\s+-\s+PagineGialle.*', '', name, flags=re.I)
    return cleaned.strip()

def is_valid_business_name(name):
    if not name or len(name.strip()) < 3:
        return False
    cl = name.strip().lower()
    if cl in GENERIC_AND_BRAND_NAMES:
        return False
    if cl.isdigit():
        return False
    return True

def is_matching_city(city_query, address_text):
    """Ensures the business is strictly located in the requested city, excluding neighboring towns."""
    if not address_text:
        return True
    
    city_words = [w.lower() for w in re.split(r'[\s,-]+', city_query) if len(w) > 2]
    addr_lower = address_text.lower()

    # Must contain at least one primary city word (e.g. "chianciano")
    for cw in city_words:
        if cw in addr_lower:
            return True
            
    return False

def is_matching_category(requested_category, business_cat, business_name):
    """Ensures the business actually belongs to the requested category (e.g. no plumbers when searching hairdressers)."""
    cat_key = requested_category.lower()
    keywords = CATEGORY_KEYWORDS.get(cat_key, [])
    if not keywords or cat_key == "tutti":
        return True

    text_to_check = f"{business_cat} {business_name}".lower()
    for kw in keywords:
        if kw in text_to_check:
            return True
            
    return False

def fetch_from_paginegialle(city_name, category="tutti", max_results=60):
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    pg_categories = PG_CATEGORY_MAPPING.get(category.lower(), ["parrucchieri", "ristoranti", "bar-caffe", "centri-estetici"])

    for cat_slug in pg_categories:
        url = f"https://www.paginegialle.it/ricerca/{cat_slug}/{urllib.parse.quote(city_name)}"
        try:
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code != 200:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            headers_divs = soup.find_all("div", class_=lambda c: c and "search-itm__header" in c)

            for header_div in headers_divs:
                h2 = header_div.find("h2")
                if not h2:
                    continue

                name = clean_name(h2.text)
                if not is_valid_business_name(name):
                    continue

                parent = header_div.parent
                adr_div = parent.find("div", class_=lambda c: c and "search-itm__adr" in c) if parent else None
                address = adr_div.text.strip() if adr_div else city_name

                # Strict City Check (Exclude neighboring towns like Montepulciano/Cetona)
                if not is_matching_city(city_name, address):
                    continue

                cat_div = parent.find("div", class_=lambda c: c and "search-itm__category" in c) if parent else None
                cat_label = cat_div.text.strip() if cat_div else category.capitalize()

                # Strict Category Check (Exclude irrelevant professions)
                if not is_matching_category(category, cat_label, name):
                    continue

                # Clean address formatting
                address_clean = re.sub(r'\s*-\s*\d{5}.*', '', address).strip()

                phone = ""
                tel_a = parent.find("a", href=re.compile(r"tel:", re.I)) if parent else None
                if tel_a:
                    phone = tel_a.text.strip() or tel_a["href"].replace("tel:", "").strip()

                full_query = f"{name}, {address_clean}" if address_clean and address_clean != city_name else f"{name}, {city_name}"
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(full_query)}"

                results.append({
                    "name": name,
                    "category": cat_label,
                    "phone": phone,
                    "website": "",
                    "email": "",
                    "address": address_clean,
                    "city": city_name,
                    "lat": None,
                    "lon": None,
                    "google_maps_url": google_maps_url
                })

                if len(results) >= max_results:
                    break
        except Exception as e:
            print(f"Error scraping PagineGialle for {cat_slug}: {e}")

        if len(results) >= max_results:
            break

    return results

def get_city_bounding_box(city_name):
    url = f"https://nominatim.openstreetmap.org/search?city={urllib.parse.quote(city_name)}&country=Italy&format=json&limit=1"
    headers = {"User-Agent": "LeadScout-WebDev-Finder/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200 and resp.json():
            data = resp.json()[0]
            lat = float(data["lat"])
            lon = float(data["lon"])
            bbox = data.get("boundingbox", [])
            if len(bbox) == 4:
                return {
                    "min_lat": float(bbox[0]),
                    "max_lat": float(bbox[1]),
                    "min_lon": float(bbox[2]),
                    "max_lon": float(bbox[3]),
                    "lat": lat,
                    "lon": lon,
                    "display_name": data.get("display_name", city_name).split(",")[0]
                }
    except Exception as e:
        print(f"Error fetching city info: {e}")
    return None

def fetch_from_osm(city_name, category="tutti", max_results=60):
    city_info = get_city_bounding_box(city_name)
    if not city_info:
        return []

    min_lat = city_info["min_lat"]
    max_lat = city_info["max_lat"]
    min_lon = city_info["min_lon"]
    max_lon = city_info["max_lon"]

    filter_tag = CATEGORY_OSM_MAPPING.get(category.lower(), '[~"amenity|shop|craft|tourism"~".*"]')

    query = f"""
    [out:json][timeout:20];
    (
      node{filter_tag}["name"]({min_lat},{min_lon},{max_lat},{max_lon});
      way{filter_tag}["name"]({min_lat},{min_lon},{max_lat},{max_lon});
    );
    out center body {max_results};
    """

    data = None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            response = requests.post(endpoint, data={"data": query}, headers={"User-Agent": "LeadScout/5.0"}, timeout=15)
            if response.status_code == 200:
                data = response.json()
                break
        except Exception:
            pass

    if not data or "elements" not in data:
        return []

    results = []

    for elem in data["elements"]:
        tags = elem.get("tags", {})
        raw_name = tags.get("name", "").strip()
        if not raw_name:
            continue

        sub_names = [n.strip() for n in raw_name.split(";") if n.strip()]

        for name in sub_names:
            if not is_valid_business_name(name):
                continue

            raw_cat = tags.get("shop") or tags.get("amenity") or tags.get("craft") or tags.get("tourism") or "Attività Commerciale"
            category_label = TAG_TRANSLATIONS.get(raw_cat.lower(), raw_cat.capitalize())

            # Strict Category Check for OSM results as well
            if not is_matching_category(category, category_label, name):
                continue

            lat = elem.get("lat") or elem.get("center", {}).get("lat")
            lon = elem.get("lon") or elem.get("center", {}).get("lon")

            phone = tags.get("phone") or tags.get("contact:phone") or tags.get("mobile") or tags.get("contact:mobile") or ""
            website = tags.get("website") or tags.get("contact:website") or tags.get("url") or ""
            email = tags.get("email") or tags.get("contact:email") or ""

            street = tags.get("addr:street", "").strip()
            housenumber = tags.get("addr:housenumber", "").strip()
            address = f"{street}, {housenumber}".strip(", ") if street else city_info["display_name"]

            full_query = f"{name}, {address}" if street else f"{name}, {city_info['display_name']}"
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(full_query)}"
            if lat and lon and not street:
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            results.append({
                "name": name,
                "category": category_label,
                "phone": phone,
                "website": website,
                "email": email,
                "address": address,
                "city": city_info["display_name"],
                "lat": lat,
                "lon": lon,
                "google_maps_url": google_maps_url
            })

    return results

def fetch_businesses_from_osm(city_name, category="tutti", max_results=80):
    """
    Hybrid Search Engine combining Local Web Directory (PagineGialle) + OpenStreetMap
    with Strict City Matching & Strict Category Validation.
    """
    pg_results = fetch_from_paginegialle(city_name, category=category, max_results=max_results)
    osm_results = fetch_from_osm(city_name, category=category, max_results=max_results)

    merged = []
    seen_normalized_names = set()

    for item in pg_results + osm_results:
        norm_key = re.sub(r'[^a-z0-9]', '', item["name"].lower())
        if not norm_key or norm_key in seen_normalized_names:
            continue

        is_dup = False
        for existing_key in seen_normalized_names:
            if norm_key in existing_key or existing_key in norm_key:
                if len(norm_key) > 5 and len(existing_key) > 5:
                    is_dup = True
                    break
        if is_dup:
            continue

        seen_normalized_names.add(norm_key)
        merged.append(item)

        if len(merged) >= max_results:
            break

    return {
        "city": city_name,
        "count": len(merged),
        "businesses": merged
    }
