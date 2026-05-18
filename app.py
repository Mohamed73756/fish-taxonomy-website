import streamlit as st
import pandas as pd
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fish Taxonomy Database",
    page_icon="🐟",
    layout="wide"
)

# =====================================================
# OCEAN THEME
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #dff6ff, #ffffff);
    }

    h1, h2, h3 {
        color: #0b3d91;
    }

    .stSidebar {
        background-color: #cfefff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_excel("fish_data.xlsx")

df.columns = df.columns.str.strip()

# =====================================================
# HARD CLEAN (CRITICAL FIX FOR YOUR ISSUE)
# =====================================================

def clean(x):
    return (
        str(x)
        .replace("\xa0", " ")   # hidden non-breaking spaces
        .strip()
        .lower()
    )

for col in ["Order", "Family", "Scientific_Name", "image"]:
    df[col] = df[col].apply(clean)

# =====================================================
# WORKING COPY
# =====================================================

filtered_df = df.copy()

IMAGE_FOLDER = "images"

# =====================================================
# TITLE
# =====================================================

st.title("🐟 Marine Fish Taxonomy Database")
st.write("Browse fish species by Order and Family with images.")

# =====================================================
# DEBUG (REMOVE LATER IF YOU WANT)
# =====================================================

# st.write(df["Order"].value_counts())

# =====================================================
# ORDER FILTER
# =====================================================

order_list = ["all"] + sorted(filtered_df["Order"].unique().tolist())

selected_order = st.sidebar.selectbox("Order", order_list)

if selected_order != "all":
    filtered_df = filtered_df[
        filtered_df["Order"] == selected_order
    ]

# =====================================================
# FAMILY FILTER (DEPENDS ON ORDER)
# =====================================================

family_list = ["all"] + sorted(filtered_df["Family"].unique().tolist())

selected_family = st.sidebar.selectbox("Family", family_list)

if selected_family != "all":
    filtered_df = filtered_df[
        filtered_df["Family"] == selected_family
    ]

# =====================================================
# SEARCH
# =====================================================

search = st.sidebar.text_input("Search Scientific Name")

if search:
    filtered_df = filtered_df[
        filtered_df["Scientific_Name"].str.contains(
            search.lower(),
            case=False,
            na=False
        )
    ]

# =====================================================
# RESULTS COUNT
# =====================================================

st.success(f"{len(filtered_df)} species found")

st.divider()

# =====================================================
# DISPLAY RESULTS
# =====================================================

if len(filtered_df) == 0:
    st.warning("No fish found for this selection.")

for _, row in filtered_df.iterrows():

    col1, col2 = st.columns([1, 2])

    # -------------------------
    # IMAGE
    # -------------------------
    with col1:

        img_file = row["image"]
        img_path = os.path.join(IMAGE_FOLDER, img_file)

        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.error(f"Missing image: {img_file}")

    # -------------------------
    # INFO
    # -------------------------
    with col2:

        st.subheader(row["Scientific_Name"])

        st.write(f"**Order:** {row['Order']}")
        st.write(f"**Family:** {row['Family']}")

    st.divider()
