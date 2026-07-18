import os
import pandas as pd


# =====================================
# DEFAULT PATH
# =====================================

DEFAULT_ANALYTICS = "output/analytics.csv"

OUTPUT_FOLDER = "output"



# =====================================
# AI BUSINESS RECOMMENDATION ENGINE
# =====================================

def generate_recommendation(
        analytics_file=DEFAULT_ANALYTICS
):


    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )


    df = pd.read_csv(
        analytics_file
    )


    recommendations = []


    # =====================================
    # CALCULATE AVERAGES
    # =====================================

    avg_visitors = df["Visitors"].mean()

    avg_dwell = df[
        "Total Dwell Time (sec)"
    ].mean()



    # =====================================
    # RULE BASED AI ENGINE
    # =====================================

    for _, row in df.iterrows():


        shelf = row["Shelf"]

        visitors = row["Visitors"]

        dwell = row[
            "Total Dwell Time (sec)"
        ]



        # ---------------------------------
        # HIGH TRAFFIC LOW ENGAGEMENT
        # ---------------------------------

        if (
            visitors > avg_visitors
            and
            dwell < avg_dwell
        ):


            insight = (
                "High customer traffic "
                "but low engagement."
            )


            recommendation = (
                "Improve product visibility, "
                "packaging, pricing display, "
                "or shelf arrangement."
            )



        # ---------------------------------
        # HIGH DWELL TIME
        # ---------------------------------

        elif dwell > 2:


            insight = (
                "Customers spend more time "
                "at this shelf."
            )


            recommendation = (
                "Place premium products, "
                "new arrivals, or promotional "
                "items here."
            )



        # ---------------------------------
        # SHORT INTERACTION
        # ---------------------------------

        elif (
            visitors > 0
            and
            dwell <= 2
        ):


            insight = (
                "Customers notice this shelf "
                "but leave quickly."
            )


            recommendation = (
                "Improve product arrangement, "
                "add attractive pricing labels, "
                "or introduce promotions."
            )



        # ---------------------------------
        # NO VISITORS
        # ---------------------------------

        elif visitors == 0:


            insight = (
                "No customer interaction detected."
            )


            recommendation = (
                "Consider changing product "
                "placement, adding signage, "
                "or relocating products."
            )



        # ---------------------------------
        # NORMAL
        # ---------------------------------

        else:


            insight = (
                "Average customer engagement."
            )


            recommendation = (
                "Maintain current placement "
                "and continue monitoring."
            )



        recommendations.append(

            {

                "Shelf": shelf,

                "Insight": insight,

                "Recommendation": recommendation

            }

        )



    # =====================================
    # SAVE CSV
    # =====================================


    output_csv = os.path.join(
        OUTPUT_FOLDER,
        "recommendations.csv"
    )


    result_df = pd.DataFrame(
        recommendations
    )


    result_df.to_csv(
        output_csv,
        index=False
    )



    # =====================================
    # SAVE TEXT FILE FOR STREAMLIT
    # =====================================


    text_file = os.path.join(
        OUTPUT_FOLDER,
        "recommendations.txt"
    )



    with open(
        text_file,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "="*60
            +
            "\nAI BUSINESS RECOMMENDATION ENGINE\n"
            +
            "="*60
            +
            "\n\n"
        )


        for item in recommendations:


            f.write(
                f"Shelf : {item['Shelf']}\n\n"
            )


            f.write(
                "Insight:\n"
            )


            f.write(
                item["Insight"]
                +
                "\n\n"
            )


            f.write(
                "Recommendation:\n"
            )


            f.write(
                item["Recommendation"]
                +
                "\n"
            )


            f.write(
                "-"*60
                +
                "\n\n"
            )



    # =====================================
    # TERMINAL OUTPUT
    # =====================================


    print("\n")
    print("="*60)
    print(
        " AI BUSINESS RECOMMENDATION ENGINE "
    )
    print("="*60)



    for item in recommendations:


        print(
            "\nShelf :",
            item["Shelf"]
        )


        print(
            "Insight :"
        )


        print(
            item["Insight"]
        )


        print(
            "Recommendation :"
        )


        print(
            item["Recommendation"]
        )


        print(
            "-"*60
        )



    print(
        "\nRecommendation File Saved Successfully!"
    )



    return (
        output_csv,
        text_file
    )


def generate_recommendations():

    csv_path="output/analytics.csv"

    df=pd.read_csv(csv_path)


    avg_visitors=df["Visitors"].mean()
    avg_dwell=df["Total Dwell Time (sec)"].mean()


    recommendations=[]


    for _,row in df.iterrows():

        shelf=row["Shelf"]
        visitors=row["Visitors"]
        dwell=row["Total Dwell Time (sec)"]


        if visitors==0:

            insight="No customer interaction detected."

            recommendation=(
                "Consider changing product placement "
                "or adding signage."
            )


        elif visitors>avg_visitors and dwell<avg_dwell:

            insight="High traffic but low engagement."

            recommendation=(
                "Improve product visibility, "
                "packaging or shelf arrangement."
            )


        elif dwell>2:

            insight="Customers spend more time here."

            recommendation=(
                "Place premium products or "
                "promotional items here."
            )


        else:

            insight="Customers notice this shelf but leave quickly."

            recommendation=(
                "Improve product arrangement, "
                "pricing visibility or promotions."
            )


        recommendations.append({

            "Shelf":shelf,
            "Insight":insight,
            "Recommendation":recommendation

        })


    pd.DataFrame(
        recommendations
    ).to_csv(
        "output/recommendations.csv",
        index=False
    )

# =====================================
# MAIN EXECUTION
# =====================================

if __name__ == "__main__":


    generate_recommendation()