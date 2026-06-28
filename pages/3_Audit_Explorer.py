import streamlit as st

from models.entities import Scenario

from engine.constraint_engine import ConstraintEngine
from engine.interaction_engine import InteractionEngine
from engine.failure_engine import FailureEngine
from engine.risk_engine import RiskEngine
from engine.prototype_engine import PrototypeEngine
from engine.research_engine import ResearchEngine
from engine.grant_engine import GrantEngine

MAX_ITEMS = 8

st.title(
    "Audit Explorer"
)

st.caption(
    "Audit Explorer traces how scenario conditions connect to risks, "
    "prototype opportunities, research priorities, and funding pathways."
)


lineage_level = st.selectbox(
    "Lineage Detail Level",
    [
        "summary",
        "detailed",
        "full"
    ]
)

if lineage_level == "summary":
    MAX_ITEMS = 5
elif lineage_level == "detailed":
    MAX_ITEMS = 8
else:
    MAX_ITEMS = 999

if "scenario" not in st.session_state:

    st.warning(
        "Please create a scenario first."
    )

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

def summarize(items, top_k=8):
    return sorted(
        items,
        key=lambda x: x.pressure,
        reverse=True
    )[:top_k]

engine = ConstraintEngine()

constraints, audit = engine.run(scenario)
constraints = summarize(constraints, MAX_ITEMS)

interaction_engine = InteractionEngine()

interactions, interaction_audit = (
    interaction_engine.run(
        constraints
    )
)
interactions = summarize(interactions, MAX_ITEMS)

failure_engine = FailureEngine()

failure_modes, failure_audit = (
    failure_engine.run(
        interactions
    )
)
failure_modes = summarize(failure_modes, MAX_ITEMS)

risk_engine = RiskEngine()

risks, risk_audit = (
    risk_engine.run(
        failure_modes
    )
)
risks = summarize(risks, MAX_ITEMS)

prototype_engine = PrototypeEngine()

prototypes, prototype_audit = (
    prototype_engine.run(
        risks
    )
)
prototypes = summarize(prototypes, MAX_ITEMS)

research_engine = ResearchEngine()

research_programs, research_audit = (
    research_engine.run(prototypes)
)

all_research_programs = research_programs.copy()

research_names = {
    rp.id: rp.name
    for rp in all_research_programs
}

research_programs = summarize(research_programs, MAX_ITEMS)

grant_engine = GrantEngine()

grant_packages, grant_audit = (
    grant_engine.run(
        research_programs
    )
)
grant_packages = summarize(grant_packages, MAX_ITEMS)

constraint_names = {
       c.id: c.name
       for c in constraints
    }

interaction_names = {
       i.id: i.name
       for i in interactions
    }

failure_names = {
       f.id: f.name
       for f in failure_modes
    }

risk_names = {
       r.id: r.name
       for r in risks
    }

prototype_names = {
       p.id: p.name
       for p in prototypes
    }

with st.expander("Research Program Library"):
    st.json(research_names)

grant_names = {
       g.id: g.name
       for g in grant_packages
    }

st.subheader("Transition Lineage")

st.caption(
    "This view traces how funding pathways connect to research programs, "
    "prototype opportunities, risks, and operational failure pathways."
)

selected_grant = st.selectbox(
    "Select Grant Package",
    [g.id for g in grant_packages]
)

grant_record = next(
    (
        a
        for a in grant_audit
        if a["grant_package_id"] == selected_grant
    ),
    None
)

if grant_record:

    st.markdown(
    f"**Grant Package:** {grant_names.get(selected_grant, selected_grant)}"
)

    
    if lineage_level == "summary":

        for rp_id in grant_record["derived_from"]:

            st.write("↓")

            st.markdown(
                f"**Research Program:** {research_names.get(rp_id, rp_id)}"
            )


    elif lineage_level == "detailed": 


        for rp_id in grant_record["derived_from"]:

            st.write("↓")

            st.markdown(
                f"**Research Program:** {research_names.get(rp_id, rp_id)}"
        )


        st.info(
            "Select Detailed view to expand prototype → risk → failure → constraint lineage."
        )


    elif lineage_level == "full":

        selected_rp = st.selectbox(
            "Select Research Program",
            [
                research_names.get(rp_id, rp_id)
                for rp_id in grant_record["derived_from"]
            ]
        )


        selected_rp_id = next(
            (
                rp_id
                for rp_id in grant_record["derived_from"]
                if research_names.get(rp_id, rp_id) == selected_rp
            ),
            None
        )


        research_record = next(
            (
                a
                for a in research_audit
                if a["research_program_id"] == selected_rp_id
            ),
            None
        )


        if research_record:


            selected_prototype_id = st.selectbox(
                "Select Prototype",
                research_record["derived_from"][:MAX_ITEMS],
                format_func=lambda p_id: prototype_names.get(p_id, p_id)
            )
 
           
            prototype_record = next(
                (
                     a
                     for a in prototype_audit
                     if a["prototype_id"] == selected_prototype_id
                ),
                None
            )
            
            st.write("↓")

            st.markdown(
               f"**Prototype:** {prototype_names.get(selected_prototype_id, selected_prototype_id)}"
            )
                      
            st.divider()

            st.subheader("Risk Pathway")

            selected_risk_id = st.selectbox(
                "Select Risk",
                prototype_record["derived_from"][:MAX_ITEMS],
                format_func=lambda r_id: risk_names.get(r_id, r_id)
            )
            st.write(
                f"Selected Risk: {risk_names.get(selected_risk_id, selected_risk_id)}"
            )
            risk_record = next(
                (a for a in risk_audit if a["risk_id"] == selected_risk_id),
                None
            )

            if risk_record:

                 st.write("↓")
                 st.subheader("Failure Pathways")

                 st.caption(
                    "Operational failure pathways identified from the selected welfare risk."
                 )

                 for failure_id in risk_record["derived_from"][:MAX_ITEMS]:

                      st.markdown(
                          f"**{failure_names.get(failure_id, failure_id)}**"
                      )


            