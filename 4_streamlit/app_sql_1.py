import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "app.db"

# ------------- DATABASE HELPERS -------------

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table (VERY SIMPLE - plain text passwords, just for demo!)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Table to log user actions (clicks, events, etc.)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            ts TEXT NOT NULL
        )
    """)

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
        # username already exists
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

def log_action(username, action):
    conn = get_connection()
    cur = conn.cursor()
    ts = datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO user_actions (username, action, ts) VALUES (?, ?, ?)",
        (username, action, ts)
    )
    conn.commit()
    conn.close()

def get_user_actions(username=None):
    conn = get_connection()
    cur = conn.cursor()
    if username:
        cur.execute(
            "SELECT username, action, ts FROM user_actions WHERE username = ? ORDER BY id DESC",
            (username,)
        )
    else:
        cur.execute(
            "SELECT username, action, ts FROM user_actions ORDER BY id DESC"
        )
    rows = cur.fetchall()
    conn.close()
    return rows

# ------------- UI HELPERS -------------

def show_login_page():
    st.title("Login")

    tab_login, tab_register = st.tabs(["Sign in", "Register"])

    with tab_login:
        st.subheader("Sign in")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if verify_user(login_user, login_pass):
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_user
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


def show_dashboard():
    username = st.session_state.get("username", "unknown")

    st.title("📊 Demo Dashboard")
    st.write(f"Logged in as **{username}**")

    # Top row: some dummy KPI cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Clicks (all users)", get_total_clicks())
    with col2:
        st.metric("Your Clicks", get_user_click_count(username))
    with col3:
        st.metric("Unique Users", get_unique_user_count())

    st.markdown("---")

    st.subheader("Actions")

    col_a, col_b, col_c = st.columns(3)

    # Buttons that log user actions
    with col_a:
        if st.button("👍 Like dashboard"):
            log_action(username, "like_dashboard")
            st.success("Thanks for the like!")
    with col_b:
        if st.button("📥 Download report (fake)"):
            log_action(username, "download_report")
            st.info("In a real app, a report file would be generated.")
    with col_c:
        if st.button("📈 View analytics section"):
            log_action(username, "view_analytics")
            st.info("Analytics section opened (imaginary).")

    st.markdown("---")
    st.subheader("Your recent activity")

    rows = get_user_actions(username)
    if rows:
        df = pd.DataFrame(rows, columns=["Username", "Action", "Timestamp (UTC)"])
        st.dataframe(df)
    else:
        st.info("No actions logged yet. Click some buttons above!")

    st.markdown("---")
    st.subheader("All users' activity (admin-style view)")

    all_rows = get_user_actions()
    if all_rows:
        df_all = pd.DataFrame(all_rows, columns=["Username", "Action", "Timestamp (UTC)"])
        st.dataframe(df_all)
    else:
        st.info("No activity logged in the system yet.")


def get_total_clicks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM user_actions")
    (count,) = cur.fetchone()
    conn.close()
    return count

def get_user_click_count(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM user_actions WHERE username = ?", (username,))
    (count,) = cur.fetchone()
    conn.close()
    return count

def get_unique_user_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT username) FROM user_actions")
    (count,) = cur.fetchone()
    conn.close()
    return count

# ------------- MAIN APP -------------

def main():
    st.set_page_config(page_title="SQL + Streamlit Demo", layout="wide")
    init_db()

    # Simple navbar area
    with st.sidebar:
        st.header("Menu")
        if "logged_in" in st.session_state and st.session_state["logged_in"]:
            st.write(f"👤 {st.session_state['username']}")
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                st.session_state["username"] = None
                st.rerun()
        else:
            st.write("Not logged in")

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        show_login_page()
    else:
        show_dashboard()


if __name__ == "__main__":
    main()
