from data_loader import load_library


class FailureEngine:

    def run(self, interactions):

        failures = load_library(
            "failure_modes.json"
        )

        interaction_map = {
            i.id: i
            for i in interactions
        }

        activated = []
        audit = []

        for f in failures:

            required = f.get(
                "interaction_ids",
                []
            )

            matched = [
                interaction_map[iid]
                for iid in required
                if iid in interaction_map
            ]

            if len(matched) == 0:
                continue

            avg_pressure = sum(
                i.pressure
                for i in matched
            ) / len(matched)

            failure_pressure = (
                avg_pressure
                * f["activation_strength"]
                / 100
            )

            result = {
                "id": f["id"],
                "name": f["name"],
                "scenario_fit": avg_pressure,
                "pressure": failure_pressure
            }

            activated.append(
                type(
                    "FailureMode",
                    (),
                    result
                )
            )

            audit.append({
                "failure_mode_id": f["id"],
                "derived_from": required,
                "average_interaction_pressure":
                    avg_pressure,
                "pressure":
                    failure_pressure
            })

        activated.sort(
            key=lambda x: x.pressure,
            reverse=True
        )

        return activated, audit