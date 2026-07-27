import json
import os
import sys
from datetime import datetime

def _get_data_dir():
    if getattr(sys, 'frozen', False):
        exec_dir = os.path.dirname(sys.executable)
        if "Contents/MacOS" in exec_dir:
            # Su macOS inside .app bundle, salva nella cartella utente ~/LeadScoutData
            user_data = os.path.expanduser("~/LeadScoutData")
            return os.path.join(user_data, "data")
        return os.path.join(exec_dir, "data")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

DATA_DIR = _get_data_dir()
CRM_FILE = os.path.join(DATA_DIR, "crm_leads.json")

def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CRM_FILE):
        with open(CRM_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)

def get_all_crm_leads():
    _ensure_data_dir()
    try:
        with open(CRM_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading CRM file: {e}")
        return {}

def update_crm_lead(lead_id, status=None, notes=None, biz_data=None):
    _ensure_data_dir()
    leads = get_all_crm_leads()

    if lead_id not in leads:
        leads[lead_id] = {
            "lead_id": lead_id,
            "status": "new",
            "notes": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "biz_data": biz_data or {}
        }

    if status is not None:
        leads[lead_id]["status"] = status
    if notes is not None:
        leads[lead_id]["notes"] = notes
    if biz_data is not None:
        leads[lead_id]["biz_data"] = biz_data

    leads[lead_id]["updated_at"] = datetime.now().isoformat()

    try:
        with open(CRM_FILE, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving CRM lead: {e}")
        return False
