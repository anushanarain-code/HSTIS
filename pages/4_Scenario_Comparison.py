import streamlit as st

from models.entities import Scenario

from engine.constraint_engine import ConstraintEngine
from engine.interaction_engine import InteractionEngine
from engine.failure_engine import FailureEngine
from engine.risk_engine import RiskEngine
from engine.prototype_engine import PrototypeEngine
from engine.research_engine import ResearchEngine
from engine.grant_engine import GrantEngine

def top_items(items, n=5):

    return sorted(
        items,
        key=lambda x: x.pressure,
        reverse=True
    )[:n]

def compare_results(result_A, result_B):

    all_items = set(
        result_A.keys()
    ).union(
        result_B.keys()
    )


    changes = []


    for item in all_items:

        a = result_A.get(item,0)

        b = result_B.get(item,0)

        changes.append(
            {
                "name": item,
                "scenario_A": a,
                "scenario_B": b,
                "change": b-a
            }
        )


    return sorted(
        changes,
        key=lambda x: abs(x["change"]),
        reverse=True
    )

st.title(
    "Scenario Comparison"
)

left_col, right_col = st.columns(2)

with left_col:

    st.subheader("Scenario A")

    species_a = st.selectbox(
        "Species A",
        ["salmon","trout","tilapia","carp","tuna","mixed_species"],
        key="species_a"
    )

    throughput_a = st.selectbox(
        "Throughput A",
        ["low","medium","high","very_high"],
        key="throughput_a"
    )
    
    fish_size_a = st.selectbox(
        "Fish Size A",
        ["small","medium","large"],
        key="fish_size_a"
    )

    verification_a = st.selectbox(
        "Verification Capacity A",
        ["low","medium","high"],
        key="verification_a"
    )

    monitoring_a = st.selectbox(
        "Monitoring Level A",
        ["low","medium","high"],
        key="monitoring_a"
    )

    crew_a = st.selectbox(
        "Crew Skill A",
        ["low","medium","high"],
        key="crew_a"
    )

    environment_a = st.selectbox(
        "Environment A",
        ["vessel","facility","automated_facility","research_facility"],
        key="environment_a"
    )

    power_a = st.selectbox(
        "Power Availability A",
        ["low","medium","high"],
        key="power_a"
    )


with right_col:

    st.subheader("Scenario B")

    species_b = st.selectbox(
        "Species B",
        ["salmon","trout","tilapia","carp","tuna","mixed_species"],
        key="species_b"
    )

    throughput_b = st.selectbox(
        "Throughput B",
        ["low","medium","high","very_high"],
        key="throughput_b"
    )

    fish_size_b = st.selectbox(
        "Fish Size B",
        ["small","medium","large"],
        key="fish_size_b"
    )

    verification_b = st.selectbox(
        "Verification Capacity B",
        ["low","medium","high"],
        key="verification_b"
    )

    monitoring_b = st.selectbox(
        "Monitoring Level B",
        ["low","medium","high"],
        key="monitoring_b"
    )

    crew_b = st.selectbox(
        "Crew Skill B",
        ["low","medium","high"],
        key="crew_b"
    )

    environment_b = st.selectbox(
        "Environment B",
        ["vessel","facility","automated_facility","research_facility"],
        key="environment_b"
    )

    power_b = st.selectbox(
        "Power Availability B",
        ["low","medium","high"],
        key="power_b"
    )

scenario_a = Scenario(
    scenario_id="A",
    species_type=species_a,
    fish_size=fish_size_a,
    throughput=throughput_a,
    power_availability=power_a,
    verification_capacity=verification_a,
    monitoring_level=monitoring_a,
    crew_skill=crew_a,
    environment_type=environment_a

)

scenario_b = Scenario(
    scenario_id="B",
    species_type=species_b,
    fish_size=fish_size_b,
    throughput=throughput_b,
    power_availability=power_b,
    verification_capacity=verification_b,
    monitoring_level=monitoring_b,
    crew_skill=crew_b,
    environment_type=environment_b

)

engine = ConstraintEngine()

constraints_a, audit_a = engine.run(
    scenario_a
)

constraints_b, audit_b = engine.run(
    scenario_b
)

