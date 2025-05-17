# --- Utility Functions
def get_achievement_pct(achieved, budget):
    return achieved / (budget if budget != 0 else 1)


def get_per_unit_incentive(pct):
    if pct >= 1.25:
        return 4000
    elif pct >= 1.0:
        return 3000
    elif pct >= 0.8:
        return 1000
    return 0


def calculate_incentive(inputs, designation):
    # Unpack inputs
    achieved = inputs['achieved']
    budget = inputs['budget']
    resale_achieved = inputs['resale_achieved']
    resale_budget = inputs['resale_budget']
    temp_invoice = inputs['temp_invoice']

    # Step 1: Core %
    pct = get_achievement_pct(achieved, budget)
    unit_incentive = get_per_unit_incentive(pct)

    # Step 2: Basic Incentive
    early_bonus = unit_incentive * 1.25 * temp_invoice
    base_incentive = (achieved - temp_invoice) * unit_incentive + early_bonus

    # Step 3: Add-ons
    add_ons = (
        inputs['rotavator'] * 500 +
        inputs['canopy'] * 500 +
        inputs['rx_supreme'] * 5000 +
        inputs['zero_sales'] * 1000 +
        inputs['exchange'] * 1000 +
        inputs['dp20'] * 1000 +
        inputs['dp30'] * 1500 +
        inputs['cash'] * 5000 +
        inputs['installment'] * 1000 +
        inputs['smart'] * 6000 +
        (resale_achieved - inputs['smart']) * 4500
    )

    penalty = inputs['credit'] * 1500
    total_before_mult = base_incentive + add_ons - penalty

    # Step 4: Multiplier logic
    multiplier = 1.0
    if designation == "Territory officer":
        if pct >= 1.75 and resale_achieved >= resale_budget + 1:
            multiplier = 2.0
        elif pct >= 1.6 and resale_achieved >= resale_budget + 1:
            multiplier = 1.5
        elif pct >= 1.4 and resale_achieved >= resale_budget + 1:
            multiplier = 1.25
    else:
        if pct >= 1.65 and resale_achieved >= resale_budget + 1:
            multiplier = 2.0
        elif pct >= 1.5 and resale_achieved >= resale_budget + 1:
            multiplier = 1.5
        elif pct >= 1.3 and resale_achieved >= resale_budget + 1:
            multiplier = 1.25

    # Step 5: Designation logic
    if designation == "Area Head":
        sup_level_incentive = 0.5
        total_adjusted = total_before_mult * sup_level_incentive
    elif designation == "Deputy RSM":
        sup_level_incentive = 0.4
        total_adjusted = total_before_mult * sup_level_incentive
    elif designation == "RSM":
        sup_level_incentive = 0.3
        total_adjusted = total_before_mult * sup_level_incentive
    elif designation == "Part Head":
        sup_level_incentive = 0.15
        total_adjusted = total_before_mult * sup_level_incentive
    else:
        total_adjusted = total_before_mult

    final = total_adjusted * multiplier

    return {
        "unit_incentive": unit_incentive,
        "early_bonus": early_bonus,
        "base_incentive": base_incentive,
        "add_ons": add_ons,
        "penalty": penalty,
        "total_before_mult": total_before_mult,
        "total_adjusted": total_adjusted,
        "multiplier": multiplier,
        "final": final
    }
