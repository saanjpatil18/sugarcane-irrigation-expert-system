# Import Streamlit for the web interface.
import streamlit as st

# Import the existing forward-chaining engine.
from engine import run_engine


# Show the irrigation advice in a clear format.
def show_advisory(facts):
    # Check the ripening stop advice first.
    if facts.get("stop_for_ripening") == "yes":
        st.markdown(
            '<div class="advice-card stop-card"><div class="advice-icon">⏸</div>'
            '<div><div class="advice-label">FINAL ADVISORY</div>'
            '<div class="advice-title">Stop irrigation for ripening</div>'
            '<div class="advice-text">The crop is in the ripening stage.</div></div></div>',
            unsafe_allow_html=True,
        )
    # Check whether the engine recommends immediate irrigation.
    elif facts.get("irrigate_now") == "yes":
        # Read the duration from the concluded facts.
        duration = facts.get("duration_hours", 0)
        # Show the immediate irrigation recommendation.
        st.markdown(
            f'<div class="advice-card now-card"><div class="advice-icon">💧</div>'
            f'<div><div class="advice-label">FINAL ADVISORY</div>'
            f'<div class="advice-title">Irrigate now</div>'
            f'<div class="advice-text">Run irrigation for about '
            f'<strong>{duration} hours</strong>.</div></div></div>',
            unsafe_allow_html=True,
        )
    # Check whether irrigation should happen later.
    elif facts.get("irrigate_later") == "yes":
        st.markdown(
            '<div class="advice-card later-card"><div class="advice-icon">🕒</div>'
            '<div><div class="advice-label">FINAL ADVISORY</div>'
            '<div class="advice-title">Irrigate later</div>'
            '<div class="advice-text">Schedule irrigation when the condition allows it.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
    # Check whether irrigation should be skipped.
    elif facts.get("skip") == "yes":
        st.markdown(
            '<div class="advice-card skip-card"><div class="advice-icon">✓</div>'
            '<div><div class="advice-label">FINAL ADVISORY</div>'
            '<div class="advice-title">Skip irrigation for now</div>'
            '<div class="advice-text">The current conditions do not require irrigation.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
    # Explain that the rules did not reach final advice.
    else:
        st.markdown(
            '<div class="advice-card unknown-card"><div class="advice-icon">?</div>'
            '<div><div class="advice-label">FINAL ADVISORY</div>'
            '<div class="advice-title">No advisory reached</div>'
            '<div class="advice-text">Provide more field information and try again.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )


# Show each fired rule as a readable explanation.
def show_trace(trace):
    # Add a heading for the explanation section.
    st.subheader("How the decision was reached")
    # Explain when no rules fired.
    if not trace:
        st.info("No rules fired.")
        return
    # Display every fired rule in firing order.
    for step, item in enumerate(trace, start=1):
        # Convert the triggering conditions to readable text.
        reasons = " and ".join(
            f"{name} = {value}"
            for name, value in item["triggered_by"].items()
        )
        # Convert the conclusions to readable text.
        conclusions = " and ".join(
            f"{name} = {value}"
            for name, value in item["concluded"].items()
        )
        # Show one numbered explanation step for this rule.
        with st.expander(f"Step {step}  ·  {item['rule_id']}  ·  {conclusions}", expanded=True):
            st.markdown(f"**Because:** {reasons}")
            st.markdown(f"**Conclusion:** {conclusions}")
            st.caption(f"Source: {item['source']}")


# Collect the selected user inputs as a facts dictionary.
def collect_facts():
    # Start with an empty facts dictionary.
    facts = {}
    # Create a select box for the crop stage.
    crop_stage = st.selectbox(
        "Crop stage",
        ["Unknown", "germination", "tillering", "grand_growth", "ripening"],
    )
    # Add the crop stage when it is known.
    if crop_stage != "Unknown":
        facts["crop_stage"] = crop_stage
    # Create a select box for the soil type.
    soil_type = st.selectbox("Soil type", ["Unknown", "black", "red", "sandy"])
    # Add the soil type when it is known.
    if soil_type != "Unknown":
        facts["soil_type"] = soil_type
    # Create a select box for soil moisture.
    soil_moisture = st.selectbox(
        "Soil moisture",
        ["Unknown", "low", "medium", "high"],
    )
    # Add soil moisture when it is known.
    if soil_moisture != "Unknown":
        facts["soil_moisture"] = soil_moisture
    # Create a number input for days since irrigation.
    days_since_irrigation = st.number_input(
        "Days since irrigation (0 means unknown)",
        min_value=0,
        step=1,
        value=0,
    )
    # Add the number only when it is known.
    if days_since_irrigation != 0:
        facts["days_since_irrigation"] = days_since_irrigation
    # Create a select box for the rain forecast.
    rain_forecast = st.selectbox(
        "Rain forecast",
        ["Unknown", "none", "light", "heavy"],
    )
    # Add the rain forecast when it is known.
    if rain_forecast != "Unknown":
        facts["rain_forecast"] = rain_forecast
    # Create a select box for temperature.
    temperature = st.selectbox(
        "Temperature",
        ["Unknown", "cool", "moderate", "hot"],
    )
    # Add temperature when it is known.
    if temperature != "Unknown":
        facts["temperature"] = temperature
    # Create a select box for power availability.
    power_available = st.selectbox(
        "Power available",
        ["Unknown", "yes", "no"],
    )
    # Add power availability when it is known.
    if power_available != "Unknown":
        facts["power_available"] = power_available
    # Create a select box for irrigation method.
    irrigation_method = st.selectbox(
        "Irrigation method",
        ["Unknown", "flood", "drip"],
    )
    # Add the irrigation method when it is known.
    if irrigation_method != "Unknown":
        facts["irrigation_method"] = irrigation_method
    # Return all known facts.
    return facts


# Build the complete Streamlit page.
def main():
    # Set the browser tab title and wide page layout.
    st.set_page_config(
        page_title="Sugarcane Irrigation Expert System",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Add the visual theme and reusable card styles.
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 95% 2%, rgba(104, 190, 143, .18), transparent 26rem),
                linear-gradient(180deg, #f8fbf8 0%, #f2f6f2 100%);
            color: #18352a;
            color-scheme: light;
        }
        html, body, [data-testid="stAppViewContainer"] {
            color-scheme: light !important;
        }
        [data-testid="stAppViewContainer"],
        [data-testid="stSidebar"] {
            color: #18352a !important;
        }
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4 {
            color: #12372a !important;
        }
        [data-testid="stMarkdownContainer"] .hero h1 {
            color: #ffffff !important;
        }
        .block-container {
            max-width: 1440px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }
        .hero {
            background:
                linear-gradient(120deg, rgba(15, 48, 37, .97), rgba(32, 111, 74, .94)),
                radial-gradient(circle at 95% 0%, rgba(152, 225, 178, .35), transparent 18rem);
            padding: 2.6rem 3rem;
            border-radius: 28px;
            color: white;
            margin-bottom: 1.8rem;
            box-shadow: 0 18px 40px rgba(18, 55, 42, .19);
            position: relative;
            overflow: hidden;
        }
        .hero:after {
            content: "IRRIGATION INTELLIGENCE";
            position: absolute;
            right: 2rem;
            bottom: 1.4rem;
            color: rgba(222, 247, 231, .45);
            font-size: .68rem;
            font-weight: 800;
            letter-spacing: .18em;
        }
        .hero h1 {
            color: white;
            font-size: 2.65rem;
            margin: 0 0 .4rem 0;
            letter-spacing: -.04em;
        }
        .hero p {
            color: #d8eee1;
            font-size: 1.08rem;
            margin: 0;
        }
        .hero-status {
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            background: rgba(232, 250, 238, .12);
            border: 1px solid rgba(232, 250, 238, .25);
            border-radius: 999px;
            padding: .42rem .75rem;
            margin-top: 1.25rem;
            color: #dff6e6;
            font-size: .76rem;
            font-weight: 700;
        }
        .hero-status-dot {
            width: .45rem;
            height: .45rem;
            border-radius: 50%;
            background: #74e29a;
            box-shadow: 0 0 0 .2rem rgba(116, 226, 154, .14);
        }
        .eyebrow {
            color: #a9e2bc;
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .18em;
            margin-bottom: .65rem;
        }
        .section-title {
            color: #12372a;
            font-size: 1.45rem;
            font-weight: 700;
            margin: .5rem 0 .3rem 0;
            letter-spacing: -.02em;
        }
        .section-subtitle {
            color: #6a8175;
            font-size: .92rem;
            margin-bottom: 1rem;
        }
        .panel {
            background: rgba(255, 255, 255, .78);
            border: 1px solid #e1ebe4;
            border-radius: 20px;
            padding: 1.25rem 1.35rem;
            box-shadow: 0 10px 28px rgba(22, 54, 39, .06);
        }
        .result-heading {
            color: #12372a;
            font-size: 1.65rem;
            font-weight: 800;
            letter-spacing: -.03em;
            margin: .1rem 0 .25rem 0;
        }
        .result-subtitle {
            color: #6a8175;
            margin-bottom: 1rem;
        }
        .trace-table {
            width: 100%;
            border-collapse: collapse;
            font-size: .88rem;
        }
        .trace-table th {
            background: #edf6ef;
            color: #35634a;
            font-size: .72rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            text-align: left;
            padding: .7rem;
        }
        .trace-table td {
            border-bottom: 1px solid #e5eee7;
            padding: .72rem;
            color: #355344;
            vertical-align: top;
        }
        .sidebar-title {
            color: #153d2d;
            font-weight: 800;
            font-size: 1.2rem;
            letter-spacing: -.02em;
        }
        .mini-pill {
            display: inline-block;
            background: #e3f4e9;
            color: #236b47;
            border-radius: 999px;
            padding: .32rem .65rem;
            font-size: .73rem;
            font-weight: 800;
            margin: .25rem .2rem .35rem 0;
        }
        .advice-card {
            display: flex;
            gap: 1.1rem;
            align-items: center;
            padding: 1.35rem 1.5rem;
            border-radius: 20px;
            margin: .4rem 0 1.3rem 0;
            box-shadow: 0 12px 30px rgba(20, 50, 35, .10);
            border-left: 7px solid;
        }
        .now-card { background: #e7f7ed; border-color: #159447; }
        .later-card { background: #fff5d8; border-color: #e0a528; }
        .skip-card { background: #e8f1f8; border-color: #3784b7; }
        .stop-card { background: #fdebea; border-color: #d64b45; }
        .unknown-card { background: #eeeeee; border-color: #777777; }
        .advice-icon { font-size: 2.2rem; }
        .advice-label {
            color: #587064;
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .12em;
        }
        .advice-title {
            color: #12372a;
            font-size: 1.45rem;
            font-weight: 800;
        }
        .advice-text { color: #40584c; font-size: 1rem; }
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, .86);
            border: 1px solid #e0eae3;
            border-radius: 20px;
            padding: 1.4rem 1.5rem .8rem 1.5rem;
            box-shadow: 0 10px 28px rgba(22, 54, 39, .06);
        }
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label,
        [data-testid="stNumberInput"] label {
            color: #355344 !important;
            font-weight: 650 !important;
        }
        [data-baseweb="select"] > div {
            background: #ffffff !important;
            color: #18352a !important;
            border-color: #cddbd1 !important;
        }
        [data-baseweb="select"] span,
        [data-baseweb="select"] input {
            color: #18352a !important;
            -webkit-text-fill-color: #18352a !important;
        }
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [role="listbox"],
        [role="option"] {
            background: #ffffff !important;
            color: #18352a !important;
        }
        [role="option"]:hover,
        [role="option"][aria-selected="true"] {
            background: #e5f4e9 !important;
            color: #12372a !important;
        }
        [data-testid="stNumberInput"] input {
            background: #ffffff !important;
            color: #18352a !important;
            -webkit-text-fill-color: #18352a !important;
            border-color: #cddbd1 !important;
        }
        [data-testid="stExpander"] {
            border: 1px solid #e0eae3;
            border-radius: 14px;
            background: rgba(255, 255, 255, .74);
        }
        div.stButton > button, div.stFormSubmitButton > button {
            width: 100%;
            background: linear-gradient(135deg, #1f6f4a, #2f8b5d);
            color: white;
            border: 0;
            border-radius: 12px;
            padding: .78rem 1rem;
            font-weight: 700;
            box-shadow: 0 7px 16px rgba(31, 111, 74, .2);
        }
        div.stButton > button:hover, div.stFormSubmitButton > button:hover {
            background: #155437;
            color: white;
        }
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, .9);
            border: 1px solid #e0e9e2;
            padding: .9rem;
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(22, 54, 39, .05);
        }
        [data-testid="stMetricLabel"] {
            color: #6a8175;
        }
        [data-testid="stMetricValue"] {
            color: #183f2e;
            font-weight: 800;
        }
        .footer {
            color: #789084;
            font-size: .78rem;
            text-align: center;
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid #dfe9e2;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Show the branded header.
    st.markdown(
        '<div class="hero"><div class="eyebrow">SMART FARMING · RULE-BASED DECISION SUPPORT</div>'
        '<h1>🌱 Sugarcane Irrigation Advisor</h1>'
        '<p>Rule-based guidance for clear, explainable irrigation decisions.</p>'
        '<div class="hero-status"><span class="hero-status-dot"></span>'
        'Inference engine ready · 20 rules loaded</div></div>',
        unsafe_allow_html=True,
    )
    # Show a short guide in the sidebar.
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🌾 About this tool</div>', unsafe_allow_html=True)
        st.markdown(
            '<span class="mini-pill">20 rules</span><span class="mini-pill">3 layers</span>'
            '<span class="mini-pill">Explainable</span>',
            unsafe_allow_html=True,
        )
        st.write(
            "Enter the current field conditions. The expert system applies "
            "20 manually written IF-THEN rules."
        )
        st.markdown("### Advice meanings")
        st.markdown(
            "- **Irrigate now:** immediate watering is recommended\n"
            "- **Irrigate later:** wait and schedule watering\n"
            "- **Skip:** no watering for now\n"
            "- **Stop:** ripening rule has priority"
        )
        st.caption("This is an educational decision-support tool, not a replacement for local agricultural advice.")
    # Create the main input and information columns.
    input_column, info_column = st.columns([1.45, 1], gap="large")
    with input_column:
        # Show the input section heading.
        st.subheader("Field conditions")
        st.caption("Tell us what is happening in the field today.")
        # Put the input controls inside a form.
        with st.form("irrigation_form"):
            # Split the form into two compact columns.
            form_left, form_right = st.columns(2)
            with form_left:
                # Collect the crop stage.
                crop_stage = st.selectbox(
                    "Crop stage",
                    ["Unknown", "germination", "tillering", "grand_growth", "ripening"],
                )
                # Collect the soil type.
                soil_type = st.selectbox("Soil type", ["Unknown", "black", "red", "sandy"])
                # Collect the soil moisture.
                soil_moisture = st.selectbox(
                    "Soil moisture", ["Unknown", "low", "medium", "high"]
                )
                # Collect the number of days since irrigation.
                days_since_irrigation = st.number_input(
                    "Days since irrigation",
                    min_value=0,
                    step=1,
                    value=0,
                    help="Enter 0 when this information is unknown.",
                )
            with form_right:
                # Collect the rain forecast.
                rain_forecast = st.selectbox(
                    "Rain forecast", ["Unknown", "none", "light", "heavy"]
                )
                # Collect the temperature.
                temperature = st.selectbox(
                    "Temperature", ["Unknown", "cool", "moderate", "hot"]
                )
                # Collect power availability.
                power_available = st.selectbox(
                    "Power available", ["Unknown", "yes", "no"]
                )
                # Collect the irrigation method.
                irrigation_method = st.selectbox(
                    "Irrigation method", ["Unknown", "flood", "drip"]
                )
            # Add the form action button.
            submitted = st.form_submit_button("Get irrigation advice")
        # Build the facts dictionary from known selections.
        facts = {}
        selected_values = {
            "crop_stage": crop_stage,
            "soil_type": soil_type,
            "soil_moisture": soil_moisture,
            "rain_forecast": rain_forecast,
            "temperature": temperature,
            "power_available": power_available,
            "irrigation_method": irrigation_method,
        }
        # Add known choice values to the facts dictionary.
        for fact_name, fact_value in selected_values.items():
            if fact_value != "Unknown":
                facts[fact_name] = fact_value
        # Add the days value only when it is known.
        if days_since_irrigation != 0:
            facts["days_since_irrigation"] = days_since_irrigation
    with info_column:
        # Show a quick project summary beside the form.
        st.subheader("How it works")
        st.markdown(
            '<div class="panel">The system starts with your facts, derives water demand '
            'and stress risk, then selects the highest-priority advisory rule.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("#### Decision flow")
        st.markdown(
            "📝 **Input facts**  \n"
            "↓  \n"
            "🔎 **Derived facts**  \n"
            "↓  \n"
            "⚖️ **Stress assessment**  \n"
            "↓  \n"
            "💧 **Final advisory**"
        )
        st.markdown("#### Knowledge base")
        metric_one, metric_two = st.columns(2)
        metric_one.metric("Rules", "20")
        metric_two.metric("Layers", "3")
    # Run the engine only after the form is submitted.
    if submitted:
        # Copy the inputs so the displayed input facts remain clear.
        input_facts = facts.copy()
        # Run the existing forward-chaining engine.
        final_facts, trace = run_engine(facts)
        # Add a divider before the result area.
        st.divider()
        # Show the final recommendation.
        st.subheader("Your irrigation recommendation")
        st.markdown(
            '<div class="result-subtitle">Based on the field conditions you entered and the active rule set.</div>',
            unsafe_allow_html=True,
        )
        show_advisory(final_facts)
        # Show summary metrics for the reasoning run.
        metric_one, metric_two, metric_three = st.columns(3)
        metric_one.metric("Rules fired", len(trace))
        metric_two.metric("Known inputs", len(input_facts))
        metric_three.metric(
            "Last rule",
            trace[-1]["rule_id"] if trace else "None",
        )
        # Organize evidence into clear dashboard tabs.
        trace_tab, facts_tab, method_tab = st.tabs(
            ["Decision trail", "Facts & evidence", "About this decision"]
        )
        with trace_tab:
            # Show the rule explanation trace.
            show_trace(trace)
        with facts_tab:
            # Show the facts entered by the user.
            facts_column, derived_column = st.columns(2)
            with facts_column:
                st.markdown("#### Input facts")
                st.json(input_facts)
            with derived_column:
                st.markdown("#### Facts after reasoning")
                st.json(final_facts)
        with method_tab:
            st.markdown(
                '<div class="panel"><strong>Forward chaining</strong><br>'
                'The engine starts from your input facts, applies matching rules, '
                'adds derived facts, and continues until no unused rule matches. '
                'Higher-priority rules resolve conflicts.</div>',
                unsafe_allow_html=True,
            )
            st.caption(
                "The explanation trail below the recommendation shows the exact "
                "rules that fired and their source tags."
            )
        # Show missing direct inputs when no advisory was reached.
        final_keys = {"stop_for_ripening", "irrigate_now", "irrigate_later", "skip"}
        if not any(final_facts.get(key) is not None for key in final_keys):
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
            missing = [name for name in input_names if name not in input_facts]
            if missing:
                st.info("Missing information: " + ", ".join(missing))
    # Add a small professional footer.
    st.markdown(
        '<div class="footer">Sugarcane Irrigation Advisor · Educational decision-support prototype · '
        'Powered by forward chaining</div>',
        unsafe_allow_html=True,
    )


# Start the Streamlit application.
if __name__ == "__main__":
    main()
