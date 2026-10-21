# Sugarcane Irrigation Expert System Report

## SECTION 1: PROJECT OVERVIEW

### 1.1 System description

This project is a simple command-line sugarcane irrigation expert system. It asks for crop, soil, weather, power, and irrigation information, applies IF-THEN rules, and prints an irrigation recommendation with an explanation trace. The code is intended for sugarcane irrigation decisions. Specific user roles are NOT FOUND IN CODE, although sugarcane farmers and field supervisors are suitable users for this type of system.

### 1.2 Input facts

| Input fact | Allowed values |
|---|---|
| `crop_stage` | `germination`, `tillering`, `grand_growth`, `ripening` |
| `soil_type` | `black`, `red`, `sandy` |
| `soil_moisture` | `low`, `medium`, `high` |
| `days_since_irrigation` | Any positive whole number; `0` means unknown |
| `rain_forecast` | `none`, `light`, `heavy` |
| `temperature` | `cool`, `moderate`, `hot` |
| `power_available` | `yes`, `no` |
| `irrigation_method` | `flood`, `drip` |

For choice questions, `0` means unknown. The unknown fact is not added to the facts dictionary.

### 1.3 Possible final advisories

- `Final advice: Irrigate now for about X hours.`
- `Final advice: Irrigate later when the condition allows it.`
- `Final advice: Skip irrigation for now.`
- `Final advice: Stop irrigation for ripening.`
- `Final advice: No final advisory could be reached.`

## SECTION 2: KNOWLEDGE BASE

### 2.1 Complete rule table

| Rule ID | Layer | IF conditions | THEN conclusion | Priority | Source tag |
|---|---|---|---|---:|---|
| L1-R1 | Layer 1 | `crop_stage = grand_growth` AND `temperature = hot` | `water_demand = high` | 30 | `S1, S2` |
| L1-R2 | Layer 1 | `crop_stage = grand_growth` AND `temperature = moderate` | `water_demand = high` | 29 | `S1, S2` |
| L1-R3 | Layer 1 | `crop_stage = tillering` AND `temperature = hot` | `water_demand = high` | 28 | `S1, S2` |
| L1-R4 | Layer 1 | `crop_stage = germination` AND `temperature = hot` | `water_demand = medium` | 27 | `S1, S2` |
| L1-R5 | Layer 1 | `crop_stage = ripening` | `stage_status = ripening` | 35 | `S1, S2` |
| L1-R6 | Layer 1 | `rain_forecast = heavy` | `rain_risk = high` | 40 | `S4` |
| L2-R1 | Layer 2 | `soil_moisture = low` AND `water_demand = high` | `stress_risk = high` | 60 | `S1, S2` |
| L2-R2 | Layer 2 | `soil_moisture = low` AND `water_demand = medium` | `stress_risk = medium` | 59 | `S1, S2` |
| L2-R3 | Layer 2 | `soil_moisture = medium` AND `water_demand = high` | `stress_risk = medium` | 58 | `S1, S2` |
| L2-R4 | Layer 2 | `soil_moisture = high` | `stress_risk = low` | 57 | `S1, S2` |
| L2-R5 | Layer 2 | `soil_moisture = low` AND `days_since_irrigation = 3_or_more` | `irrigation_is_overdue = yes` | 56 | `Design choice (our assumption)` |
| L2-R6 | Layer 2 | `power_available = no` | `irrigation_is_blocked = yes` | 55 | `Design choice (our assumption)` |
| L3-R1 | Layer 3 | `crop_stage = ripening` | `irrigate_now = no`; `stop_for_ripening = yes`; `duration_hours = 0` | 100 | `S2` |
| L3-R2 | Layer 3 | `rain_risk = high` | `irrigate_now = no`; `irrigate_later = no`; `skip = yes`; `duration_hours = 0` | 99 | `S4` |
| L3-R3 | Layer 3 | `soil_moisture = high` | `irrigate_now = no`; `skip = yes`; `duration_hours = 0` | 98 | `S1, S2, S3` |
| L3-R4 | Layer 3 | `power_available = no` AND `stress_risk = high` | `irrigate_now = no`; `irrigate_later = yes`; `duration_hours = 0` | 97 | `Design choice (our assumption)` |
| L3-R5 | Layer 3 | `stress_risk = high` AND `rain_forecast = none` AND `power_available = yes` AND `irrigation_method = flood` | `irrigate_now = yes`; `duration_hours = 2` | 96 | `S1, S2` |
| L3-R6 | Layer 3 | `stress_risk = high` AND `rain_forecast = none` AND `power_available = yes` AND `irrigation_method = drip` | `irrigate_now = yes`; `duration_hours = 1` | 95 | `S1, S3` |
| L3-R7 | Layer 3 | `stress_risk = medium` AND `power_available = yes` AND `rain_forecast = not_heavy` | `irrigate_later = yes`; `duration_hours = 0` | 94 | `Design choice (our assumption)` |
| L3-R8 | Layer 3 | `stress_risk = low` AND `crop_stage = not_ripening` | `skip = yes`; `duration_hours = 0` | 93 | `S1, S2` |

