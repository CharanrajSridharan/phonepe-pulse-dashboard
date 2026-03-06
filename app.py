import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="phonepe_pulse"
    )

conn = get_connection()

# ---------------------------
# SIDEBAR NAVIGATION
# ---------------------------
st.sidebar.title("🔎 Navigation")

page = st.sidebar.selectbox(
    "Select a page:",
    ["Home", "Analysis"]
)

# ---------------------------
# HOME PAGE MAP
# ---------------------------
if page == "Home":

    st.markdown("<h1 style='text-align: center;'>📱 PHONEPE DASHBOARD</h1>", unsafe_allow_html=True)

    st.write("Welcome to the PhonePe Business Case Dashboard")

    st.markdown("### 🏳️ India Overview Map")

    # -----------------------------
    # Dropdown Selection
    # -----------------------------
    map_option = st.selectbox(
        "Select Data to Display",
        ["Transaction Value", "Registered Users", "Insurance Amount"]
    )

    # -----------------------------
    # TRANSACTION MAP
    # -----------------------------
    if map_option == "Transaction Value":

        query = """
        SELECT State,
               SUM(Transaction_amount) AS Value
        FROM aggregated_transaction
        GROUP BY State;
        """

        df = pd.read_sql(query, conn)

        df["State"] = df["State"].str.replace("-", " ").str.title()
        df = df.rename(columns={"State": "state"})

        title = "Transaction Value Across India"
        colorbar_title = "Transaction Value"

    # -----------------------------
    # USER MAP
    # -----------------------------
    elif map_option == "Registered Users":

        query = """
        SELECT State,
               SUM(RegisteredUsers) AS Value
        FROM aggregated_user
        GROUP BY State;
        """

        df = pd.read_sql(query, conn)

        # Fix state names so they match geojson
        df["State"] = df["State"].str.replace("-", " ").str.title()

     # Rename column for map
        df = df.rename(columns={"State": "state"})

        title = "Registered Users Across India"
        colorbar_title = "Users"

    # -----------------------------
    # INSURANCE MAP
    # -----------------------------
    else:

        query = """
        SELECT State,
               SUM(Insurance_amount) AS Value
        FROM map_insurance
        GROUP BY State;
        """

        df = pd.read_sql(query, conn)

        df["State"] = df["State"].str.replace("-", " ").str.title()
        df = df.rename(columns={"State": "state"})

        title = "Insurance Amount Across India"
        colorbar_title = "Insurance Amount"

    # Rename column for geojson compatibility
    df = df.rename(columns={"State": "state"})

    # -----------------------------
    # INDIA MAP
    # -----------------------------
    fig = go.Figure(data=go.Choropleth(

        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",

        featureidkey="properties.ST_NM",

        locationmode="geojson-id",

        locations=df["state"],

        z=df["Value"],

        colorscale="inferno",

        marker_line_color="white",

        colorbar=dict(title=colorbar_title)

    ))

    fig.update_geos(
        visible=False,
        projection=dict(type="conic conformal"),
        lonaxis={"range": [68, 98]},
        lataxis={"range": [6, 38]}
    )

    fig.update_layout(
        title=title,
        height=750,  
        width=1000
    )

    st.plotly_chart(fig, use_container_width=True)

