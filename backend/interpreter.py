def generate_interpretation(

    prediction,
    adme,
    toxicity,
    sa_score
):

    insights = []

    # ---------------------------------
    # TARGET INTERPRETATION
    # ---------------------------------

    target = prediction["Target"]

    prob = prediction["Probability"]

    target_class = prediction["Class"]

    if prob > 0.8:

        insights.append(

            f"🧠 Strong prediction confidence "
            f"observed for {target}."
        )

    elif prob > 0.5:

        insights.append(

            f"⚠ Moderate confidence prediction "
            f"for {target}."
        )

    else:

        insights.append(

            f"ℹ Weak prediction confidence "
            f"for {target}."
        )

    insights.append(

        f"🎯 Predicted target belongs to "
        f"the {target_class} family."
    )

    # ---------------------------------
    # ADME INTERPRETATION
    # ---------------------------------

    if adme["Lipinski Rule"] == "Pass":

        insights.append(

            "✅ Molecule satisfies "
            "Lipinski drug-likeness criteria."
        )

    else:

        insights.append(

            "⚠ Lipinski violations detected."
        )

    if adme["LogP"] > 5:

        insights.append(

            "⚠ High lipophilicity may "
            "reduce solubility."
        )

    else:

        insights.append(

            "✅ Lipophilicity within "
            "acceptable range."
        )

    if adme["TPSA"] < 140:

        insights.append(

            "✅ TPSA suggests favorable "
            "oral bioavailability."
        )

    else:

        insights.append(

            "⚠ High polarity may affect "
            "membrane permeability."
        )

    # ---------------------------------
    # TOXICITY INTERPRETATION
    # ---------------------------------

    if toxicity["Overall Toxicity"] == "Safe":

        insights.append(

            "✅ Toxicity profile appears "
            "relatively safe."
        )

    else:

        insights.append(

            "⚠ Potential toxicity risks "
            "identified."
        )

    if toxicity["hERG Toxicity"] == "High Risk":

        insights.append(

            "⚠ Possible cardiotoxicity "
            "risk due to hERG interaction."
        )

    if toxicity["AMES Toxicity"] == "High Risk":

        insights.append(

            "⚠ Mutagenicity concern "
            "detected."
        )

    # ---------------------------------
    # SYNTHETIC ACCESSIBILITY
    # ---------------------------------

    score = sa_score["SA Score"]

    if score < 4:

        insights.append(

            "✅ Molecule likely easy "
            "to synthesize."
        )

    elif score < 7:

        insights.append(

            "⚠ Moderate synthetic "
            "complexity detected."
        )

    else:

        insights.append(

            "❌ Molecule may be difficult "
            "to synthesize."
        )

    # ---------------------------------
    # FINAL ASSESSMENT
    # ---------------------------------

    final_assessment = []

    if (
        adme["Lipinski Rule"] == "Pass"
        and toxicity["Overall Toxicity"] == "Safe"
        and score < 7
    ):

        final_assessment.append(

            "🧬 Molecule demonstrates "
            "promising drug-like characteristics."
        )

    else:

        final_assessment.append(

            "⚠ Molecule may require "
            "further optimization."
        )

    final_assessment.append(

        f"🔍 Predicted biological activity "
        f"is primarily associated with {target}."
    )

    return {

        "Insights": insights,

        "Final Assessment": final_assessment
    }