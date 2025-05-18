import requests
import streamlit as st

def enrich_iocs(iocs):
    enriched = []
    vt_api_key = st.secrets.get("VIRUSTOTAL_API_KEY", "")
    abuse_ipdb_key = st.secrets.get("ABUSEIPDB_API_KEY", "")

    for ioc in iocs:
        info = {"ioc": ioc, "type": "IP" if "." in ioc else "Executable", "reputation": "Unknown"}
        if "." in ioc and abuse_ipdb_key:
            try:
                response = requests.get("https://api.abuseipdb.com/api/v2/check",
                    headers={"Key": abuse_ipdb_key, "Accept": "application/json"},
                    params={"ipAddress": ioc, "maxAgeInDays": "90"})
                data = response.json()
                info["reputation"] = data.get("data", {}).get("abuseConfidenceScore", "Unknown")
            except: pass
        if vt_api_key:
            try:
                headers = {"x-apikey": vt_api_key}
                url = f"https://www.virustotal.com/api/v3/ip_addresses/{ioc}" if "." in ioc else f"https://www.virustotal.com/api/v3/files/{ioc}"
                response = requests.get(url, headers=headers)
                vt_data = response.json()
                info["vt_score"] = vt_data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            except: pass
        enriched.append(info)
    return enriched
