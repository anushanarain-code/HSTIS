from data_loader import load_library


class ResearchEngine:

    def run(self, prototypes):

        research_programs = load_library(
            "research_programs.json"
        )

        prototype_map = {
            p.id: p
            for p in prototypes
        }

        activated = []
        audit = []

        for rp in research_programs:

            required = rp.get(
                "prototype_ids",
                []
            )

            matched = [
                prototype_map[pid]
                for pid in required
                if pid in prototype_map
            ]

            if len(matched) == 0:
                continue

            avg_pressure = sum(
                p.pressure
                for p in matched
            ) / len(matched)

            research_pressure = (
                avg_pressure
                * rp["activation_strength"]
                / 100
            )

            result = {
                "id": rp["id"],
                "name": rp["name"],
                "scenario_fit": avg_pressure,
                "pressure": research_pressure
            }

            activated.append(
                type(
                    "ResearchProgram",
                    (),
                    result
                )
            )

            audit.append({
                "research_program_id": rp["id"],
                "derived_from": required,
                "average_prototype_pressure":
                    round(avg_pressure, 2),
                "pressure":
                    round(research_pressure, 2)
            })

        activated.sort(
            key=lambda x: x.pressure,
            reverse=True
        )

        return activated, audit