import streamlit as st

st.title("Scenario Builder")

st.info(
"""
HSTIS is a decision-support prototype that maps fish slaughter
operational scenarios into constraint activation patterns,
failure pathways, welfare risks, and prototype opportunities.
"""
)

# --- Species ---

species_type = st.selectbox(
"Species Type",
[
"salmon",
"trout",
"tilapia",
"carp",
"tuna",
"mixed_species"
]
)
st.caption("Biological category of fish population being processed.")

# --- Fish Size ---

fish_size = st.selectbox(
"Fish Size",
[
"small",
"medium",
"large",
"mixed"
]
)
st.caption("Distribution of fish body sizes in the batch.")

# --- Throughput ---

throughput = st.selectbox(
"Throughput",
[
"low",
"medium",
"high",
"very_high"
]
)
st.caption("Processing speed / volume pressure in the system.")

# --- Power ---

power_availability = st.selectbox(
"Power Availability",
[
"low",
"moderate",
"high"
]
)
st.caption("Available energy capacity for stunning, monitoring, or automation systems.")

# --- Verification ---

verification_capacity = st.selectbox(
"Verification Capacity",
[
"low",
"medium",
"high"
]
)
st.caption("Ability to confirm insensibility and welfare state in real time.")

# --- Monitoring ---

monitoring_level = st.selectbox(
"Monitoring Level",
[
"low",
"medium",
"high"
]
)
st.caption("Extent of continuous observation of slaughter process conditions.")

# --- Crew Skill ---

crew_skill = st.selectbox(
"Crew Skill",
[
"low",
"medium",
"high"
]
)
st.caption("Operational expertise of personnel handling slaughter processes.")

# --- Environment ---

environment_type = st.selectbox(
"Environment Type",
[
"vessel",
"facility",
"automated_facility",
"research_facility"
]
)
st.caption("Physical and infrastructural context of the slaughter system.")

# --- Store scenario ---

st.session_state["scenario"] = {
"species_type": species_type,
"fish_size": fish_size,
"throughput": throughput,
"power_availability": power_availability,
"verification_capacity": verification_capacity,
"monitoring_level": monitoring_level,
"crew_skill": crew_skill,
"environment_type": environment_type
}

st.success("Scenario saved.")

# --- SAFE DEBUG VIEW (replace raw state dump) ---

with st.expander("Debug View (Scenario Data)"):
    st.json(st.session_state["scenario"])