### 2.2 Rule counts

- Total rules: **20**
- Layer 1 rules: **6**
- Layer 2 rules: **6**
- Layer 3 rules: **8**

### 2.3 Sources used

The source tags found in `rules.py` are:

| Source tag | Rules using the tag |
|---|---|
| `S1` | L1-R1, L1-R2, L1-R3, L1-R4, L1-R5, L2-R1, L2-R2, L2-R3, L2-R4, L3-R3, L3-R5, L3-R6, L3-R8 |
| `S2` | L1-R1, L1-R2, L1-R3, L1-R4, L1-R5, L2-R1, L2-R2, L2-R3, L2-R4, L3-R1, L3-R3, L3-R5, L3-R8 |
| `S3` | L3-R3, L3-R6 |
| `S4` | L1-R6, L3-R2 |
| `Design choice (our assumption)` | L2-R5, L2-R6, L3-R4, L3-R7 |

The full names or URLs for S1, S2, S3, and S4 are NOT FOUND IN CODE. Only the source tags appear in `rules.py`.

### 2.4 Design-choice rules

- L2-R5
- L2-R6
- L3-R4
- L3-R7

### 2.5 Rule dependencies

| Layer 3 rule | Final conclusion | Layer 1 rules feeding it | Layer 2 rules feeding it | Direct input conditions |
|---|---|---|---|---|
| L3-R1 | Stop for ripening | None | None | `crop_stage = ripening` |
| L3-R2 | Skip because of rain | L1-R6 provides `rain_risk = high` | None | None |
| L3-R3 | Skip because soil moisture is high | None | None | `soil_moisture = high` |
| L3-R4 | Irrigate later because power is unavailable | None | L2-R1 provides `stress_risk = high` | `power_available = no` |
| L3-R5 | Irrigate now using flood irrigation | L1-R1, L1-R2, or L1-R3 can provide `water_demand = high` | L2-R1 provides `stress_risk = high` | `rain_forecast = none`, `power_available = yes`, `irrigation_method = flood` |
| L3-R6 | Irrigate now using drip irrigation | L1-R1, L1-R2, or L1-R3 can provide `water_demand = high` | L2-R1 provides `stress_risk = high` | `rain_forecast = none`, `power_available = yes`, `irrigation_method = drip` |
| L3-R7 | Irrigate later for medium stress | L1-R1, L1-R2, L1-R3, or L1-R4 may provide water demand | L2-R2 or L2-R3 provides `stress_risk = medium` | `power_available = yes`, `rain_forecast = not_heavy` |
| L3-R8 | Skip irrigation | None | L2-R4 provides `stress_risk = low` | `crop_stage = not_ripening` |

Important observations:

- L1-R5 creates `stage_status = ripening`, but no later rule uses `stage_status`.
- L2-R5 creates `irrigation_is_overdue`, but no Layer 3 rule uses it.
- L2-R6 creates `irrigation_is_blocked`, but L3-R4 checks `power_available = no` directly.
- L3-R7 requires `rain_forecast = not_heavy`, but the CLI allows only `none`, `light`, or `heavy`.

