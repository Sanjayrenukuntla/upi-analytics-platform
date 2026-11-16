from pathlib import Path
import sys

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

DATA_FILE = PROJECT_DIR / "data" / "processed" / "upi_2024_2026.csv"

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="UPI Pulse | Digital Payments Intelligence",
    page_icon="💳",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #080d24;
        color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background-color: #10182f;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #172c68, #243e91);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #3556a5;
    }

    h1, h2, h3 {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df["Month"] = pd.to_datetime(df["Month"])
    df = df.sort_values("Month").reset_index(drop=True)

    numeric_columns = [
        "No. of Banks live on UPI",
        "Volume (In Mn.)",
        "Value (In Cr.)",
        "Volume Growth (%)",
        "Value Growth (%)",
        "Average Transaction Value (₹)"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


try:
    df = load_data()
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("💳 UPI Pulse")
st.sidebar.caption("India's Digital Payments Intelligence Platform")
st.sidebar.divider()

page = st.sidebar.radio(
    "Dashboard Navigation",
    [
        "Overview",
        "Transaction Trends",
        "Forecast Analysis",
        "Raw Data",
        "AI Assistant"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Data period: April 2024 – March 2026")

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("💳 UPI Pulse")
st.subheader("India's Digital Payments Intelligence Platform")
st.caption("Explore transaction activity, financial trends and predictive insights.")
st.divider()

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":

    st.header("National UPI Performance")

    total_volume = df["Volume (In Mn.)"].sum()
    total_value = df["Value (In Cr.)"].sum()

    average_value = (
        total_value / total_volume * 10
        if total_volume else 0
    )

    latest_banks = df["No. of Banks live on UPI"].iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Transactions",
        f"{total_volume / 1000:,.2f} Billion"
    )

    col2.metric(
        "Total Transaction Value",
        f"₹{total_value / 100000:,.2f} Lakh Cr"
    )

    col3.metric(
        "Average Transaction Value",
        f"₹{average_value:,.2f}"
    )

    col4.metric(
        "Banks Live on UPI",
        f"{latest_banks:,.0f}"
    )

    st.divider()

    st.subheader("Monthly Transaction Volume")

    fig = px.line(
        df,
        x="Month",
        y="Volume (In Mn.)",
        markers=True,
        title="Monthly UPI Transaction Volume"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Transaction Value")

    fig = px.line(
        df,
        x="Month",
        y="Value (In Cr.)",
        markers=True,
        title="Monthly UPI Transaction Value"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# TRANSACTION TRENDS
# --------------------------------------------------

elif page == "Transaction Trends":

    st.header("Transaction Trend Analysis")

    st.subheader("Volume and Value Growth")

    fig = px.line(
        df,
        x="Month",
        y=["Volume Growth (%)", "Value Growth (%)"],
        markers=True,
        title="Monthly Growth Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average Transaction Value")

    fig = px.line(
        df,
        x="Month",
        y="Average Transaction Value (₹)",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Banks Live on UPI")

    fig = px.line(
        df,
        x="Month",
        y="No. of Banks live on UPI",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Financial Year Comparison")

    fy_df = df.copy()

    fy_df["Financial Year"] = fy_df["Month"].apply(
        lambda date: (
            f"FY {date.year}-{str(date.year + 1)[-2:]}"
            if date.month >= 4
            else f"FY {date.year - 1}-{str(date.year)[-2:]}"
        )
    )

    yearly = (
        fy_df.groupby("Financial Year")["Volume (In Mn.)"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        yearly,
        x="Financial Year",
        y="Volume (In Mn.)",
        title="Average Monthly Transaction Volume by Financial Year"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# FORECAST ANALYSIS
# --------------------------------------------------

elif page == "Forecast Analysis":

    st.header("Forecast Analysis")

    st.info(
        "The current dataset contains 24 monthly observations. "
        "Forecasts should be treated as exploratory, not reliable "
        "long-term predictions."
    )

    from sklearn.linear_model import LinearRegression
    import numpy as np

    target = df["Volume (In Mn.)"].dropna()

    if len(target) < 6:
        st.warning("Not enough observations to build a forecast.")
    else:
        X = np.arange(len(target)).reshape(-1, 1)
        y = target.to_numpy()

        model = LinearRegression()
        model.fit(X, y)

        future_periods = 6

        future_X = np.arange(
            len(target),
            len(target) + future_periods
        ).reshape(-1, 1)

        predictions = model.predict(future_X)

        future_dates = pd.date_range(
            start=df["Month"].max() + pd.offsets.MonthBegin(1),
            periods=future_periods,
            freq="MS"
        )

        forecast_df = pd.DataFrame({
            "Month": future_dates,
            "Forecast Volume (In Mn.)": predictions
        })

        historical_df = df[["Month", "Volume (In Mn.)"]].copy()
        historical_df = historical_df.rename(
            columns={"Volume (In Mn.)": "Historical Volume (In Mn.)"}
        )

        st.subheader("Next 6 Months — Exploratory Forecast")

        fig = px.line(
            forecast_df,
            x="Month",
            y="Forecast Volume (In Mn.)",
            markers=True,
            title="Exploratory UPI Volume Forecast"
        )

        fig.add_scatter(
            x=historical_df["Month"],
            y=historical_df["Historical Volume (In Mn.)"],
            mode="lines+markers",
            name="Historical Volume"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(forecast_df, use_container_width=True)

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------

elif page == "Raw Data":

    st.header("UPI Dataset Explorer")

    search_month = st.text_input(
        "Search month (example: 2025-01)"
    )

    display_df = df.copy()

    if search_month:
        display_df = display_df[
            display_df["Month"].astype(str).str.contains(
                search_month,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Dataset",
        data=csv_data,
        file_name="upi_pulse_data.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# AI ASSISTANT
# --------------------------------------------------

elif page == "AI Assistant":

    st.header("UPI Pulse AI Assistant")

    st.write(
        "Ask questions about the information available "
        "in the UPI Pulse knowledge base."
    )

    question = st.text_input(
        "Enter your question",
        placeholder="What data period does UPI Pulse cover?"
    )

    if st.button("Generate Answer"):

        if not question.strip():
            st.warning("Please enter a question first.")

        else:
            with st.spinner(
                "Searching knowledge base and generating answer..."
            ):
                try:
                    from ai.rag_pipeline import answer_question

                    answer = answer_question(question)

                    st.subheader("AI Response")
                    st.write(answer)

                except Exception as error:
                    st.error(
                        f"Unable to generate an answer: {error}"
                    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "UPI Pulse | Built with Python, SQL, Power BI, "
    "Machine Learning and AI"
)