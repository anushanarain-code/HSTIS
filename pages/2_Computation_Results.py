import streamlit as st

from models.entities import Scenario
from engine.constraint_engine import ConstraintEngine
from engine.interaction_engine import InteractionEngine
from engine.failure_engine import FailureEngine
from engine.risk_engine import RiskEngine
from engine.prototype_engine import PrototypeEngine
from engine.research_engine import ResearchEngine
from engine.grant_engine import GrantEngine


st.title("Computation Results")


if "scenario" not in st.session_state:
    st.warning("Please create a scenario first.")
    st.stop()


scenario_data = st.session_state["scenario"]

scenario = Scenario(
    scenario_id="demo",
    species_type=scenario_data["species_type"],
    fish_size=scenario_data["fish_size"],
    throughput=scenario_data["throughput"],
    power_availability=scenario_data["power_availability"],
    verification_capacity=scenario_data["verification_capacity"],
    monitoring_level=scenario_data["monitoring_level"],
    crew_skill=scenario_data["crew_skill"],
    environment_type=scenario_data["environment_type"]
)


engine = ConstraintEngine()
constraints, audit = engine.run(scenario)

interaction_engine = InteractionEngine()
interactions, interaction_audit = interaction_engine.run(constraints)

failure_engine = FailureEngine()
failure_modes, failure_audit = failure_engine.run(interactions)

risk_engine = RiskEngine()
risks, risk_audit = risk_engine.run(failure_modes)

prototype_engine = PrototypeEngine()
prototypes, prototype_audit = prototype_engine.run(risks)

research_engine = ResearchEngine()
research_programs, research_audit = research_engine.run(prototypes)

grant_engine = GrantEngine()
grant_packages, grant_audit = grant_engine.run(research_programs)


# --------------------------
# Sorting (unchanged logic)
# --------------------------

for lst in [
    constraints,
    interactions,
    failure_modes,
    risks,
    prototypes,
    research_programs,
    grant_packages
]:
    lst.sort(key=lambda x: x.pressure, reverse=True)


# --------------------------
# SCENARIO SUMMARY
# --------------------------

st.subheader("Scenario Summary")
st.caption("Operational conditions defining the slaughter system context.")

st.markdown(f"**Species:** {scenario.species_type}")
st.markdown(f"**Fish Size:** {scenario.fish_size}")
st.markdown(f"**Throughput:** {scenario.throughput}")
st.markdown(f"**Verification Capacity:** {scenario.verification_capacity}")
st.markdown(f"**Monitoring Level:** {scenario.monitoring_level}")
st.markdown(f"**Crew Skill:** {scenario.crew_skill}")
st.markdown(f"**Environment:** {scenario.environment_type}")
st.markdown(f"**Power Availability:** {scenario.power_availability}")

st.divider()


# --------------------------
# CONSTRAINTS
# --------------------------

st.subheader("Primary System Constraints")

st.caption(
     "Activation Strength indicates the degree to which a factor is activated in this scenario. "
     "Scenario Relevance indicates its contextual importance under the selected operating conditions."
)

for c in constraints[:5]:
    st.markdown(f"**{c.name}**")
    st.write(f"**Activation Strength:** {c.pressure:.1f}")
    st.write(f"**Scenario Relevance:** {c.scenario_fit:.1f}")
    st.divider()


# --------------------------
# RISKS
# --------------------------

st.subheader("Primary Welfare Risks")

st.caption(
    "Activation Strength indicates risk intensity. "
    "Scenario Relevance indicates how strongly the risk applies to the selected scenario."
)

for r in risks[:5]:
    st.markdown(f"**{r.name}**")
    st.write(f"**Activation Strength:** {r.pressure:.1f}")
    st.write(f"**Scenario Relevance:** {r.scenario_fit:.1f}")
    st.divider()


# --------------------------
# PROTOTYPES
# --------------------------

st.subheader("Prototype Opportunity Areas")

st.caption(
    "Prototype opportunities represent intervention directions linked to identified risks and constraints."
)
for p in prototypes[:5]:
    st.markdown(f"**{p.name}**")
    st.write(f"**Activation Strength:** {p.pressure:.1f}")
    st.write(f"**Scenario Relevance:** {p.scenario_fit:.1f}")
    st.divider()


# --------------------------
# FULL VIEW (DEBUG)
# --------------------------

show_full = st.checkbox("Show Full Computation Results")

if show_full:

    st.subheader("Activated Constraints")
    for c in constraints:
        st.write(f"**{c.name}**")
        st.write(f"**Activation Strength:** {c.pressure:.1f}")
        st.write(f"**Scenario Relevance:** {c.scenario_fit:.1f}")
        st.divider()

    st.subheader("Constraint Interactions")
    if interactions:
        for i in interactions:
            st.write(f"**{i.name}**")
            st.write(f"Activation Strength: {i.pressure:.1f}")
            st.write(f"Scenario Relevance: {i.scenario_fit:.1f}")
            st.divider()
    else:
        st.write("No interactions triggered.")

    st.subheader("Failure Pathways")
    if failure_modes:
        for f in failure_modes:
            st.write(f"**{f.name}**")
            st.write(f"Activation Strength: {f.pressure:.1f}")
            st.write(f"Scenario Relevance: {f.scenario_fit:.1f}")
            st.divider()
    else:
        st.write("No failure pathways triggered.")

    st.subheader("Welfare Risk Map")
    if risks:
        for r in risks:
            st.write(f"**{r.name}**")
            st.write(f"Activation Strength: {r.pressure:.1f}")
            st.write(f"Scenario Relevance: {r.scenario_fit:.1f}")
            st.divider()
    else:
        st.write("No risks triggered.")

    st.subheader("Prototype Opportunities")
    if prototypes:
        for p in prototypes:
            st.write(f"**{p.name}**")
            st.write(f"**Activation Strength:** {p.pressure:.1f}")
            st.write(f"**Scenario Relevance:** {p.scenario_fit:.1f}")
            st.divider()
    else:
        st.write("No prototype opportunities triggered.")

    st.subheader("Research Programs")
    if research_programs:
        for rp in research_programs:
            st.write(f"**{rp.name}**")
            st.write(f"Activation Strength: {rp.pressure:.1f}")
            st.write(f"Scenario Relevance: {rp.scenario_fit:.1f}")
            st.divider()
    else:
        st.write("No research programs triggered.")

    st.subheader("Funding Pathways")
    if grant_packages:
        for g in grant_packages:
            st.write(f"**{g.name}**")
            st.write(f"Activation Strength: {g.pressure:.1f}")
            st.write(f"Scenario Relevance: {g.scenario_fit:.1f}")
            st.divider()
    else:
        st.write("No funding pathways triggered.")