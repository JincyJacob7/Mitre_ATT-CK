# 🛡️ Agentic Rule-to-MITRE ATT&CK Mapping Tool

This is a Streamlit-based AI assistant that automatically maps cybersecurity detection use cases to the [MITRE ATT&CK](https://attack.mitre.org/) framework using an **agentic AI pipeline**.

---

## 🚀 Features

- 📄 Upload detection rules in CSV format
- 🧠 Map rules to top MITRE ATT&CK techniques using embedding similarity (MPNet)
- 🧩 Multi-agent system for:
  - IOC extraction
  - Natural language translation
  - Log source identification
  - Technique justification
- 📊 Visual dashboard with filters and pie charts
- ⬇️ Export results as:
  - Mapped CSV
  - MITRE Navigator JSON layer

---

## 📁 Project Structure

```
.
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── secrets.toml            # Optional API keys (VirusTotal, etc.)
├── mitre_data/
│   └── attack_techniques.json # MITRE dataset (~200+ techniques)
└── src/
    ├── embedding_model.py      # Model logic (MPNet)
    ├── navigator_generator.py  # Generates Navigator JSON
    ├── visualization.py        # Charts and filters
    └── agents/
        ├── ioc_agent.py
        ├── enrichment_agent.py
        ├── nl_agent.py
        ├── mapping_agent.py
        ├── justification_agent.py
        └── data_source_agent.py
```

---

## 📄 Input Format (CSV)

Required columns:
- `Use Case Name`
- `Description`
- `Log Source`

Example:

| Use Case Name | Description                             | Log Source |
|---------------|-----------------------------------------|------------|
| Password Spray Detection | Detects multiple failed logins against AD accounts | Windows     |
| Kerberoasting | Detects SPN-based ticket requests       | Sysmon     |

---

## 🧠 How It Works

Each rule is processed through several agents:

1. **IOC Agent** – extracts IPs, hashes, file names  
2. **NL Agent** – converts rule into natural language  
3. **Mapping Agent** – finds top 3 matching MITRE techniques using sentence similarity  
4. **Justification Agent** – explains why a technique was selected  
5. **Visualization** – creates charts and navigator layers  

---

## 📊 Dashboard

- Filter by tactic or technique
- View donut charts of MITRE coverage
- View all mapping results in a searchable table

---

## 📦 Setup Instructions

1. Clone the repo:
```bash
git clone https://github.com/your-org/ram-project.git
cd ram-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Add `.streamlit/secrets.toml` if using API keys:
```toml
VIRUSTOTAL_API_KEY = "your-key"
ABUSEIPDB_API_KEY = "your-key"
```

4. Run the app:
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this project to GitHub
2. Go to https://streamlit.io/cloud
3. Click **New App** and select:
   - Repo: your-repo
   - File: `app.py`
4. Click **Deploy**

---

## 👥 Credits

This tool was enhanced using the [MITRE ATT&CK framework](https://attack.mitre.org/) and inspired by agentic design patterns in AI tooling.
