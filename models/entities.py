from pydantic import BaseModel


class Scenario(BaseModel):

    scenario_id: str

    species_type: str
    fish_size: str
    throughput: str
    power_availability: str
    verification_capacity: str
    monitoring_level: str
    crew_skill: str
    environment_type: str
