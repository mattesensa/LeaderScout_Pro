from flask import Flask, render_template, request, jsonify
from overpass_client import fetch_businesses_from_osm, CATEGORY_OSM_MAPPING
from web_auditor import audit_website
from pitch_generator import generate_pitch
from crm_store import get_all_crm_leads, update_crm_lead
import concurrent.futures
import re

app = Flask(__name__)

def generate_lead_id(name, city):
    """Generates a stable, unique lead ID based on name and city."""
    raw = f"{name}_{city}".lower()
    return re.sub(r'[^a-z0-9_]', '', raw)

@app.route("/")
def index():
    categories = list(CATEGORY_OSM_MAPPING.keys())
    return render_template("index.html", categories=categories)

@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.json or {}
    city = data.get("city", "").strip()
    category = data.get("category", "tutti").strip()

    if not city:
        return jsonify({"error": "Inserisci il nome di una città o comune."}), 400

    # 1. Fetch businesses from OSM + Web Directory
    osm_res = fetch_businesses_from_osm(city, category=category, max_results=50)
    if "error" in osm_res:
        return jsonify({"error": osm_res["error"]}), 400

    businesses = osm_res["businesses"]
    crm_leads = get_all_crm_leads()

    # 2. Audit websites in parallel
    def process_business(biz):
        website = biz.get("website", "")
        audit_res = audit_website(website)

        biz_result = dict(biz)
        biz_result.update(audit_res)

        if not biz_result.get("email") and audit_res.get("emails_found"):
            biz_result["email"] = audit_res["emails_found"][0]

        # Generate unique Lead ID
        lead_id = generate_lead_id(biz_result["name"], biz_result["city"])
        biz_result["lead_id"] = lead_id

        # Attach CRM data if already saved
        if lead_id in crm_leads:
            biz_result["crm_status"] = crm_leads[lead_id].get("status", "new")
            biz_result["crm_notes"] = crm_leads[lead_id].get("notes", "")
        else:
            biz_result["crm_status"] = "new"
            biz_result["crm_notes"] = ""

        return biz_result

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        audited_businesses = list(executor.map(process_business, businesses))

    audited_businesses.sort(key=lambda x: x.get("opportunity_score", 0), reverse=True)

    total = len(audited_businesses)
    no_website_count = sum(1 for b in audited_businesses if not b.get("has_website"))
    outdated_or_insecure_count = sum(1 for b in audited_businesses if b.get("has_website") and (b.get("is_outdated_design") or b.get("is_http_only") or not b.get("is_responsive")))
    critical_count = sum(1 for b in audited_businesses if b.get("opportunity_score", 0) >= 80)

    return jsonify({
        "city": osm_res["city"],
        "count": total,
        "metrics": {
            "total": total,
            "no_website": no_website_count,
            "outdated_or_insecure": outdated_or_insecure_count,
            "critical_opportunity": critical_count
        },
        "results": audited_businesses
    })

@app.route("/api/crm", methods=["GET"])
def api_get_crm():
    crm_leads = get_all_crm_leads()
    return jsonify(list(crm_leads.values()))

@app.route("/api/crm/update", methods=["POST"])
def api_update_crm():
    data = request.json or {}
    lead_id = data.get("lead_id")
    status = data.get("status")
    notes = data.get("notes")
    biz_data = data.get("biz_data")

    if not lead_id:
        return jsonify({"error": "Lead ID mancante."}), 400

    success = update_crm_lead(lead_id, status=status, notes=notes, biz_data=biz_data)
    if success:
        return jsonify({"message": "CRM aggiornato con successo!", "lead_id": lead_id})
    else:
        return jsonify({"error": "Errore durante il salvataggio del CRM."}), 500

@app.route("/api/audit-single", methods=["POST"])
def api_audit_single():
    data = request.json or {}
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "Inserisci un URL valido."}), 400

    res = audit_website(url)
    return jsonify(res)

@app.route("/api/pitch", methods=["POST"])
def api_pitch():
    data = request.json or {}
    name = data.get("name", "Attività")
    city = data.get("city", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    website = data.get("website", "")
    audit = data.get("audit", {})

    pitch_data = generate_pitch(name, city, phone, email, website, audit)
    return jsonify(pitch_data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
