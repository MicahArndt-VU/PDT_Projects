# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import matplotlib.pyplot as plt

# Data Quality Checks
def check_data_quality(df):
    results = {
        "Name Masked": (df["NAME_MASKED"].str.endswith("X.")).mean(),
        "Email Hashed": (df["EMAIL_HASHED"].str.len() == 64).mean(),  # SHA-256 check
        "Phone Masked": (df["PHONE_MASKED"].str.contains("X")).mean(),
        "Address Masked": (df["ADDRESS_MASKED"] == "REDACTED").mean()
    }
    return results

@st.cache_data
def get_masked_data():
    query = "SELECT * FROM pii_mask LIMIT 1000"
    df = session.sql(query).to_pandas()
    return df

# Write directly to the app
st.title("GRDP Data Quality Monitoring")
st.write("This app monitors PII data masking to ensure GDPR compliance.")

# Get the current credentials
session = get_active_session()

df = get_masked_data()

st.write('### Data Quality Stats')
quality_results = check_data_quality(df)

# Display Pass/Fail Results
st.write("**Masking Validation Summary:**")
for field, score in quality_results.items():
    status = "✅" if score == 1.0 else "⚠️"
    st.write(f"{status} {field}: {round(score * 100, 2)}% masked correctly")

# Generate Visual Insights
st.write("### 📊 Masking Compliance Breakdown")
fig, ax = plt.subplots()
ax.bar(quality_results.keys(), [v * 100 for v in quality_results.values()], color=["blue", "green", "red", "purple"])
ax.set_ylabel("Percentage Masked Correctly")
ax.set_ylim([0, 100])
ax.set_title("Masking Accuracy by Field")
st.pyplot(fig)

# Final Compliance Message
if all(score == 1.0 for score in quality_results.values()):
    st.success("🎉 All PII fields are correctly masked!")
else:
    st.warning("⚠️ Some PII fields are not fully masked. Review the data masking rules.")

# Display Sample Data
st.write("### Sample Masked Data")
st.dataframe(df.head())


