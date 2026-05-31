import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="SQL + Login + EDA",
    layout="wide"
)

DB_PATH = "app.db"

# ============================================================
# SQL / AUTH LAYER
# ============================================================

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Very simple demo users table (plain text passwords!)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Base definition of user_actions table (for fresh DBs)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            ts TEXT NOT NULL
        )
    """)

    # --- Ensure 'details' column exists (handles old DBs) ---
    cur.execute("PRAGMA table_info(user_actions)")
    columns = [row[1] for row in cur.fetchall()]
    if "details" not in columns:
        cur.execute("ALTER TABLE user_actions ADD COLUMN details TEXT")

    conn.commit()
    conn.close()

def create_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    row = cur.fetchone()
    conn.close()
    return row is not None

def log_action(username, action, details=None):
    conn = get_connection()
    cur = conn.cursor()
    ts = datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO user_actions (username, action, details, ts) VALUES (?, ?, ?, ?)",
        (username, action, details, ts)
    )
    conn.commit()
    conn.close()

# ============================================================
# LOGIN / REGISTER UI
# ============================================================

def show_login_page():
    st.title("🔐 Login to EDA App")

    tab_login, tab_register = st.tabs(["Sign in", "Register"])

    with tab_login:
        st.subheader("Sign in")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if verify_user(login_user, login_pass):
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_user
                log_action(login_user, "login_success")
                st.success(f"Welcome, {login_user}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab_register:
        st.subheader("Create new account")
        new_user = st.text_input("New username", key="new_user")
        new_pass = st.text_input("New password", type="password", key="new_pass")
        if st.button("Register"):
            if not new_user or not new_pass:
                st.error("Username and password cannot be empty")
            else:
                ok = create_user(new_user, new_pass)
                if ok:
                    st.success("Account created! You can now log in.")
                else:
                    st.error("Username already exists")

# ============================================================
# EDA PANELS (your layout, wrapped in functions)
# ============================================================

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

    # Arrange plots in 2 columns; every pair of columns = 1 'row'
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

# ============================================================
# MAIN EDA APP (only shown after login)
# ============================================================

def show_eda_app(username: str):
    st.title("📊 Data Explorer")
    st.caption(
        "Each tab is divided into four sections: overview, missingness, "
        "data types, and distributions for continuous & categorical variables."
    )

    st.markdown(f"Logged in as **{username}**")

    # File upload
    uploaded = st.file_uploader("Upload your CSV file")

    if uploaded:
        # Log upload once per file name
        log_action(username, "upload_csv", details=uploaded.name)

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

        # Optional button to log an explicit "analysis saved" action
        if st.sidebar.button("💾 Save analysis snapshot"):
            log_action(
                username,
                "save_snapshot",
                details=f"rows={len(df)}, cols={len(df.columns)}"
            )
            st.sidebar.success("Snapshot saved in SQL log.")

        # Tabs – each visually divided into 4 sections
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

# ============================================================
# MAIN
# ============================================================

def main():
    init_db()

    # Sidebar menu / logout
    with st.sidebar:
        st.header("User")
        if "logged_in" in st.session_state and st.session_state["logged_in"]:
            st.write(f"👤 {st.session_state['username']}")
            if st.button("Logout"):
                log_action(st.session_state["username"], "logout")
                st.session_state["logged_in"] = False
                st.session_state["username"] = None
                st.rerun()
        else:
            st.write("Not logged in")

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        show_login_page()
    else:
        show_eda_app(st.session_state["username"])

if __name__ == "__main__":
    main()