## SECTION 3: INFERENCE ENGINE

### 3.1 Functions

`rule_matches(rule, facts)` checks one rule. It reads the rule conditions, compares every required value with the current facts, and returns `False` if a fact is missing or different. It returns `True` only when every condition matches.

`run_engine(facts)` creates `trace` and `fired_rules` lists. It repeatedly finds unused matching rules. If none match, it stops. Otherwise, it selects a rule, records its ID, adds its conclusions to `facts`, records the explanation information in `trace`, and repeats. It returns the updated facts and trace.

### 3.2 Conflict resolution

The code uses the key `(rule["priority"], len(rule["if"]))`. Therefore:

1. The highest priority wins.
2. If priority is tied, the rule with more conditions wins.
3. If both are tied, the first matching rule in the `RULES` list wins.

### 3.3 Infinite-loop prevention

Every fired rule ID is added to `fired_rules`. The engine ignores any rule whose ID is already in that list. Therefore, each rule fires only once.

### 3.4 Missing and unknown facts

When the user enters `0`, the interface returns `None` and does not add that fact to the dictionary. When the engine checks a missing fact, `facts.get()` returns `None`, so the condition normally does not match. If no final advisory is reached, `main.py` prints missing direct input names.

### 3.5 Why forward chaining was used

1. The system starts with facts entered by the user.
2. Layer 1 creates derived facts.
3. Layer 2 creates stress assessments.
4. Layer 3 creates final advice.
5. The trace shows the reasoning path.
6. The method is simple to understand and explain.

Backward chaining was not chosen because this code is designed to start with the available facts and move forward through the rule layers.

## SECTION 4: USER INTERFACE

### 4.1 Program flow

The questions are asked in this order:

1. Crop stage
2. Soil type
3. Soil moisture
4. Days since irrigation
5. Rain forecast
6. Temperature
7. Power available
8. Irrigation method

Choice questions show numbered options and `0. Unknown`. Invalid numbers cause the question to be repeated. The days value accepts non-negative whole numbers, and `0` means unknown.

After collecting facts, the program calls `run_engine()`, prints the advisory, prints the explanation trace, reports missing information if needed, and asks whether to run again. It runs again only when the answer is `yes`.

### 4.2 Real CLI output

Sample input used:

- Crop stage: `grand_growth`
- Soil type: `black`
- Soil moisture: `low`
- Days since irrigation: `5`
- Rain forecast: `none`
- Temperature: `hot`
- Power available: `yes`
- Irrigation method: `flood`
- Run again: `no`

```text
Sugarcane Irrigation Expert System
Crop stage:
0. Unknown
1. germination
2. tillering
3. grand_growth
4. ripening
Enter the number: Soil type:
0. Unknown
1. black
2. red
3. sandy
Enter the number: Soil moisture:
0. Unknown
1. low
2. medium
3. high
Enter the number: Days since irrigation (enter 0 if unknown): Rain forecast:
0. Unknown
1. none
2. light
3. heavy
Enter the number: Temperature:
0. Unknown
1. cool
2. moderate
3. hot
Enter the number: Power available:
0. Unknown
1. yes
2. no
Enter the number: Irrigation method:
0. Unknown
1. flood
2. drip
Enter the number: Final advice: Irrigate now for about 2 hours.

Explanation trace:
Rule L1-R1 fired because crop_stage = grand_growth and temperature = hot, so water_demand = high (Source: S1, S2)
Rule L2-R1 fired because soil_moisture = low and water_demand = high, so stress_risk = high (Source: S1, S2)
Rule L3-R5 fired because stress_risk = high and rain_forecast = none and power_available = yes and irrigation_method = flood, so irrigate_now = yes and duration_hours = 2 (Source: S1, S2)

Run again? (yes/no): Goodbye.
```

## SECTION 5: TEST REPORT

### 5.1 Real test output

