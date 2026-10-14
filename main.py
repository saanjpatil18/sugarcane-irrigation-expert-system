# Import the forward-chaining function from the engine file.
from engine import run_engine


# Ask for one choice and keep asking until the user enters a valid number.
def ask_choice(question, choices):
    # Show the question and all numbered choices.
    print(question)
    # Show option zero for an unknown answer.
    print("0. Unknown")
    # Print each available choice with its number.
    for number, choice in enumerate(choices, start=1):
        # Display one numbered choice.
        print(f"{number}. {choice}")
    # Keep asking until the answer is valid.
    while True:
        # Read the user's answer and remove extra spaces.
        answer = input("Enter the number: ").strip()
        # Accept zero and leave this fact out of the facts dictionary.
        if answer == "0":
            # Return None to represent an unknown fact.
            return None
        # Check whether the answer is a number for one of the choices.
        if answer.isdigit() and 1 <= int(answer) <= len(choices):
            # Return the selected choice text.
            return choices[int(answer) - 1]
        # Explain the invalid input before asking again.
        print("Invalid choice. Please enter one of the shown numbers.")


# Ask for a whole-number value and keep asking until it is valid.
def ask_number(question):
    # Keep asking until the user enters zero or a non-negative whole number.
    while True:
        # Read the number and remove extra spaces.
        answer = input(f"{question} (enter 0 if unknown): ").strip()
        # Check that the answer contains only digits.
        if answer.isdigit():
            # Convert the answer from text to an integer.
            number = int(answer)
            # Return None for an unknown value.
            if number == 0:
                return None
            # Return the valid number.
            return number
        # Explain the invalid input before asking again.
        print("Invalid number. Please enter a non-negative whole number.")


# Ask all user questions and return the known answers as facts.
def collect_facts():
    # Start with an empty dictionary of facts.
    facts = {}
    # Ask for the crop stage.
    crop_stage = ask_choice(
        "Crop stage:",
        ["germination", "tillering", "grand_growth", "ripening"],
    )
    # Save the crop stage only when it is known.
    if crop_stage is not None:
        facts["crop_stage"] = crop_stage
    # Ask for the soil type.
    soil_type = ask_choice("Soil type:", ["black", "red", "sandy"])
    # Save the soil type only when it is known.
    if soil_type is not None:
        facts["soil_type"] = soil_type
    # Ask for the soil moisture.
    soil_moisture = ask_choice("Soil moisture:", ["low", "medium", "high"])
    # Save the soil moisture only when it is known.
    if soil_moisture is not None:
        facts["soil_moisture"] = soil_moisture
    # Ask for the number of days since the last irrigation.
    days_since_irrigation = ask_number("Days since irrigation")
    # Save the number only when it is known.
    if days_since_irrigation is not None:
        facts["days_since_irrigation"] = days_since_irrigation
    # Ask for the rain forecast.
    rain_forecast = ask_choice("Rain forecast:", ["none", "light", "heavy"])
    # Save the rain forecast only when it is known.
    if rain_forecast is not None:
        facts["rain_forecast"] = rain_forecast
    # Ask for the temperature.
    temperature = ask_choice("Temperature:", ["cool", "moderate", "hot"])
    # Save the temperature only when it is known.
    if temperature is not None:
        facts["temperature"] = temperature
    # Ask whether power is available.
    power_available = ask_choice("Power available:", ["yes", "no"])
    # Save power availability only when it is known.
    if power_available is not None:
        facts["power_available"] = power_available
    # Ask for the irrigation method.
    irrigation_method = ask_choice("Irrigation method:", ["flood", "drip"])
    # Save the irrigation method only when it is known.
    if irrigation_method is not None:
        facts["irrigation_method"] = irrigation_method
    # Return all known input facts.
    return facts


# Print the final advice using the facts concluded by the engine.
def print_advisory(facts):
    # Check the highest-priority stopping advice first.
    if facts.get("stop_for_ripening") == "yes":
        print("Final advice: Stop irrigation for ripening.")
    # Check whether the crop should be irrigated immediately.
    elif facts.get("irrigate_now") == "yes":
        # Read the duration concluded by the selected rule.
        duration = facts.get("duration_hours", 0)
        # Print the immediate irrigation advice.
        print(f"Final advice: Irrigate now for about {duration} hours.")
    # Check whether irrigation should be postponed.
    elif facts.get("irrigate_later") == "yes":
        print("Final advice: Irrigate later when the condition allows it.")
    # Check whether irrigation should be skipped.
    elif facts.get("skip") == "yes":
        print("Final advice: Skip irrigation for now.")
    # Report that the available facts did not produce final advice.
    else:
        print("Final advice: No final advisory could be reached.")


# Print every rule explanation in the order in which it fired.
def print_trace(trace):
    # Print a heading for the explanation section.
    print("\nExplanation trace:")
    # Report when no rules fired.
    if not trace:
        print("No rules fired.")
        return
    # Explain each fired rule.
    for item in trace:
        # Convert each triggering fact into readable text.
        reasons = " and ".join(
            f"{name} = {value}"
            for name, value in item["triggered_by"].items()
        )
        # Convert each conclusion into readable text.
        conclusions = " and ".join(
            f"{name} = {value}"
            for name, value in item["concluded"].items()
        )
        # Print the rule, reasons, conclusions, and source.
        print(
            f"Rule {item['rule_id']} fired because {reasons}, "
            f"so {conclusions} (Source: {item['source']})"
        )


# Explain which direct input facts are missing for rules that could not fire.
def print_missing_facts(facts, trace):
    # Do not show missing information when a final advisory exists.
    final_keys = {"stop_for_ripening", "irrigate_now", "irrigate_later", "skip"}
    # Stop when the engine already produced a final advisory.
    if any(facts.get(key) is not None for key in final_keys):
        return
    # List the direct inputs that are absent from the facts.
    input_names = [
        "crop_stage",
        "soil_type",
        "soil_moisture",
        "days_since_irrigation",
        "rain_forecast",
        "temperature",
        "power_available",
        "irrigation_method",
    ]
    # Find input names that were not supplied by the user.
    missing = [name for name in input_names if name not in facts]
    # Print the missing inputs when at least one exists.
    if missing:
        print("Missing information: " + ", ".join(missing) + ".")
    # Explain that available facts were insufficient when none are missing.
    elif not trace:
        print("The supplied facts were not enough to match a final rule.")


# Run the question-and-advice process once.
def run_once():
    # Collect the user's known input facts.
    facts = collect_facts()
    # Run the forward-chaining engine.
    updated_facts, trace = run_engine(facts)
    # Print the final advisory.
    print_advisory(updated_facts)
    # Print the rule explanation trace.
    print_trace(trace)
    # Print missing information when no final advice was reached.
    print_missing_facts(updated_facts, trace)


# Start the program and allow the user to run it again.
def main():
    # Continue running until the user chooses to stop.
    while True:
        # Print a heading for one consultation.
        print("\nSugarcane Irrigation Expert System")
        # Run one complete consultation.
        run_once()
        # Ask whether another consultation is wanted.
        again = input("\nRun again? (yes/no): ").strip().lower()
        # Stop unless the user clearly answers yes.
        if again != "yes":
            print("Goodbye.")
            break


# Run the command-line program only when this file is started directly.
if __name__ == "__main__":
    main()
