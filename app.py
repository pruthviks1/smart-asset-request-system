import streamlit as st
import pandas as pd
import uuid
import datetime

# Simulated database file
DB_FILE = "requests.csv"

# Initialize CSV if not exists
def init_db():
    try:
        pd.read_csv(DB_FILE)
    except:
        df = pd.DataFrame(columns=["Request ID", "Asset", "Justification", "Status", "Submitted At"])
        df.to_csv(DB_FILE, index=False)

# Submit a new asset request
def submit_request(asset, justification):
    df = pd.read_csv(DB_FILE)
    request_id = str(uuid.uuid4())[:8]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = {
        "Request ID": request_id,
        "Asset": asset,
        "Justification": justification,
        "Status": "Pending Approval",
        "Submitted At": now
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return request_id

# Simulated admin approval
def approve_request(request_id):
    df = pd.read_csv(DB_FILE)
    df.loc[df["Request ID"] == request_id, "Status"] = "Approved ✅"
    df.to_csv(DB_FILE, index=False)

# Email simulation
def send_email(to, subject, body):
    st.info(f"📧 Email sent to {to}: {subject}\n{body}")

# Streamlit UI
st.title("📦 Smart IT Asset Request System")
st.markdown("""
    <style>
        .reportview-container {
            background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
            padding: 2rem;
        }
        .sidebar .sidebar-content {
            background-color: #e0f7fa;
        }
        .stButton>button {
            background-color: #009688;
            color: white;
            padding: 0.5em 1em;
            border-radius: 8px;
            font-weight: bold;
        }
        .stSelectbox>div {
            border-radius: 8px;
        }
        .stTextArea>div>textarea {
            border-radius: 8px;
        }
        .stDataFrame {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)


init_db()

menu = st.sidebar.radio("Menu", ["Submit Request", "Dashboard (Admin Mode)"])

if menu == "Submit Request":
    st.header("📝 Request a New Asset")

    asset = st.selectbox("Select Asset", ["Laptop - Dell", "Headphones", "Software License", "Monitor"])
    justification = st.text_area("Justification")

    if st.button("Submit Request"):
        if asset and justification:
            request_id = submit_request(asset, justification)
            st.success(f"Request Submitted ✅ ID: {request_id}")
            send_email("approver@company.com", "New Asset Request", f"Request ID: {request_id} needs approval.")
        else:
            st.error("Please fill out all fields.")

elif menu == "Dashboard (Admin Mode)":
    st.header("🛠️ Admin Dashboard")
    df = pd.read_csv(DB_FILE)
    st.dataframe(df)

    pending = df[df["Status"] == "Pending Approval"]

    if not pending.empty:
        request_to_approve = st.selectbox("Select Request ID to Approve", pending["Request ID"].tolist())
        if st.button("Approve Selected Request"):
            approve_request(request_to_approve)
            st.success(f"✅ Approved Request: {request_to_approve}")
            send_email("user@company.com", "Request Approved", f"Your request {request_to_approve} has been approved.")
    else:
        st.info("✅ No pending approvals.")
