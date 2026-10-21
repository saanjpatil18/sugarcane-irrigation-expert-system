# Import the engine function that will run each test scenario.
from engine import run_engine


# Store test scenarios with their inputs and expected engine results.
SCENARIOS = [
    {
        "name": "Normal flood irrigation",
        "facts": {
            "crop_stage": "grand_growth",
            "soil_moisture": "low",
            "rain_forecast": "none",
            "temperature": "hot",
            "power_available": "yes",
            "irrigation_method": "flood",
        },
        "expected_advisory": {"irrigate_now": "yes", "duration_hours": 2},
        "expected_rules": ["L1-R1", "L2-R1", "L3-R5"],
    },
    {
        "name": "Skip because of heavy rain",
        "facts": {
            "crop_stage": "grand_growth",
            "soil_moisture": "medium",
            "rain_forecast": "heavy",
            "temperature": "moderate",
            "power_available": "yes",
            "irrigation_method": "flood",
        },
        "expected_advisory": {"skip": "yes", "duration_hours": 0},
        "expected_rules": ["L1-R6", "L3-R2", "L1-R2", "L2-R3"],
    },
    {
        "name": "Heavy rain overrides low moisture",
        "facts": {
            "crop_stage": "grand_growth",
            "soil_moisture": "low",
            "rain_forecast": "heavy",
            "temperature": "hot",
            "power_available": "yes",
            "irrigation_method": "flood",
        },
        "expected_advisory": {"skip": "yes", "duration_hours": 0},
        "expected_rules": ["L1-R6", "L3-R2", "L1-R1", "L2-R1"],
    },
    {
        "name": "Stop during ripening",
        "facts": {
            "crop_stage": "ripening",
            "soil_moisture": "low",
            "rain_forecast": "none",
            "temperature": "hot",
            "power_available": "yes",
            "irrigation_method": "flood",
        },
        "expected_advisory": {"stop_for_ripening": "yes", "duration_hours": 0},
        "expected_rules": ["L3-R1", "L1-R5"],
    },
    {
        "name": "Irrigate later when power is unavailable",
        "facts": {
            "crop_stage": "grand_growth",
            "soil_moisture": "low",
            "rain_forecast": "none",
            "temperature": "hot",
            "power_available": "no",
            "irrigation_method": "flood",
        },
        "expected_advisory": {"irrigate_later": "yes", "duration_hours": 0},
        "expected_rules": ["L2-R6", "L1-R1", "L2-R1", "L3-R4"],
    },
    {
        "name": "Skip when soil moisture is high",
        "facts": {
            "crop_stage": "tillering",
            "soil_moisture": "high",
            "rain_forecast": "none",
            "temperature": "moderate",
            "power_available": "yes",
            "irrigation_method": "flood",
        },
        "expected_advisory": {"skip": "yes", "duration_hours": 0},
        "expected_rules": ["L3-R3", "L2-R4"],
    },
    {
        "name": "No final advisory with missing facts",
        "facts": {
            "crop_stage": "grand_growth",
            "soil_moisture": "low",
        },
        "expected_advisory": {},
        "expected_rules": [],
    },
    {
        "name": "Drip irrigation uses shorter duration than flood",
        "facts": {
            "crop_stage": "grand_growth",
            "soil_moisture": "low",
            "rain_forecast": "none",
            "temperature": "hot",
            "power_available": "yes",
            "irrigation_method": "drip",
        },
        "expected_advisory": {"irrigate_now": "yes", "duration_hours": 1},
        "expected_rules": ["L1-R1", "L2-R1", "L3-R6"],
    },
]


# Run every scenario and print whether its result matches the expectation.
def run_tests():
    # Check each test scenario separately.
    for scenario in SCENARIOS:
        # Copy the input facts so the test data is not changed directly.
        facts = scenario["facts"].copy()
        # Run the forward-chaining engine.
        final_facts, trace = run_engine(facts)
        # Get the rule IDs in the order in which they fired.
        fired_rules = [item["rule_id"] for item in trace]
        # Keep the expected advisory fields that the engine actually produced.
        actual_advisory = {
            name: final_facts.get(name)
            for name in scenario["expected_advisory"]
        }
        # Require every expected advisory field to have the expected value.
        advisory_matches = actual_advisory == scenario["expected_advisory"]
        # Check the fired rule IDs in their exact order.
        rules_match = fired_rules == scenario["expected_rules"]
        # Mark the scenario as passed only when both checks succeed.
        result = "PASS" if advisory_matches and rules_match else "FAIL"
        # Print the test result and its important details.
        print(f"{result}: {scenario['name']}")
        print(f"  Inputs: {scenario['facts']}")
        print(f"  Fired rules: {fired_rules}")
        print(f"  Output: {actual_advisory}")


# Run the tests when this file is started directly.
if __name__ == "__main__":
    run_tests()
