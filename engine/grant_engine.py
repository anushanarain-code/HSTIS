from data_loader import load_library


class GrantEngine:

    def run(self, research_programs):

        grants = load_library(
            "grant_packages.json"
        )

        research_map = {
            rp.id: rp
            for rp in research_programs
        }

        activated = []
        audit = []

        for g in grants:

            required = g.get(
                "research_program_ids",
                []
            )

            matched = [
                research_map[rpid]
                for rpid in required
                if rpid in research_map
            ]

            if len(matched) == 0:
                continue

            avg_pressure = sum(
                rp.pressure
                for rp in matched
            ) / len(matched)

            grant_pressure = (
                avg_pressure
                * g["activation_strength"]
                / 100
            )

            result = {
                "id": g["id"],
                "name": g["name"],
                "scenario_fit": avg_pressure,
                "pressure": grant_pressure
            }

            activated.append(
                type(
                    "GrantPackage",
                    (),
                    result
                )
            )

            audit.append({
                "grant_package_id": g["id"],
                "derived_from": required,
                "average_research_pressure":
                    round(avg_pressure, 2),
                "pressure":
                    round(grant_pressure, 2)
            })

        activated.sort(
            key=lambda x: x.pressure,
            reverse=True
        )

        return activated, audit