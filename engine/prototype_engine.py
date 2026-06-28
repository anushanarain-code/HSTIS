from data_loader import load_library


class PrototypeEngine:

    def run(self, risks):

        prototypes = load_library(
            "prototypes.json"
        )

        risk_map = {
            r.id: r
            for r in risks
        }

        activated = []
        audit = []

        for p in prototypes:

            required = p.get(
                "risk_ids",
                []
            )

            matched = [
                risk_map[rid]
                for rid in required
                if rid in risk_map
            ]

            if len(matched) == 0:
                continue

            avg_pressure = sum(
                r.pressure
                for r in matched
            ) / len(matched)

            prototype_pressure = (
                avg_pressure
                * p["activation_strength"]
                / 100
            )

            result = {
                "id": p["id"],
                "name": p["name"],
                "scenario_fit": avg_pressure,
                "pressure": prototype_pressure
            }

            activated.append(
                type(
                    "Prototype",
                    (),
                    result
                )
            )

            audit.append({
                "prototype_id": p["id"],
                "derived_from": required,
                "average_risk_pressure":
                    round(avg_pressure, 2),
                "pressure":
                    round(prototype_pressure, 2)
            })

        activated.sort(
            key=lambda x: x.pressure,
            reverse=True
        )

        return activated, audit