
import streamlit as st
import pandas as pd
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from agents.ioc_agent import extract_iocs_from_text
from agents.enrichment_agent import enrich_iocs
from agents.nl_agent import translate_rule_to_nl
from agents.data_source_agent import identify_log_source
from agents.mapping_agent import map_to_mitre_technique
from agents.justification_agent import generate_justification
from embedding_model import load_mitre_techniques
from navigator_generator import generate_navigator_layer
from visualization import show_summary_charts, add_filter_controls

st.set_page_config(page_title="🛡️ Agentic Mapper", layout="wide")
st.title("🧠 Agentic Rule-ATT&CK Dashboard")

tab_data, tab_dash = st.tabs(["📋 Upload & Mapping", "📊 Dashboard"])
with tab_data:
    uploaded_file = st.file_uploader("📂 Upload CSV with Use Case, Description, Log Source", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        mitre_techniques = load_mitre_techniques("mitre_data/attack_techniques.json")
        output = []

        with st.spinner("🔄 Mapping use cases to MITRE ATT&CK techniques. This may take a moment..."):
            progress = st.progress(0)
            status = st.empty()

            for i, row in enumerate(df.iterrows()):
                try:
                    index, row = row
                    description = row['Description']
                    source = row['Log Source']
                    name = row['Use Case Name']

                    iocs = extract_iocs_from_text(description)
                    enriched_iocs = enrich_iocs(iocs)
                    nl_description = translate_rule_to_nl(description)
                    data_source = identify_log_source(description, source)

                    matches = map_to_mitre_technique(nl_description, mitre_techniques, top_n=3)
                    tech_ids = [m[0] for m in matches]
                    tech_names = [m[1] for m in matches]
                    tactics = [m[2] for m in matches]
                    justification = generate_justification(nl_description, ", ".join(tactics), ", ".join(tech_ids))

                    output.append({
                        "Use Case Name": name,
                        "Description": description,
                        "Log Source": source,
                        "Translated Description": nl_description,
                        "Data Source": data_source,
                        "MITRE Tactic": ", ".join(tactics),
                        "MITRE Technique": ", ".join(tech_ids),
                        "Extracted IOCs": ", ".join(iocs),
                        "Justification": justification
                    })

                    progress.progress((i + 1) / len(df))
                    status.text(f"✅ Processed: {name}")

                except Exception as e:
                    st.error(f"Error while mapping use case {row.get('Use Case Name', 'Unknown')}: {e}")

            st.session_state["mapped_data"] = output
            st.success("✅ Mapping completed. Review the results below.")
            st.dataframe(pd.DataFrame(output), use_container_width=True)

            csv = pd.DataFrame(output).to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Mapped CSV", data=csv, file_name="mapped_usecases.csv", mime='text/csv')

            layer_json = generate_navigator_layer(output)
            st.download_button("⬇️ Download Navigator JSON", data=json.dumps(layer_json, indent=4),
                               file_name="navigator_layer.json", mime="application/json")

with tab_dash:
    if "mapped_data" in st.session_state:
        add_filter_controls(st.session_state["mapped_data"])
    else:
        st.info("Please upload and map data to view dashboard.")
