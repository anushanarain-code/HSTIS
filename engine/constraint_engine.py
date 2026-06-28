from data_loader import load_library
from models.entities import Scenario


class ConstraintEngine:

    def run(self, scenario: Scenario):

        constraints = load_library("constraints.json")

        activated = []
        audit = []

        for c in constraints:

            fit_scores = []
            triggers = []

            for var in c.get("activation_variables", []):

                value = getattr(scenario, var, None)

                fit = self._score(var, value)

                fit_scores.append(fit)

                triggers.append({
                    "field": var,
                    "value": value
                })

            if not fit_scores:
                continue

            scenario_fit = sum(fit_scores) / len(fit_scores)

            pressure = scenario_fit * c["activation_strength"] / 100

            result = {
                "id": c["id"],
                "name": c["name"],
                "scenario_fit": scenario_fit,
                "pressure": pressure
            }

            activated.append(type("Constraint", (), result))

            audit.append({
                "constraint_id": c["id"],
                "triggered_by": triggers,
                "scenario_fit": scenario_fit,
                "pressure": pressure
            })

        activated.sort(key=lambda x: x.pressure, reverse=True)

        return activated, audit

    def _score(self, var, value):

        mapping = {

            "throughput": {
                "very_high": 100,
                "high": 80,
                "medium": 60,
                "low": 40
            },

            "species_type": {
                "mixed_species": 100,
                "tuna": 90,
                "salmon": 70,
                "trout": 70,
                "tilapia": 60,
                "carp": 60
            },

            "verification_capacity": {
                "low": 100,
                "medium": 60,
                "high": 20
            },

            "monitoring_level": {
                "low": 100,
                "medium": 60,
                "high": 20
            },

            "crew_skill": {
                "low": 100,
                "medium": 60,
                "high": 20
            },

            "power_availability": {
                "low": 100,
                "medium": 60,
                "high": 20
            },

            "fish_size": {
                "small": 100,
                "medium": 60,
                "large": 20
            },

            "environment_type": {
                "vessel": 100,
                "facility": 40
            }

        }
        return mapping.get(var, {}).get(value, 50)
