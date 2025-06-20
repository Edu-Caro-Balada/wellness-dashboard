import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Función para cargar y procesar los datos
@st.cache_data(ttl=300)
def load_data():
    sheet_id = "10z9TpU3nwytVqDh3LlNxMloCIC1St4FH7kbZ6Z2CmQg"
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(sheet_url)

    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date

    vars_1to5 = ["FATIGUE", "SLEEP QUALITY", "MUSCLE DISCOMFORT", "MOOD"]
    var_recovery = "HOW HAVE YOU RECOVERED?"

    for var in vars_1to5:
        df[var] = df[var].astype(str).str.extract(r'(\d)').astype(float)
    df[var_recovery] = pd.to_numeric(df[var_recovery], errors='coerce')

    return df

# Interfaz principal
st.title("🏥 Wellness Dashboard")

# Botón para refrescar los datos
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

df = load_data()

tab1, tab2 = st.tabs(["📊 Daily Overview", "📈 Individual Trend"])

# =====================
# TAB 1 – DAILY OVERVIEW
# =====================
with tab1:
    st.sidebar.title("Filters")
    selected_date = st.sidebar.date_input("Select Date", value=df["Date"].max())
    filtered = df[df["Date"] == selected_date]

    if filtered.empty:
        st.warning("No data available for the selected date.")
    else:
        st.write(f"**Date: {selected_date}**")

        # Variables a mostrar
        variables = ["FATIGUE", "SLEEP QUALITY", "MUSCLE DISCOMFORT", "MOOD"]
        var_recovery = "HOW HAVE YOU RECOVERED?"

        for var in variables + [var_recovery]:
            st.subheader(var)
            fig, ax = plt.subplots(figsize=(10, 3))

            colors = []
            for v in filtered[var]:
                if pd.isna(v):
                    colors.append("gray")
                elif var == var_recovery:
                    if v < 5:
                        colors.append("red")
                    elif v <= 7:
                        colors.append("orange")
                    else:
                        colors.append("green")
                else:
                    if v < 3:
                        colors.append("red")
                    elif v == 3:
                        colors.append("orange")
                    else:
                        colors.append("green")

            sns.barplot(data=filtered, x="Name", y=var, ax=ax, palette=colors)
            ax.set_ylabel(var)
            ax.set_xlabel("")
            ax.set_ylim(0, 10 if var == var_recovery else 5)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig)

        # Additional tables
        st.subheader("💧 Urine Color Alert ( > 4 )")
        urine_alert = filtered[pd.to_numeric(filtered["URINE COLOR"], errors='coerce') > 4]
        if not urine_alert.empty:
            st.dataframe(urine_alert[["Name", "URINE COLOR"]])
        else:
            st.write("No alerts today.")

        st.subheader("🦵 Muscle Discomfort Areas")
        muscle_pain = filtered[filtered["IF THE PREVIOUS ANSWER IS 1 OR 2. WHERE (LOW = L / MEDIUM = M /HIGH = H)"].notna()]
        if not muscle_pain.empty:
            st.dataframe(muscle_pain[["Name", "IF THE PREVIOUS ANSWER IS 1 OR 2. WHERE (LOW = L / MEDIUM = M /HIGH = H)"]])
        else:
            st.write("No muscle pain reported.")

        st.subheader("😴 Hours of Sleep (1-5 or 5-7)")
        sleep_hours = filtered[filtered["HOW MANY HOURS YOU SLEEP?"].isin(["1-5", "5-7"])]
        if not sleep_hours.empty:
            st.dataframe(sleep_hours[["Name", "HOW MANY HOURS YOU SLEEP?"]])
        else:
            st.write("No short sleep reported.")

# =========================
# TAB 2 – INDIVIDUAL TREND
# =========================
with tab2:
    st.sidebar.title("Player Trend Filter")
    players = ["All"] + sorted(df["Name"].dropna().unique().tolist())
    selected_player = st.sidebar.selectbox("Select Player", players)
    
    last_day = df["Date"].max()
    first_day = last_day - datetime.timedelta(days=30)
    date_range = st.sidebar.date_input("Select Date Range", [first_day, last_day])

    df_range = df[(df["Date"] >= date_range[0]) & (df["Date"] <= date_range[1])]

    if selected_player != "All":
        df_range = df_range[df_range["Name"] == selected_player]

    if df_range.empty:
        st.warning("No data available for the selected filters.")
    else:
        st.write(f"**Player:** {selected_player}")
        st.write(f"**Date Range:** {date_range[0]} to {date_range[1]}")

        for var in variables + [var_recovery]:
            st.subheader(f"📈 {var}")
            fig, ax = plt.subplots(figsize=(10, 4))
            if selected_player == "All":
                df_plot = df_range.groupby("Date")[var].mean().reset_index()
                sns.lineplot(data=df_plot, x="Date", y=var, marker="o", ax=ax)
            else:
                sns.lineplot(data=df_range, x="Date", y=var, marker="o", ax=ax)
            ax.set_ylabel(var)
            ax.set_ylim(0, 10 if var == var_recovery else 5)
            st.pyplot(fig)

        # Muscle Discomfort Table
        st.subheader("🦵 Muscle Pain Area Report")
        pain_zone = df_range[df_range["IF THE PREVIOUS ANSWER IS 1 OR 2. WHERE (LOW = L / MEDIUM = M /HIGH = H)"].notna()]
        if not pain_zone.empty:
            st.dataframe(pain_zone[["Date", "Name", "IF THE PREVIOUS ANSWER IS 1 OR 2. WHERE (LOW = L / MEDIUM = M /HIGH = H)"]])
        else:
            st.write("No muscle discomforts reported.")

        # Urine Color Alerts
        st.subheader("💧 Urine Color Alert (>4)")
        urine_indiv = df_range[pd.to_numeric(df_range["URINE COLOR"], errors='coerce') > 4]
        if not urine_indiv.empty:
            st.dataframe(urine_indiv[["Date", "Name", "URINE COLOR"]])
        else:
            st.write("No urine alerts in this period.")

        # Short Sleep Hours
        st.subheader("😴 Short Sleep Hours (1-5 / 5-7)")
        sleep_indiv = df_range[df_range["HOW MANY HOURS YOU SLEEP?"].isin(["1-5", "5-7"])]
        if not sleep_indiv.empty:
            st.dataframe(sleep_indiv[["Date", "Name", "HOW MANY HOURS YOU SLEEP?"]])
        else:
            st.write("No short sleep entries.")
