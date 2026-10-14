# This list stores all rules used by the sugarcane irrigation expert system.
RULES = [
    # Layer 1: These rules create derived facts about water demand and rain.
    {
        "id": "L1-R1",
        "if": {"crop_stage": "grand_growth", "temperature": "hot"},
        "then": {"water_demand": "high"},
        "priority": 30,
        "source": "S1, S2",
    },
    {
        "id": "L1-R2",
        "if": {"crop_stage": "grand_growth", "temperature": "moderate"},
        "then": {"water_demand": "high"},
        "priority": 29,
        "source": "S1, S2",
    },
    {
        "id": "L1-R3",
        "if": {"crop_stage": "tillering", "temperature": "hot"},
        "then": {"water_demand": "high"},
        "priority": 28,
        "source": "S1, S2",
    },
    {
        "id": "L1-R4",
        "if": {"crop_stage": "germination", "temperature": "hot"},
        "then": {"water_demand": "medium"},
        "priority": 27,
        "source": "S1, S2",
    },
    {
        "id": "L1-R5",
        "if": {"crop_stage": "ripening"},
        "then": {"stage_status": "ripening"},
        "priority": 35,
        "source": "S1, S2",
    },
    {
        "id": "L1-R6",
        "if": {"rain_forecast": "heavy"},
        "then": {"rain_risk": "high"},
        "priority": 40,
        "source": "S4",
    },

    # Layer 2: These rules assess crop stress and irrigation conditions.
    {
        "id": "L2-R1",
        "if": {"soil_moisture": "low", "water_demand": "high"},
        "then": {"stress_risk": "high"},
        "priority": 60,
        "source": "S1, S2",
    },
    {
        "id": "L2-R2",
        "if": {"soil_moisture": "low", "water_demand": "medium"},
        "then": {"stress_risk": "medium"},
        "priority": 59,
        "source": "S1, S2",
    },
    {
        "id": "L2-R3",
        "if": {"soil_moisture": "medium", "water_demand": "high"},
        "then": {"stress_risk": "medium"},
        "priority": 58,
        "source": "S1, S2",
    },
    {
        "id": "L2-R4",
        "if": {"soil_moisture": "high"},
        "then": {"stress_risk": "low"},
        "priority": 57,
        "source": "S1, S2",
    },
    {
        "id": "L2-R5",
        "if": {"soil_moisture": "low", "days_since_irrigation": "3_or_more"},
        "then": {"irrigation_is_overdue": "yes"},
        "priority": 56,
        "source": "Design choice (our assumption)",
    },
    {
        "id": "L2-R6",
        "if": {"power_available": "no"},
        "then": {"irrigation_is_blocked": "yes"},
        "priority": 55,
        "source": "Design choice (our assumption)",
    },

    # Layer 3: These rules give the final irrigation advice.
    {
        "id": "L3-R1",
        "if": {"crop_stage": "ripening"},
        "then": {
            "irrigate_now": "no",
            "stop_for_ripening": "yes",
            "duration_hours": 0,
        },
        "priority": 100,
        "source": "S2",
    },
    {
        "id": "L3-R2",
        "if": {"rain_risk": "high"},
        "then": {
            "irrigate_now": "no",
            "irrigate_later": "no",
            "skip": "yes",
            "duration_hours": 0,
        },
        "priority": 99,
        "source": "S4",
    },
    {
        "id": "L3-R3",
        "if": {"soil_moisture": "high"},
        "then": {
            "irrigate_now": "no",
            "skip": "yes",
            "duration_hours": 0,
        },
        "priority": 98,
        "source": "S1, S2, S3",
    },
    {
        "id": "L3-R4",
        "if": {"power_available": "no", "stress_risk": "high"},
        "then": {
            "irrigate_now": "no",
            "irrigate_later": "yes",
            "duration_hours": 0,
        },
        "priority": 97,
        "source": "Design choice (our assumption)",
    },
    {
        "id": "L3-R5",
        "if": {
            "stress_risk": "high",
            "rain_forecast": "none",
            "power_available": "yes",
            "irrigation_method": "flood",
        },
        "then": {"irrigate_now": "yes", "duration_hours": 2},
        "priority": 96,
        "source": "S1, S2",
    },
    {
        "id": "L3-R6",
        "if": {
            "stress_risk": "high",
            "rain_forecast": "none",
            "power_available": "yes",
            "irrigation_method": "drip",
        },
        "then": {"irrigate_now": "yes", "duration_hours": 1},
        "priority": 95,
        "source": "S1, S3",
    },
    {
        "id": "L3-R7",
        "if": {
            "stress_risk": "medium",
            "power_available": "yes",
            "rain_forecast": "not_heavy",
        },
        "then": {"irrigate_later": "yes", "duration_hours": 0},
        "priority": 94,
        "source": "Design choice (our assumption)",
    },
    {
        "id": "L3-R8",
        "if": {"stress_risk": "low", "crop_stage": "not_ripening"},
        "then": {"skip": "yes", "duration_hours": 0},
        "priority": 93,
        "source": "S1, S2",
    },
]