interaction_engine = InteractionEngine()

interactions_a, interaction_audit_a = (
    interaction_engine.run(
        constraints_a
    )
)

interactions_b, interaction_audit_b = (
    interaction_engine.run(
        constraints_b
    )
)

failure_engine = FailureEngine()

failure_modes_a, failure_audit_a = (
    failure_engine.run(
        interactions_a
    )
)

failure_modes_b, failure_audit_b = (
    failure_engine.run(
        interactions_b
    )
)

risk_engine = RiskEngine()

risks_a, risk_audit_a = (
    risk_engine.run(
        failure_modes_a
    )
)

risks_b, risk_audit_b = (
    risk_engine.run(
        failure_modes_b
    )
)

prototype_engine = PrototypeEngine()

prototypes_a, prototype_audit_a = (
    prototype_engine.run(
        risks_a
    )
)

prototypes_b, prototype_audit_b = (
    prototype_engine.run(
        risks_b
    )
)

research_engine = ResearchEngine()

research_programs_a, research_audit_a = (
    research_engine.run(
        prototypes_a
    )
)

research_programs_b, research_audit_b = (
    research_engine.run(
        prototypes_b
    )
)

grant_engine = GrantEngine()

grant_packages_a, grant_audit_a = (
    grant_engine.run(
        research_programs_a
    )
)

grant_packages_b, grant_audit_b = (
    grant_engine.run(
        research_programs_b
    )
)

result_A = {
    c.name: c.pressure
    for c in constraints_a
}


result_B = {
    c.name: c.pressure
    for c in constraints_b
}


comparison = compare_results(
    result_A,
    result_B
)

st.header(
    "Scenario Impact Summary"
)


st.subheader(
    "Largest Changes"
)


for item in comparison[:10]:

    st.write(
        f"""
**{item['name']}**

Scenario A: {item['scenario_A']:.1f}

Scenario B: {item['scenario_B']:.1f}

Change: {item['change']:+.1f}

"""
    )

    st.divider()


left_results, right_results = st.columns(2)

with left_results:

    st.subheader("Scenario A")

    st.markdown("### Constraints")

    for c in top_items(constraints_a):
        st.write(f"{c.name} ({c.pressure:.1f})")

    st.markdown("### Interactions")

    for i in top_items(interactions_a):
        st.write(f"{i.name} ({i.pressure:.1f})")

    st.markdown("### Failure Modes")

    for f in top_items(failure_modes_a):
        st.write(f"{f.name} ({f.pressure:.1f})")

    st.markdown("### Risks")

    for r in top_items(risks_a):
        st.write(f"{r.name} ({r.pressure:.1f})")

    st.markdown("### Prototypes")

    for p in top_items(prototypes_a):
        st.write(f"{p.name} ({p.pressure:.1f})")

    st.markdown("### Research Programs")

    for rp in top_items(research_programs_a):
        st.write(f"{rp.name} ({rp.pressure:.1f})")

    st.markdown("### Grant Packages")

    for g in top_items(grant_packages_a):
        st.write(f"{g.name} ({g.pressure:.1f})")
with right_results:

    st.subheader("Scenario B")

    st.markdown("### Constraints")

    for c in top_items(constraints_b):
        st.write(f"{c.name} ({c.pressure:.1f})")

    st.markdown("### Interactions")

    for i in top_items(interactions_b):
        st.write(f"{i.name} ({i.pressure:.1f})")

    st.markdown("### Failure Modes")

    for f in top_items(failure_modes_b):
        st.write(f"{f.name} ({f.pressure:.1f})")

    st.markdown("### Risks")

    for r in top_items(risks_b):
        st.write(f"{r.name} ({r.pressure:.1f})")

    st.markdown("### Prototypes")

    for p in top_items(prototypes_b):
        st.write(f"{p.name} ({p.pressure:.1f})")

    st.markdown("### Research Programs")

    for rp in top_items(research_programs_b):
        st.write(f"{rp.name} ({rp.pressure:.1f})")

    st.markdown("### Grant Packages")

    for g in top_items(grant_packages_b):
        st.write(f"{g.name} ({g.pressure:.1f})")