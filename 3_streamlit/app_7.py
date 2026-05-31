import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Page configuration (title, layout, favicon, etc.)
# ------------------------------------------------------------
st.set_page_config(
    page_title="Layout 1: Sidebar Controls + Top Navigation",
    layout="wide"
)

# ------------------------------------------------------------
# Page title and description
# ------------------------------------------------------------
st.title("Layout 1: Sidebar Controls + Top Navigation")
st.caption(
    "Sidebar is used to control the data view: number of rows in preview, "
    "and which column to use for a histogram (e.g. Titanic dataset)."
)

st.subheader("4-Panel Data Overview (2×2 Grid)")

# ------------------------------------------------------------
# File upload widget
# ------------------------------------------------------------
uploaded = st.file_uploader("Upload your CSV (e.g. Titanic)")

# ------------------------------------------------------------
# Helper panel functions
# ------------------------------------------------------------

def show_basic_info(df):
    """Display the DataFrame's shape and data types."""
    st.write("### Basic Info")
    st.write("Shape:", df.shape)
    st.write(df.dtypes)

def show_preview(df, n_rows=5):
    """Show the first N rows of the DataFrame."""
    st.write(f"### Data Preview (first {n_rows} rows)")
    st.write(df.head(n_rows))

def show_missing(df):
    """Show the count of missing values for each column."""
    st.write("### Missing Values")
    st.write(df.isna().sum())

def show_histogram(df, column, bins=20):
    """Plot a histogram for a selected numeric column."""
    st.write(f"### Histogram: {column}")

    # Drop missing values so histogram can be generated cleanly
    data = df[column].dropna()
    if data.empty:
        st.write("No non-missing values in this column.")
        return

    # Create histogram using Matplotlib
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)
    ax.set_xlabel(column)
    ax.set_ylabel("Count")

    # Display histogram in Streamlit
    st.pyplot(fig)

# ------------------------------------------------------------
# When a file is uploaded, load data and show controls + panels
# ------------------------------------------------------------
if uploaded:
    df = pd.read_csv(uploaded)

    # -----------------------------
    # Sidebar controls panel
    # -----------------------------
    st.sidebar.header("Display Controls")

    # Slider to choose how many rows are shown in the preview
    max_rows = len(df)
    default_rows = min(10, max_rows) if max_rows > 0 else 0
    n_head = st.sidebar.slider(
        "Number of rows in preview (head)",
        min_value=1,
        max_value=max(1, max_rows),
        value=max(1, default_rows),
    )

    # Histogram column selector (only numeric columns allowed)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    hist_column = None
    bins = 20

    if numeric_cols:
        # Choose which numeric column to plot
        hist_column = st.sidebar.selectbox(
            "Column for histogram",
            options=numeric_cols,
            index=0,
        )

        # Choose number of bins in histogram
        bins = st.sidebar.slider(
            "Number of bins",
            min_value=5,
            max_value=50,
            value=20,
        )
    else:
        st.sidebar.info("No numeric columns found for histogram.")

    # ------------------------------------------------------------
    # Create a *true* 2-column layout for a clean 2×2 look
    # ------------------------------------------------------------
    left_col, right_col = st.columns(2)

    # -----------------------------
    # LEFT column panels (stacked)
    # -----------------------------
    with left_col:
        show_preview(df, n_rows=n_head)        # top-left panel
        show_basic_info(df)                    # bottom-left panel

    # -----------------------------
    # RIGHT column panels (stacked)
    # -----------------------------
    with right_col:
        show_missing(df)                       # top-right panel

        # Bottom-right panel (histogram), only if numeric column exists
        if hist_column:
            show_histogram(df, hist_column, bins=bins)
        else:
            st.info("No numeric column available for histogram.")

else:
    # Message shown when no file is uploaded yet
    st.info("Upload a CSV file (e.g. Titanic) to see the 4-panel overview and controls.")
