import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Data Explorer: Tabs + 4-Section Layout",
    layout="wide"
)

# ------------------------------------------------------------
# Title and description
# ------------------------------------------------------------
st.title("Data Explorer")
st.caption(
    "Each tab is divided into four sections: overview, missingness, "
    "data types, and distributions for continuous & categorical variables."
)

# ------------------------------------------------------------
# File upload
# ------------------------------------------------------------
uploaded = st.file_uploader("Upload your CSV file")

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def panel_overview(df, n_head: int):
    """Tab: Overview – 4 sections."""
    st.subheader("Overview")

    col1, col2 = st.columns(2)

    # Top-left: Shape + basic info
    with col1:
        st.markdown("#### 1️⃣ Shape & Basic Info")
        st.write("Number of rows:", df.shape[0])
        st.write("Number of columns:", df.shape[1])

        st.write("**First few rows**")
        st.dataframe(df.head(n_head))

    # Top-right: Column names
    with col2:
        st.markdown("#### 2️⃣ Column Names")
        st.write(list(df.columns))

    # Bottom row – reuse columns
    col3, col4 = st.columns(2)

    # Bottom-left: Summary of numeric columns
    with col3:
        st.markdown("#### 3️⃣ Numeric Summary (describe)")
        num_df = df.select_dtypes(include="number")
        if not num_df.empty:
            st.dataframe(num_df.describe())
        else:
            st.info("No numeric columns found.")

    # Bottom-right: Summary of non-numeric columns
    with col4:
        st.markdown("#### 4️⃣ Categorical Summary (describe)")
        cat_df = df.select_dtypes(exclude="number")
        if not cat_df.empty:
            st.dataframe(cat_df.describe(include="all"))
        else:
            st.info("No categorical/non-numeric columns found.")


def panel_missing_and_types(df):
    """Tab: Missing + dtypes – 4 sections."""
    st.subheader("Missing Values & Data Types")

    col1, col2 = st.columns(2)

    # Top-left: Missing counts
    with col1:
        st.markdown("#### 1️⃣ Missing Values (Count)")
        missing_count = df.isna().sum().to_frame("missing_count")
        st.dataframe(missing_count)

    # Top-right: Missing percentages
    with col2:
        st.markdown("#### 2️⃣ Missing Values (%)")
        missing_pct = (df.isna().mean() * 100).to_frame("missing_%")
        st.dataframe(missing_pct.style.format("{:.2f}"))

    col3, col4 = st.columns(2)

    # Bottom-left: Data types
    with col3:
        st.markdown("#### 3️⃣ Data Types")
        dtypes_df = df.dtypes.to_frame("dtype")
        st.dataframe(dtypes_df)

    # Bottom-right: Unique counts per column
    with col4:
        st.markdown("#### 4️⃣ Unique Values per Column")
        unique_counts = df.nunique().to_frame("n_unique")
        st.dataframe(unique_counts)


def panel_continuous(df, bins: int):
    """Tab: All continuous variables histograms – arranged in sections."""
    st.subheader("Continuous Variables – Histograms")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    if not num_cols:
        st.info("No numeric (continuous) columns found.")
        return

    st.markdown("Showing histograms for **all numeric columns**.")

    # We’ll arrange plots in 2 columns; every pair of columns = 1 'row'
    for i, col in enumerate(num_cols):
        if i % 2 == 0:
            col_left, col_right = st.columns(2)

        target_col = col_left if i % 2 == 0 else col_right

        with target_col:
            st.markdown(f"##### {col}")
            data = df[col].dropna()
            if data.empty:
                st.write("No non-missing data in this column.")
                continue

            fig, ax = plt.subplots()
            ax.hist(data, bins=bins)
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            st.pyplot(fig)


def panel_categorical(df, top_n: int):
    """Tab: All categorical variables bar plots – arranged in sections."""
    st.subheader("Categorical Variables – Bar Plots")

    cat_cols = df.select_dtypes(exclude="number").columns.tolist()
    if not cat_cols:
        st.info("No categorical columns found.")
        return

    st.markdown(
        f"Showing bar plots for **all categorical columns** "
        f"(top {top_n} categories by frequency)."
    )

    for i, col in enumerate(cat_cols):
        if i % 2 == 0:
            col_left, col_right = st.columns(2)

        target_col = col_left if i % 2 == 0 else col_right

        with target_col:
            st.markdown(f"##### {col}")
            vc = df[col].value_counts().head(top_n)

            if vc.empty:
                st.write("No data in this column.")
                continue

            fig, ax = plt.subplots()
            ax.bar(vc.index.astype(str), vc.values)
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)


# ------------------------------------------------------------
# Main logic
# ------------------------------------------------------------
if uploaded:
    df = pd.read_csv(uploaded)

    # Sidebar controls that affect multiple tabs
    st.sidebar.header("Display Controls")

    # Number of rows in preview
    max_rows = len(df)
    default_rows = min(10, max_rows) if max_rows > 0 else 5
    n_head = st.sidebar.slider(
        "Rows in preview (head)",
        min_value=1,
        max_value=max(1, max_rows),
        value=max(1, default_rows),
    )

    # Bins for continuous histograms
    bins = st.sidebar.slider(
        "Number of bins (continuous histograms)",
        min_value=5,
        max_value=50,
        value=20,
    )

    # Top categories for bar plots
    top_n = st.sidebar.slider(
        "Top N categories (categorical bar plots)",
        min_value=3,
        max_value=30,
        value=10,
    )

    # --------------------------------------------------------
    # Tabs – each visually divided into 4 sections
    # --------------------------------------------------------
    tab_overview, tab_missing, tab_continuous, tab_categorical = st.tabs(
        ["Overview", "Missing & Types", "Continuous", "Categorical"]
    )

    with tab_overview:
        panel_overview(df, n_head)

    with tab_missing:
        panel_missing_and_types(df)

    with tab_continuous:
        panel_continuous(df, bins)

    with tab_categorical:
        panel_categorical(df, top_n)

else:
    st.info("Upload a CSV file to explore it in the tabs.")