```text
PASS: Normal flood irrigation
  Inputs: {'crop_stage': 'grand_growth', 'soil_moisture': 'low', 'rain_forecast': 'none', 'temperature': 'hot', 'power_available': 'yes', 'irrigation_method': 'flood'}
  Fired rules: ['L1-R1', 'L2-R1', 'L3-R5']
  Output: {'irrigate_now': 'yes', 'duration_hours': 2}
PASS: Skip because of heavy rain
  Inputs: {'crop_stage': 'grand_growth', 'soil_moisture': 'medium', 'rain_forecast': 'heavy', 'temperature': 'moderate', 'power_available': 'yes', 'irrigation_method': 'flood'}
  Fired rules: ['L1-R6', 'L3-R2', 'L1-R2', 'L2-R3']
  Output: {'skip': 'yes', 'duration_hours': 0}
PASS: Heavy rain overrides low moisture
  Inputs: {'crop_stage': 'grand_growth', 'soil_moisture': 'low', 'rain_forecast': 'heavy', 'temperature': 'hot', 'power_available': 'yes', 'irrigation_method': 'flood'}
  Fired rules: ['L1-R6', 'L3-R2', 'L1-R1', 'L2-R1']
  Output: {'skip': 'yes', 'duration_hours': 0}
PASS: Stop during ripening
  Inputs: {'crop_stage': 'ripening', 'soil_moisture': 'low', 'rain_forecast': 'none', 'temperature': 'hot', 'power_available': 'yes', 'irrigation_method': 'flood'}
  Fired rules: ['L3-R1', 'L1-R5']
  Output: {'stop_for_ripening': 'yes', 'duration_hours': 0}
PASS: Irrigate later when power is unavailable
  Inputs: {'crop_stage': 'grand_growth', 'soil_moisture': 'low', 'rain_forecast': 'none', 'temperature': 'hot', 'power_available': 'no', 'irrigation_method': 'flood'}
  Fired rules: ['L2-R6', 'L1-R1', 'L2-R1', 'L3-R4']
  Output: {'irrigate_later': 'yes', 'duration_hours': 0}
PASS: Skip when soil moisture is high
  Inputs: {'crop_stage': 'tillering', 'soil_moisture': 'high', 'rain_forecast': 'none', 'temperature': 'moderate', 'power_available': 'yes', 'irrigation_method': 'flood'}
  Fired rules: ['L3-R3', 'L2-R4']
  Output: {'skip': 'yes', 'duration_hours': 0}
PASS: No final advisory with missing facts
  Inputs: {'crop_stage': 'grand_growth', 'soil_moisture': 'low'}
  Fired rules: []
  Output: {}
PASS: Drip irrigation uses shorter duration than flood
  Inputs: {'crop_stage': 'grand_growth', 'soil_moisture': 'low', 'rain_forecast': 'none', 'temperature': 'hot', 'power_available': 'yes', 'irrigation_method': 'drip'}
  Fired rules: ['L1-R1', 'L2-R1', 'L3-R6']
  Output: {'irrigate_now': 'yes', 'duration_hours': 1}
```

### 5.2 Test scenario table

