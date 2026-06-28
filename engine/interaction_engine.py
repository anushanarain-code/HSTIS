from data_loader import load_library


class InteractionEngine:

    def run(self, constraints):

        interactions = load_library("interactions.json")

        constraint_map = {
            c.id: c for c in constraints
        }

        activated = []
        audit = []

        for i in interactions:

            required = i.get(
                "constraint_ids",
                i.get("constraints", [])
            )

            matched = [
                constraint_map[cid]
                for cid in required
                if cid in constraint_map
            ]

            # Skip if not enough overlap
            if len(matched) < 2:
                continue

            avg_pressure = sum(
                c.pressure for c in matched
            ) / len(matched)

            interaction_pressure = (
                avg_pressure
                * i["activation_strength"]
                / 100
            )

            result = {
                "id": i["id"],
                "name": i["name"],
                "scenario_fit": avg_pressure,
                "pressure": interaction_pressure
            }

            activated.append(type("Interaction", (), result))

            audit.append({
                "interaction_id": i["id"],
                "derived_from": required,
                "average_constraint_pressure": avg_pressure,
                "pressure": interaction_pressure
            })

        activated.sort(
            key=lambda x: x.pressure,
            reverse=True
        )

        return activated, audit