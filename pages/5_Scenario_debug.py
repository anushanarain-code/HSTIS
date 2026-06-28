import streamlit as st

from models.entities import Scenario
from engine.constraint_engine import ConstraintEngine


st.title("Scenario Variable Debugger")


st.subheader("Scenario A")


species_A = st.selectbox(
    "Species A",
    [
        "salmon",
        "tilapia",
        "trout",
        "carp",
        "mixed_species"
    ],
    key="species_A"
)


verification_A = st.selectbox(
    "Verification Capacity A",
    [
        "low",
        "medium",
        "high"
    ],
    key="verification_A"
)


monitoring_A = st.selectbox(
    "Monitoring Level A",
    [
        "low",
        "medium",
        "high"
    ],
    key="monitoring_A"
)

st.subheader("Scenario B")


species_B = st.selectbox(
    "Species B",
    [
        "salmon",
        "tilapia",
        "trout",
        "carp",
        "mixed_species"
    ],
    key="species_B"
)


verification_B = st.selectbox(
    "Verification Capacity B",
    [
        "low",
        "medium",
        "high"
    ],
    key="verification_B"
)


monitoring_B = st.selectbox(
    "Monitoring Level B",
    [
        "low",
        "medium",
        "high"
    ],
    key="monitoring_B"
)

st.subheader("Operational Variables")


throughput_A = st.selectbox(
    "Throughput A",
    [
        "low",
        "medium",
        "high",
        "very_high"
    ],
    key="throughput_A"
)


throughput_B = st.selectbox(
    "Throughput B",
    [
        "low",
        "medium",
        "high",
        "very_high"
    ],
    key="throughput_B"
)


crew_skill_A = st.selectbox(
    "Crew Skill A",
    [
        "low",
        "medium",
        "high"
    ],
    key="crew_skill_A"
)


crew_skill_B = st.selectbox(
    "Crew Skill B",
    [
        "low",
        "medium",
        "high"
    ],
    key="crew_skill_B"
)


power_A = st.selectbox(
    "Power Availability A",
    [
        "low",
        "medium",
        "high"
    ],
    key="power_A"
)


power_B = st.selectbox(
    "Power Availability B",
    [
        "low",
        "medium",
        "high"
    ],
    key="power_B"
)


environment_A = st.selectbox(
    "Environment A",
    [
        "vessel",
        "facility",
        "automated_facility",
        "research_facility"
    ],
    key="environment_A"
)


environment_B = st.selectbox(
    "Environment B",
    [
        "vessel",
        "facility",
        "automated_facility",
        "research_facility"
    ],
    key="environment_B"
)

fish_size_A = st.selectbox(
    "Fish Size A",
    [
        "small",
        "medium",
        "large"
    ],
    key="fish_size_A"
)


fish_size_B = st.selectbox(
    "Fish Size B",
    [
        "small",
        "medium",
        "large"
    ],
    key="fish_size_B"
)

def run_constraints(
    species,
    fish_size,
    verification,
    monitoring,
    throughput,
    crew_skill,
    power_availability,
    environment_type
):

    scenario = Scenario(

        scenario_id="debug",

        species_type=species,

        fish_size=fish_size,

        throughput=throughput,

        power_availability=power_availability,

        verification_capacity=verification,

        monitoring_level=monitoring,

        crew_skill=crew_skill,

        environment_type=environment_type

    )


    engine = ConstraintEngine()


    constraints, audit = engine.run(
        scenario
    )


    return {
        c.name: c.pressure
        for c in constraints
    }



if st.button("Compare Scenarios"):


    result_A = run_constraints(
        species_A,
        fish_size_A,
        verification_A,
        monitoring_A, 
        throughput_A,
        crew_skill_A,
        power_A,
        environment_A
    )


    result_B = run_constraints(
        species_B,
        fish_size_B,
        verification_B,
        monitoring_B,
        throughput_B,
        crew_skill_B,
        power_B,
        environment_B
    )


    all_constraints = set(
        result_A.keys()
    ).union(
        result_B.keys()
    )


    differences = []


    for c in all_constraints:


        a = result_A.get(
            c,
            0
        )


        b = result_B.get(
            c,
            0
        )


        change = b - a


        differences.append(
            (
                c,
                a,
                b,
                change
            )
        )


    differences.sort(
        key=lambda x: abs(x[3]),
        reverse=True
    )



    st.subheader(
        "Constraint Changes"
    )


    for name, a, b, change in differences:


        if abs(change) > 0:


            st.write(
                f"""
                **{name}**

                Scenario A: {a:.1f}

                Scenario B: {b:.1f}

                Change: {change:+.1f}

                """
            )


            st.divider()