| Test number | Scenario name | Input facts | Expected advisory | Actual advisory | Rules fired in order | Result |
|---:|---|---|---|---|---|---|
| 1 | Normal flood irrigation | `crop_stage=grand_growth`, `soil_moisture=low`, `rain_forecast=none`, `temperature=hot`, `power_available=yes`, `irrigation_method=flood` | `irrigate_now=yes`, `duration_hours=2` | `irrigate_now=yes`, `duration_hours=2` | L1-R1, L2-R1, L3-R5 | PASS |
| 2 | Skip because of heavy rain | `crop_stage=grand_growth`, `soil_moisture=medium`, `rain_forecast=heavy`, `temperature=moderate`, `power_available=yes`, `irrigation_method=flood` | `skip=yes`, `duration_hours=0` | `skip=yes`, `duration_hours=0` | L1-R6, L3-R2, L1-R2, L2-R3 | PASS |
| 3 | Heavy rain overrides low moisture | `crop_stage=grand_growth`, `soil_moisture=low`, `rain_forecast=heavy`, `temperature=hot`, `power_available=yes`, `irrigation_method=flood` | `skip=yes`, `duration_hours=0` | `skip=yes`, `duration_hours=0` | L1-R6, L3-R2, L1-R1, L2-R1 | PASS |
| 4 | Stop during ripening | `crop_stage=ripening`, `soil_moisture=low`, `rain_forecast=none`, `temperature=hot`, `power_available=yes`, `irrigation_method=flood` | `stop_for_ripening=yes`, `duration_hours=0` | `stop_for_ripening=yes`, `duration_hours=0` | L3-R1, L1-R5 | PASS |
| 5 | Irrigate later when power is unavailable | `crop_stage=grand_growth`, `soil_moisture=low`, `rain_forecast=none`, `temperature=hot`, `power_available=no`, `irrigation_method=flood` | `irrigate_later=yes`, `duration_hours=0` | `irrigate_later=yes`, `duration_hours=0` | L2-R6, L1-R1, L2-R1, L3-R4 | PASS |
| 6 | Skip when soil moisture is high | `crop_stage=tillering`, `soil_moisture=high`, `rain_forecast=none`, `temperature=moderate`, `power_available=yes`, `irrigation_method=flood` | `skip=yes`, `duration_hours=0` | `skip=yes`, `duration_hours=0` | L3-R3, L2-R4 | PASS |
| 7 | No final advisory with missing facts | `crop_stage=grand_growth`, `soil_moisture=low` | No final advisory | No final advisory; output `{}` | None | PASS |
| 8 | Drip irrigation uses shorter duration than flood | `crop_stage=grand_growth`, `soil_moisture=low`, `rain_forecast=none`, `temperature=hot`, `power_available=yes`, `irrigation_method=drip` | `irrigate_now=yes`, `duration_hours=1` | `irrigate_now=yes`, `duration_hours=1` | L1-R1, L2-R1, L3-R6 | PASS |

### 5.3 Edge cases

- Test 2: heavy rain forecast.
- Test 3: low moisture conflicts with heavy rain.
- Test 4: ripening stage.
- Test 5: no power.
- Test 6: high soil moisture.
- Test 7: missing input facts.
- Test 8: drip irrigation duration.

### 5.4 Failed tests

No tests failed. All eight tests passed.

## SECTION 6: LIMITATIONS AND OBSERVATIONS

1. **Soil type is collected but not used by any rule.** `main.py` stores `soil_type`, but no rule in `rules.py` checks it.
2. **The days-since-irrigation rule cannot match normal CLI input.** L2-R5 requires the string `3_or_more`, but `ask_number()` stores an integer such as `3` or `5`.
3. **The light-rain value does not match L3-R7.** The CLI offers `light`, but L3-R7 requires `not_heavy`.
4. **The system uses exact categories.** `rule_matches()` compares values using `!=`, so spelling, spaces, and different forms do not match.
5. **Multiple advisory facts can remain in the final dictionary.** For example, L3-R2 stores `irrigate_now=no`, `irrigate_later=no`, and `skip=yes`; `print_advisory()` chooses what to display.
6. **The rules require manual maintenance.** All rules are manually stored in the `RULES` list; there is no learning or automatic rule generation.

## SECTION 7: FUTURE IMPROVEMENTS

1. Add numeric comparison logic for `days_since_irrigation`.
2. Add rules that use black, red, and sandy soil types.
3. Make the rain values consistent so `light` rain can be handled by a rule.
4. Add live soil-sensor and weather-service input.
5. Add more tests for boundaries, missing values, all crop stages, temperatures, and rain conditions.

## SECTION 8: FILE SUMMARY

| File | Purpose | Lines in file |
|---|---|---:|
| `rules.py` | Stores the 20 IF-THEN rules in the `RULES` list. | 179 |
| `engine.py` | Matches rules, performs forward chaining, applies priorities, and records the trace. | 57 |
| `main.py` | Provides the command-line interface, validates input, prints advice, and supports repeated runs. | 210 |
| `tests.py` | Runs eight scenarios and prints PASS or FAIL with the fired rules and output. | 140 |

**Total lines across the four files: 586.**
