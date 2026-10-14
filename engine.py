# Import the rules that the engine must evaluate.
from rules import RULES


# Check whether every condition in one rule matches the current facts.
def rule_matches(rule, facts):
    # Read all conditions from the rule.
    conditions = rule["if"]
    # Check each condition one at a time.
    for fact_name, required_value in conditions.items():
        # Return False when the fact is missing or has a different value.
        if facts.get(fact_name) != required_value:
            # Stop checking because all conditions must match.
            return False
    # Return True because every condition matched.
    return True


# Apply matching rules repeatedly until no new rule can be applied.
def run_engine(facts):
    # Store a readable record for every rule that fires.
    trace = []
    # Store the IDs of rules that have already fired.
    fired_rules = []
    # Continue looking for rules until no unused rule matches.
    while True:
        # Store all unused rules that match the current facts.
        matching_rules = [
            rule
            for rule in RULES
            if rule["id"] not in fired_rules and rule_matches(rule, facts)
        ]
        # Stop when there are no more matching unused rules.
        if not matching_rules:
            break
        # Select the rule with priority, condition count, and list order.
        selected_rule = max(
            matching_rules,
            key=lambda rule: (rule["priority"], len(rule["if"])),
        )
        # Record the selected rule ID so it cannot fire again.
        fired_rules.append(selected_rule["id"])
        # Add every conclusion from the selected rule to the facts.
        for fact_name, conclusion in selected_rule["then"].items():
            # Store or update the concluded fact.
            facts[fact_name] = conclusion
        # Record why the rule fired and what it concluded.
        trace.append(
            {
                "rule_id": selected_rule["id"],
                "triggered_by": selected_rule["if"],
                "concluded": selected_rule["then"],
                "source": selected_rule["source"],
            }
        )
    # Return the updated facts and the complete firing trace.
    return facts, trace