# ===========================
# ANALYSIS PAGE
# ===========================
elif page == "Analysis":

    st.title("📊 Business Case Study")

    case = st.selectbox(
        "Choose Case Study",
        [
            "1️⃣ Transaction Analysis for Market Expansion",
            "2️⃣ User Engagement and Growth Strategy",
            "3️⃣ Insurance Engagement Analysis",
            "4️⃣ Transaction Analysis Across States and Districts",
            "5️⃣ User Registration Analysis"
        ]
    )

    # ---------------------------
    # BUSINESS CASE 1
    # ---------------------------
    if case == "1️⃣ Transaction Analysis for Market Expansion":


        year_query = """
        SELECT DISTINCT Year
        FROM aggregated_transaction
        ORDER BY Year;
        """

        years_df = pd.read_sql(year_query, conn)

        selected_year = st.selectbox("Select Year", years_df["Year"])

        st.markdown("<h1 style='text-align: left; color: red;'>Total Transaction Value by State</h1>", unsafe_allow_html=True)

        query1 = f"""
        SELECT State,
            SUM(Transaction_amount) AS Total_Transaction_Value
        FROM aggregated_transaction
        WHERE Year = {selected_year}
        GROUP BY State
        ORDER BY Total_Transaction_Value DESC;
        """

        df1 = pd.read_sql(query1, conn)

        fig, ax = plt.subplots(figsize=(14,10))

        ax.barh(df1["State"], df1["Total_Transaction_Value"], color="Aqua")

        ax.set_xlabel("Transaction Value", fontsize=16, fontweight="bold")
        ax.set_ylabel("State", fontsize=16, fontweight="bold")
        ax.set_title(f"Total Transaction Value by State ({selected_year})", fontsize=20, fontweight="bold")

        ax.invert_yaxis()

        st.pyplot(fig)

        st.write("""
        **Insight**

        • This chart shows the total transaction value across different states for the selected year.    
        • These regions can be targeted for market expansion and financial services growth.
        """)

        st.markdown("<h1 style='text-align: left; color: red;'>Total Transaction Count by State</h1>", unsafe_allow_html=True)

        query2 = f"""
        SELECT State,
            SUM(Transaction_count) AS Total_Transaction_Count
        FROM aggregated_transaction
        WHERE Year = {selected_year}
        GROUP BY State
        ORDER BY Total_Transaction_Count DESC;
        """

        df2 = pd.read_sql(query2, conn)

        fig, ax = plt.subplots(figsize=(14,10))

        ax.barh(df2["State"], df2["Total_Transaction_Count"],color="lime")

        ax.set_xlabel("Transaction Count", fontsize=16, fontweight="bold")
        ax.set_ylabel("State", fontsize=16, fontweight="bold")
        ax.set_title(f"Total Transaction Count by State ({selected_year})", fontsize=20, fontweight="bold")

        ax.invert_yaxis()

        st.pyplot(fig)


        st.write("""
        **Insight**

        • This chart shows the total number of transactions made in each state for the selected year.  
        • States with higher transaction counts indicate strong PhonePe usage and digital payment activity.  
        """)
        
        st.markdown("<h1 style='text-align: left; color: red;'>Year-wise Transaction Growth</h1>", unsafe_allow_html=True)

        query3 = """
            SELECT Year,
                SUM(Transaction_amount) AS Yearly_Transaction_Value
            FROM aggregated_transaction
            GROUP BY Year
            ORDER BY Year;
            """

        df3 = pd.read_sql(query3, conn)

        fig, ax = plt.subplots(figsize=(14,8))

        ax.plot(df3["Year"], df3["Yearly_Transaction_Value"], marker="o")

        ax.set_xlabel("Year", fontsize=16, fontweight="bold")
        ax.set_ylabel("Transaction Value", fontsize=16, fontweight="bold")
        ax.set_title("Year-wise Transaction Growth", fontsize=20, fontweight="bold")

        ax.tick_params(axis='both', labelsize=14)

        st.pyplot(fig)

        st.write("""
            **Insight:**  
            • This chart Shows how total transaction value has changed each year across India.   
            • Any dips might highlight economic slowdown, pandemic effect, or seasonal factors.
            """)

        st.markdown("<h1 style='text-align: left; color: red;'>Quarterly Transaction Trend</h1>", unsafe_allow_html=True)

        state_query = "SELECT DISTINCT State FROM aggregated_transaction ORDER BY State"
        states_df = pd.read_sql(state_query, conn)
        selected_state = st.selectbox("Select State", states_df["State"])


        query4 = f"""
        SELECT Year,
            Quarter,
            SUM(Transaction_amount) AS Quarterly_Total
        FROM aggregated_transaction
        WHERE State = '{selected_state}'
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter;
        """
        df4 = pd.read_sql(query4, conn)


        fig, ax = plt.subplots(figsize=(12,5))
        ax.plot(df4["Quarterly_Total"], color="blue")


        ax.set_xlabel("Quarter Number") 
        ax.set_ylabel("Transaction Value")
        ax.set_title(f"Quarterly Transaction Trend in {selected_state}")

        st.pyplot(fig)

        st.write(f"""
        **Insight:**  
        • This chart Shows how transaction values change every quarter in **{selected_state}**.  
        • Helps identify high-transaction periods easily.
        """)

        st.markdown("<h1 style='text-align: left; color: red;'>Average Transaction Value per State</h1>", unsafe_allow_html=True)

        query5 = """
            SELECT State,
                SUM(Transaction_amount)/SUM(Transaction_count) AS Avg_Transaction_Value
            FROM aggregated_transaction
            GROUP BY State
            ORDER BY Avg_Transaction_Value DESC;
            """

        df5 = pd.read_sql(query5, conn)

        fig, ax = plt.subplots(figsize=(14,10))

        ax.barh(df5["State"], df5["Avg_Transaction_Value"], color="Coral")

        ax.set_xlabel("Average Transaction Value", fontsize=16, fontweight="bold")
        ax.set_ylabel("State", fontsize=16, fontweight="bold")
        ax.set_title("Average Transaction Value per State", fontsize=20, fontweight="bold")

        ax.invert_yaxis()

        st.pyplot(fig)

        st.write("""
            **Insight:**  
            • This chart Shows which states have the highest average value per transaction.  
            • Higher values indicate larger payments per user like urban and  high-income regions.  
            """)
                    


   
    # ---------------------------
    # BUSINESS CASE 2
    # ---------------------------
    elif case == "2️⃣ User Engagement and Growth Strategy":

        # ---------------------------
        # Query 6: Total Registered Users by State
        # ---------------------------
        st.markdown("<h2 style='color: blue;'>Total Registered Users by State</h2>", unsafe_allow_html=True)
        
        query6 = """
        SELECT State,
            SUM(RegisteredUsers) AS Total_Registered_Users
        FROM aggregated_user
        GROUP BY State
        ORDER BY Total_Registered_Users DESC;
        """
        df6 = pd.read_sql(query6, conn)

        fig, ax = plt.subplots(figsize=(14,10))
        ax.barh(df6["State"], df6["Total_Registered_Users"], color="skyblue")
        ax.set_xlabel("Total Registered Users", fontsize=14, fontweight="bold")
        ax.set_ylabel("State", fontsize=14, fontweight="bold")
        ax.set_title("Total Registered Users by State", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - States like Maharashtra and Karnataka have the highest number of registered users.  
        """)

        # ---------------------------
        # Query 7: Total App Opens by State
        # ---------------------------
        st.markdown("<h2 style='color: blue;'>Total App Opens by State</h2>", unsafe_allow_html=True)

        query7 = """
        SELECT State,
            SUM(AppOpens) AS Total_App_Opens
        FROM aggregated_user
        GROUP BY State
        ORDER BY Total_App_Opens DESC;
        """
        df7 = pd.read_sql(query7, conn)

        fig, ax = plt.subplots(figsize=(14,10))
        ax.barh(df7["State"], df7["Total_App_Opens"], color="orange")
        ax.set_xlabel("Total App Opens", fontsize=14, fontweight="bold")
        ax.set_ylabel("State", fontsize=14, fontweight="bold")
        ax.set_title("Total App Opens by State", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - App opens are highly connected with the number of users.  
        - High app usage indicates active engagementand  low usage could highlight usage risk.  
        """)

        # ---------------------------
        # Query 8: App Opens per User (Engagement Rate)
        # ---------------------------
        st.markdown("<h2 style='color: blue;'>App Opens per User (Engagement Rate)</h2>", unsafe_allow_html=True)

        query8 = """
        SELECT State,
            SUM(AppOpens) / SUM(RegisteredUsers) AS Engagement_Rate
        FROM aggregated_user
        GROUP BY State
        ORDER BY Engagement_Rate DESC;
        """
        df8 = pd.read_sql(query8, conn)

        fig, ax = plt.subplots(figsize=(14,10))
        ax.barh(df8["State"], df8["Engagement_Rate"], color="green")
        ax.set_xlabel("App Opens per User", fontsize=14, fontweight="bold")
        ax.set_ylabel("State", fontsize=14, fontweight="bold")
        ax.set_title("User Engagement Rate by State", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Higher engagement rates in smaller states indicate more active users per capita.  
        - Low engagement despite high registration suggests users are not exploring the app fully.  
        """)

        # ---------------------------
        # Query 9: Year-wise User Growth by State
        # ---------------------------
        st.markdown("<h2 style='color: blue;'>Year-wise User Growth by State</h2>", unsafe_allow_html=True)

        query9 = """
        SELECT State,
            Year,
            SUM(RegisteredUsers) AS Yearly_Users
        FROM aggregated_user
        GROUP BY State, Year
        ORDER BY State, Year;
        """
        df9 = pd.read_sql(query9, conn)

     
        states = df9['State'].unique()
        selected_state = st.selectbox("Select State", states)

       
        state_data = df9[df9["State"] == selected_state]

       
        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(state_data["Year"], state_data["Yearly_Users"], marker="o", color="purple", linewidth=2)
        ax.set_xlabel("Year", fontsize=12, fontweight="bold")
        ax.set_ylabel("Registered Users", fontsize=12, fontweight="bold")
        ax.set_title(f"Year-wise User Growth in {selected_state}", fontsize=14, fontweight="bold")
        ax.grid(True)
        st.pyplot(fig)

        st.write(f"""
        **Insight:**  
        - This shows how user registrations have grown year by year in {selected_state}.  
        """)

        # ---------------------------
        # Query 10: Quarterly Growth Trend Across India
        # ---------------------------
        st.markdown("<h2 style='color: blue;'>Quarterly User Growth Across India</h2>", unsafe_allow_html=True)

        query10 = """
            SELECT Year,
                Quarter,
                SUM(RegisteredUsers) AS Quarterly_Users
            FROM aggregated_user
            GROUP BY Year, Quarter
            ORDER BY Year, Quarter;
            """
        df10 = pd.read_sql(query10, conn)

        df10["Year_Quarter"] = df10["Year"].astype(str) + "-Q" + df10["Quarter"].astype(str)

        fig, ax = plt.subplots(figsize=(14,10))
        ax.plot(df10["Year_Quarter"], df10["Quarterly_Users"], marker="o", color="purple")
        ax.set_xlabel("Year-Quarter", fontsize=14, fontweight="bold")
        ax.set_ylabel("Registered Users", fontsize=14, fontweight="bold")
        ax.set_title("Quarterly User Growth Across India", fontsize=18, fontweight="bold")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        st.write("""
            **Insight:**  
            - The quarterly trend helps identify peak periods of user registration.   
            - This can guide future growth strategy planning.
            """)

    # ---------------------------
    # BUSINESS CASE 3
    # ---------------------------
    elif case == "3️⃣ Insurance Engagement Analysis":

        # ---------------------------
        # Query 11: Total Insurance Amount by State
        # ---------------------------
        st.markdown("<h2 style='color: teal;'>Total Insurance Amount by State</h2>", unsafe_allow_html=True)

        query11 = """
        SELECT State,
            SUM(Insurance_amount) AS Total_Insurance_Amount
        FROM map_insurance
        GROUP BY State
        ORDER BY Total_Insurance_Amount DESC;
        """
        df11 = pd.read_sql(query11, conn)

        fig, ax = plt.subplots(figsize=(14,10))
        ax.barh(df11["State"], df11["Total_Insurance_Amount"], color="skyblue")
        ax.set_xlabel("Total Insurance Amount", fontsize=14, fontweight="bold")
        ax.set_ylabel("State", fontsize=14, fontweight="bold")
        ax.set_title("Total Insurance Amount by State", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Maharashtra and Karnataka lead in total insurance amount.  
        - Shows which states contribute most to insurance revenue.  
        """)

        # ---------------------------
        # Query 12: Total Insurance Policies by State
        # ---------------------------
        st.markdown("<h2 style='color: teal;'>Total Insurance Policies by State</h2>", unsafe_allow_html=True)

        query12 = """
        SELECT State,
            SUM(Insurance_count) AS Total_Policies
        FROM map_insurance
        GROUP BY State
        ORDER BY Total_Policies DESC;
        """
        df12 = pd.read_sql(query12, conn)

        fig, ax = plt.subplots(figsize=(14,10))
        ax.barh(df12["State"], df12["Total_Policies"], color="orange")
        ax.set_xlabel("Total Policies", fontsize=14, fontweight="bold")
        ax.set_ylabel("State", fontsize=14, fontweight="bold")
        ax.set_title("Total Insurance Policies by State", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Highlights states with the most active insurance policyholders.  
        - Compare with total insurance amount to see if policies are high or low value.
        """)

        # ---------------------------
        # Query 13: District-Level Insurance Leaders
        # ---------------------------
        st.markdown("<h2 style='color: teal;'>District Contribution to Insurance Amount</h2>", unsafe_allow_html=True)

        query13 = """
        SELECT State,
            District,
            SUM(Insurance_amount) AS Total_Amount
        FROM map_insurance
        GROUP BY State, District
        ORDER BY Total_Amount DESC;
        """

        df13 = pd.read_sql(query13, conn)


        states = df13["State"].unique()
        selected_state = st.selectbox("Select State", states, key="insurance_state")


        state_data = df13[df13["State"] == selected_state]


        state_data = state_data.sort_values("Total_Amount", ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(8,8))
        ax.pie(
            state_data["Total_Amount"],
            labels=state_data["District"],
            autopct="%1.1f%%",
            startangle=140
        )

        ax.set_title(f" District Insurance Contribution in {selected_state}", fontsize=14, fontweight="bold")

        st.pyplot(fig)


        st.write(f"""
        **Insight**

        • This chart shows which districts contribute the most insurance amount in **{selected_state}**.  
        • The larger slice means higher insurance value contribution.  
        """)

        # ---------------------------
        # Query 14: Year-wise Insurance Growth
        # ---------------------------
        st.markdown("<h2 style='color: teal;'>Year-wise Insurance Growth</h2>", unsafe_allow_html=True)

        query14 = """
        SELECT Year,
            SUM(Insurance_amount) AS Yearly_Total_Amount
        FROM map_insurance
        GROUP BY Year
        ORDER BY Year;
        """

        df14 = pd.read_sql(query14, conn)

        fig, ax = plt.subplots(figsize=(10,6))

        ax.plot(
            df14["Year"],
            df14["Yearly_Total_Amount"],
            marker="o"
        )

        ax.set_xlabel("Year", fontsize=12, fontweight="bold")
        ax.set_ylabel("Total Insurance Amount", fontsize=12, fontweight="bold")
        ax.set_title("Insurance Growth Over the Years", fontsize=16, fontweight="bold")

        st.pyplot(fig)


        st.write("""
        **Insight**

        • This chart shows the growth of insurance value over the years.  
        • Increasing trend means more people are adopting insurance services.  
        • Useful to understand long-term market expansion.
        """)

        # ---------------------------
        # Query 15: Average Insurance Value per District
        # ---------------------------
        st.markdown("<h2 style='color: teal;'>Average Insurance Value per District</h2>", unsafe_allow_html=True)

        query15 = """
            SELECT State,
                District,
                SUM(Insurance_amount) / NULLIF(SUM(Insurance_count),0) AS Avg_Value
            FROM map_insurance
            GROUP BY State, District
            ORDER BY Avg_Value DESC;
            """

        df15 = pd.read_sql(query15, conn)


        states = df15["State"].unique()
        selected_state = st.selectbox("Select State", states)


        state_data = df15[df15["State"] == selected_state].sort_values("Avg_Value", ascending=False).head(10)


        fig, ax = plt.subplots(figsize=(12,6))

        ax.bar(state_data["District"], state_data["Avg_Value"], color="brown")

        ax.set_xlabel("District", fontsize=12, fontweight="bold")
        ax.set_ylabel("Average Insurance Value", fontsize=12, fontweight="bold")
        ax.set_title(f"Top Districts by Average Insurance Value in {selected_state}", fontsize=16, fontweight="bold")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        st.write("""
        **Insight**

        • This chart shows the districts with the highest average insurance value per policy.  
        • Higher values indicate districts where people purchase larger insurance coverage.  
        """)
    # ---------------------------
    # BUSINESS CASE 4
    # ---------------------------
    elif case == "4️⃣ Transaction Analysis Across States and Districts":

        # ---------------------------
        # Query 16: District-Level Transaction
        # ---------------------------
        st.markdown("<h2 style='color: darkgreen;'>Top 10 Districts by Transaction Value</h2>", unsafe_allow_html=True)

        query16 = """
        SELECT Entity_name AS District,
            SUM(Transaction_amount) AS Total_Value
        FROM top_transaction
        WHERE Level = 'District'
        GROUP BY Entity_name
        ORDER BY Total_Value DESC
        LIMIT 10;
        """
        df16 = pd.read_sql(query16, conn)

        fig, ax = plt.subplots(figsize=(14,8))
        ax.barh(df16["District"], df16["Total_Value"], color="skyblue")
        ax.set_xlabel("Transaction Value", fontsize=14, fontweight="bold")
        ax.set_ylabel("District", fontsize=14, fontweight="bold")
        ax.set_title("Top 10 Districts by Transaction Value", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Top districts contribute the most to overall transaction value.  
        - Focus on these districts for marketing, promotions, or new feature launches.
        """)

        # ---------------------------
        # Query 17: Top Pincode by Transaction Count
        # ---------------------------
        st.markdown("<h2 style='color: darkgreen;'>Top 10 Pincodes by Transaction Count</h2>", unsafe_allow_html=True)

        query17 = """
        SELECT Entity_name AS Pincode,
            SUM(Transaction_count) AS Total_Count
        FROM top_transaction
        WHERE Level = 'Pincode'
        GROUP BY Entity_name
        ORDER BY Total_Count DESC
        LIMIT 10;
        """
        df17 = pd.read_sql(query17, conn)

        fig, ax = plt.subplots(figsize=(14,8))
        ax.barh(df17["Pincode"], df17["Total_Count"], color="orange")
        ax.set_xlabel("Transaction Count", fontsize=14, fontweight="bold")
        ax.set_ylabel("Pincode", fontsize=14, fontweight="bold")
        ax.set_title("Top 10 Pincodes by Transaction Count", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Shows which pincodes have the highest number of transactions.  
        - Useful for localized campaigns and service improvements.
        """)

        # ---------------------------
        # Query 18: Average Transaction Value by District
        # ---------------------------
        st.markdown("<h2 style='color: darkgreen;'>Average Transaction Value per District</h2>", unsafe_allow_html=True)

        query18 = """
            SELECT State,
                Entity_name AS District,
                SUM(Transaction_amount) /
                NULLIF(SUM(Transaction_count),0) AS Avg_Transaction_Value
            FROM top_transaction
            WHERE Level = 'District'
            GROUP BY State, Entity_name
            ORDER BY Avg_Transaction_Value DESC;
            """

        df18 = pd.read_sql(query18, conn)


        states = df18["State"].unique()
        selected_state = st.selectbox("Select State", states)


        state_data = df18[df18["State"] == selected_state].sort_values("Avg_Transaction_Value", ascending=False).head(10)


        fig, ax = plt.subplots(figsize=(12,6))

        ax.bar(state_data["District"], state_data["Avg_Transaction_Value"], color="Teal")

        ax.set_xlabel("District", fontsize=12, fontweight="bold")
        ax.set_ylabel("Average Transaction Value", fontsize=12, fontweight="bold")
        ax.set_title(f"Districts by Average Transaction Value in {selected_state}", fontsize=16, fontweight="bold")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        st.write("""
            **Insight**

            • This chart shows districts with the highest average transaction value.  
            • Higher values indicate districts where users make larger payments per transaction.  
            """)

        # ---------------------------
        # Query 19: Year-wise Transaction Growth
        # ---------------------------
        st.markdown("<h2 style='color: darkgreen;'>Year-wise Transaction Growth</h2>", unsafe_allow_html=True)

        query19 = """
        SELECT Year,
            SUM(Transaction_amount) AS Yearly_Value
        FROM top_transaction
        GROUP BY Year
        ORDER BY Year;
        """
        df19 = pd.read_sql(query19, conn)

        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(df19["Year"], df19["Yearly_Value"], marker="o", color="purple", linewidth=2)
        ax.set_xlabel("Year", fontsize=14, fontweight="bold")
        ax.set_ylabel("Transaction Value", fontsize=14, fontweight="bold")
        ax.set_title("Year-wise Transaction Growth", fontsize=16, fontweight="bold")
        ax.grid(True)
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Shows the trend of transactions over the years across India.  
        - Steady growth indicates market expansion and increasing user adoption.
        """)

        # ---------------------------
        # Query 20: District vs Pincode Comparison
        # ---------------------------
        st.markdown("<h2 style='color: darkgreen;'>Transaction Comparison: District vs Pincode</h2>", unsafe_allow_html=True)

        query20 = """
        SELECT Level,
            SUM(Transaction_amount) AS Total_Value
        FROM top_transaction
        GROUP BY Level;
        """
        df20 = pd.read_sql(query20, conn)

        fig, ax = plt.subplots(figsize=(8,6))
        ax.bar(df20["Level"], df20["Total_Value"], color=["skyblue", "orange"])
        ax.set_xlabel("Level", fontsize=14, fontweight="bold")
        ax.set_ylabel("Total Transaction Value", fontsize=14, fontweight="bold")
        ax.set_title("Transaction Value: District vs Pincode", fontsize=16, fontweight="bold")
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Compares total transaction value at District and Pincode levels.  
        - Shows where the majority of transactions happen, helping focus analytics and business strategies.
        """)
    # ---------------------------
    # BUSINESS CASE 5
    # ---------------------------
    elif case == "5️⃣ User Registration Analysis":

        # ---------------------------
        # Query 21: State-wise Total Registrations
        # ---------------------------
        st.markdown("<h2 style='color: navy;'>State-wise Total Registrations</h2>", unsafe_allow_html=True)

        query21 = """
        SELECT State,
            SUM(Registered_Users) AS Total_Registrations
        FROM top_user
        WHERE Level = 'District'
        GROUP BY State
        ORDER BY Total_Registrations DESC;
        """
        df21 = pd.read_sql(query21, conn)

        fig, ax = plt.subplots(figsize=(14,8))
        ax.barh(df21["State"], df21["Total_Registrations"], color="skyblue")
        ax.set_xlabel("Total Registrations", fontsize=14, fontweight="bold")
        ax.set_ylabel("State", fontsize=14, fontweight="bold")
        ax.set_title("State-wise Total User Registrations", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - States like Maharashtra and Karnataka have the highest registrations.   
        - Helps prioritize marketing and engagement strategies by state.
        """)

        # ---------------------------
        # Query 22: Registration Growth Over Time (All India)
        # ---------------------------
        st.markdown("<h2 style='color: navy;'>Quarterly Registration Growth Across India</h2>", unsafe_allow_html=True)

        query22 = """
        SELECT Year,
            Quarter,
            SUM(Registered_Users) AS Quarterly_Registrations
        FROM top_user
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter;
        """
        df22 = pd.read_sql(query22, conn)

        df22["Year_Quarter"] = df22["Year"].astype(str) + "-Q" + df22["Quarter"].astype(str)

        fig, ax = plt.subplots(figsize=(14,6))
        ax.plot(df22["Year_Quarter"], df22["Quarterly_Registrations"], marker="o", color="purple", linewidth=2)
        ax.set_xlabel("Year-Quarter", fontsize=14, fontweight="bold")
        ax.set_ylabel("Quarterly Registrations", fontsize=14, fontweight="bold")
        ax.set_title("Quarterly Registration Growth Across India", fontsize=18, fontweight="bold")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Shows growth trend of new registrations over time.  
        - Easy to explain as Total users registering each quarter is steadily increasing.
        """)

        # ---------------------------
        # Query 23: District-Level Top Performers
        # ---------------------------
        st.markdown("<h2 style='color: navy;'>District-Level Top Registration</h2>", unsafe_allow_html=True)

        query23 = """
            SELECT State,
                Entity_name AS District,
                SUM(Registered_Users) AS Total_Registrations
            FROM top_user
            WHERE Level = 'District'
            GROUP BY State, Entity_name
            ORDER BY Total_Registrations DESC;
            """

        df23 = pd.read_sql(query23, conn)

        states = df23["State"].unique()
        selected_state = st.selectbox("Select State", states)

        state_data = df23[df23["State"] == selected_state].sort_values("Total_Registrations", ascending=False).head(10)


        fig, ax = plt.subplots(figsize=(12,6))

        ax.bar(state_data["District"], state_data["Total_Registrations"])

        ax.set_xlabel("District", fontsize=12, fontweight="bold")
        ax.set_ylabel("Total Registrations", fontsize=12, fontweight="bold")
        ax.set_title(f"Top Districts by User Registrations in {selected_state}", fontsize=16, fontweight="bold")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        st.write("""
            **Insight**

            • This chart shows the districts with the highest number of user registrations.  
            • High registration numbers indicate strong PhonePe adoption in these districts.  
            • These areas may be key markets for future financial services and digital payment growth.
            """)
        # ---------------------------
        # Query 24: Pincode-Level Top Performance
        # ---------------------------
        st.markdown("<h2 style='color: navy;'>Top 10 Pincodes by Registrations</h2>", unsafe_allow_html=True)

        query24 = """
        SELECT Entity_name AS Pincode,
            SUM(Registered_Users) AS Total_Registrations
        FROM top_user
        WHERE Level = 'Pincode'
        GROUP BY Entity_name
        ORDER BY Total_Registrations DESC
        LIMIT 10;
        """
        df24 = pd.read_sql(query24, conn)

        fig, ax = plt.subplots(figsize=(14,8))
        ax.barh(df24["Pincode"], df24["Total_Registrations"], color="orange")
        ax.set_xlabel("Total Registrations", fontsize=14, fontweight="bold")
        ax.set_ylabel("Pincode", fontsize=14, fontweight="bold")
        ax.set_title("Top 10 Pincodes by Registrations", fontsize=18, fontweight="bold")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.write("""
        **Insight:**  
        - Highlights pincode-level registration hotspots.  
        - Useful for hyper-local marketing and engagement initiatives.
        """)

        # ---------------------------
        # Query 25: District Contribution Inside Each State 
        # ---------------------------

        st.markdown("<h2 style='color: navy;'>District contributes to the Total Registrations</h2>", unsafe_allow_html=True)

        query25 = """
        SELECT State,
            Entity_name AS District,
            SUM(Registered_Users) AS Total_Registrations
        FROM top_user
        WHERE Level = 'District'
        GROUP BY State, Entity_name;
        """
        df25 = pd.read_sql(query25, conn)

        available_states = df25['State'].unique()

        state_to_show = st.selectbox("Select a State to view district contribution", available_states)

        state_data = df25[df25["State"] == state_to_show]

        fig, ax = plt.subplots(figsize=(12,8))
        ax.barh(state_data["District"], state_data["Total_Registrations"], color="teal")
        ax.set_xlabel("Total Registrations", fontsize=14, fontweight="bold")
        ax.set_ylabel("District", fontsize=14, fontweight="bold")
        ax.set_title(f"District Contribution to Registrations in {state_to_show}", fontsize=16, fontweight="bold")
        ax.invert_yaxis()  # Highest value on top
        st.pyplot(fig)

        st.write(f"""
        **Insight:**  
        - This chart shows how each district contributes to the total registrations in {state_to_show}.    
        - Top districts dominate user acquisition; smaller districts may need targeted campaigns.
        """)


