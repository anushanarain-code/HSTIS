from data_loader import load_library


class RiskEngine:

    def run(self, failure_modes):

        risks = load_library(
            "risks.json"
        )

        failure_map = {
            f.id: f
            for f in failure_modes
        }

        activated = []
        audit = []

        for r in risks:

            required = r.get(
                "failure_mode_ids",
                []
            )

            matched = [
                failure_map[fid]
                for fid in required
                if fid in failure_map
            ]

            if len(matched) == 0:
                continue

            avg_pressure = sum(
                f.pressure
                for f in matched
            ) / len(matched)

            risk_pressure = (
                avg_pressure
                * r["activation_strength"]
                / 100
            )

            result = {
                "id": r["id"],
                "name": r["name"],
                "scenario_fit": avg_pressure,
                "pressure": risk_pressure
            }

            activated.append(
                type(
                    "Risk",
                    (),
                    result
                )
            )

            audit.append({
                "risk_id": r["id"],
                "derived_from": required,
                "average_failure_pressure":
                    avg_pressure,
                "pressure":
                    risk_pressure
            })

        activated.sort(
            key=lambda x: x.pressure,
            reverse=True
        )

        return activated, audit