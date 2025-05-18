import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def count_items(dataframe, field):
    counts = {}
    for entry in dataframe[field]:
        for item in str(entry).split(", "):
            if item and item != "Unknown":
                counts[item] = counts.get(item, 0) + 1
    return counts

def plot_donut(ax, labels, sizes, title):
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    ax.set_title(title, fontsize=12)
    ax.set_aspect('equal')

def show_summary_charts(filtered_data):
    tactic_counts = count_items(filtered_data, "MITRE Tactic")
    technique_counts = count_items(filtered_data, "MITRE Technique")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    plot_donut(ax1, list(tactic_counts.keys()), list(tactic_counts.values()), "Tactic Mapping")
    plot_donut(ax2, list(technique_counts.keys()), list(technique_counts.values()), "Technique Mapping")
    st.pyplot(fig)

def add_filter_controls(mapped_data):
    df = pd.DataFrame(mapped_data)
    tactic_options = sorted(set(x for entry in df["MITRE Tactic"] for x in entry.split(", ")))
    tech_options = sorted(set(x for entry in df["MITRE Technique"] for x in entry.split(", ")))

    selected_tactics = st.multiselect("🎯 Filter by Tactic(s)", tactic_options, default=tactic_options)
    selected_techniques = st.multiselect("🛠️ Filter by Technique(s)", tech_options, default=tech_options)

    filtered_df = df[
        df["MITRE Tactic"].apply(lambda x: any(t in x for t in selected_tactics)) &
        df["MITRE Technique"].apply(lambda x: any(t in x for t in selected_techniques))
    ]

    st.markdown("### 📊 Filtered Dashboard View")
    st.dataframe(filtered_df, use_container_width=True)
    show_summary_charts(filtered_df)
