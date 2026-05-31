import pandas as pd              # Import pandas for data loading and manipulation
import streamlit as st           # Import Streamlit for building the web app
import matplotlib.pyplot as plt  # Import Matplotlib for plotting
import seaborn as sns            # Import Seaborn for statistical visualizations

st.title("Data Loading & EDA App")   # Display the main title at the top of the app

# ----------------------------------------
# 1. FILE UPLOAD
# ----------------------------------------
uploaded = st.file_uploader("Upload your CSV")  
# Creates a file uploader widget. The uploaded file is stored in the variable "uploaded".

# A reusable function for displaying basic info
def show_basic_info(df):                    # Define a function to show data overview
    st.subheader("Basic Info")              # Display a section header
    st.write("Shape:", df.shape)            # Show number of rows and columns
    st.write("Column types:")               # Label for dtypes section
    st.write(df.dtypes)                     # Show each column’s data type
    st.write(df.describe())                 # Show basic statistics for numeric columns

# A function for missing-value report
def show_missing_values(df):                # Define a function to display missing values
    st.subheader("Missing Values")          # Section header
    st.write(df.isna().sum())               # Count missing values per column

# A function that fills numeric NaNs with mean
def fill_missing_mean(df):                  # Define a function to fill NaNs
    numeric_means = df.mean(numeric_only=True)  # Calculate means for numeric columns
    df_filled = df.fillna(numeric_means)        # Replace NaNs with column means
    return df_filled                           # Return the filled DataFrame

# A function for loops: print value counts for all categorical columns
def show_categorical_distributions(df):     # Define a function for category counts
    st.subheader("Categorical Distributions")  # Section header
    cat_cols = df.select_dtypes('object').columns  # Identify categorical columns
    for col in cat_cols:                    # Loop through each categorical column
        st.write(f"**{col}**")              # Display the column name
        st.write(df[col].value_counts())    # Show counts of each category
        st.write("---")                     # Separator line for readability

# ----------------------------------------
# 2. LOAD AND DISPLAY DATA
# ----------------------------------------
if uploaded:                                # If a file is uploaded, proceed
    df = pd.read_csv(uploaded)              # Read CSV into a DataFrame
    st.subheader("Preview")                 # Section header
    st.write(df.head())                     # Show first 5 rows of the file
    

    # categorical encoding example
    if st.checkbox("Apply one-hot encoding to categorical columns"):  # Checkbox for encoding
        df = pd.get_dummies(df)              # Apply one-hot encoding
        st.success("Applied pd.get_dummies()")  # Success message

    # Show categorical distributions using the loop function
    if st.checkbox("Show categorical value counts"):   # Checkbox to show distributions
        show_categorical_distributions(df)             # Call the loop-based function

    # ----------------------------------------
    # 4. VISUAL EDA
    # ----------------------------------------
    st.header("Visual Exploratory Data Analysis")       # Section title

    # Numeric columns list
    num_cols = df.select_dtypes('number').columns       # Extract numeric columns

    if len(num_cols) > 0:                               # If numeric data exists:

        # ---- Distribution Plot ----
        col = st.selectbox("Choose numeric column (distribution)", num_cols)  
        # Dropdown to choose column for histogram
        fig, ax = plt.subplots()                        # Create a new figure
        sns.histplot(df[col], kde=True, ax=ax)          # Histogram with KDE
        st.pyplot(fig)                                  # Display plot

        # ---- Boxplot ----
        fig, ax = plt.subplots()                        # Create a new figure
        sns.boxplot(x=df[col], ax=ax)                   # Boxplot
        st.pyplot(fig)                                  # Display plot

        # ---- Correlation Matrix ----
        corr = df.corr()                                # Compute correlation matrix
        fig, ax = plt.subplots()                        # Create a new figure
        sns.heatmap(corr, annot=False, cmap="coolwarm", ax=ax)  # Heatmap
        st.pyplot(fig)                                  # Display plot

        # ---- Scatterplot (Two variables) ----
        x = st.selectbox("X-axis", num_cols)            # Dropdown for x variable
        y = st.selectbox("Y-axis", num_cols)            # Dropdown for y variable

        fig, ax = plt.subplots()                        # Create figure
        sns.scatterplot(data=df, x=x, y=y, ax=ax)       # Scatterplot
        st.pyplot(fig)                                  # Display plot

    else:
        st.warning("No numeric columns found for visualizations.")  
        # Warning if dataset has no numeric data
