import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    df = pd.read_csv("students_data.csv")
except FileNotFoundError:
    st.error("Error: 'students_data.csv' not found. Using mock data for demonstration.")
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Fiona', 'George', 'Hannah', 'Ian', 'Jasmine'],
        'Course': ['Math', 'Science', 'Math', 'English', 'Science', 'Math', 'English', 'Science', 'Math', 'English'],
        'City': ['New York', 'Los Angeles', 'New York', 'Chicago', 'Los Angeles', 'New York', 'Chicago', 'Los Angeles', 'New York', 'Chicago'],
        'Gender': ['Female', 'Male', 'Male', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female'],
        'Marks': [95, 82, 78, 91, 65, 88, 72, 98, 55, 85],
        'Attendance (%)': [98, 85, 76, 92, 60, 90, 75, 99, 50, 88]
    }
    df = pd.DataFrame(data)

st.title("🎓 Student Performance Dashboard")
st.markdown("A comprehensive view of student performance, filterable by various criteria.")

st.sidebar.header("⚙️ Filter Controls")

course_filter = st.sidebar.selectbox(
    "Select Course", 
    options=["All"] + list(df["Course"].unique())
)
city_filter = st.sidebar.multiselect(
    "Filter by City", 
    options=["All"] + list(df["City"].unique()),
    # default=df["City"].unique()
)
min_marks = st.sidebar.slider(
    "Minimum Marks", 
    min_value=0, 
    max_value=100, 
    value=0
)
gender_filter = st.sidebar.radio(
    "Gender", 
    ["All", "Male", "Female"],
    horizontal=True
)

filtered_df = df.copy()
if course_filter != "All":
    filtered_df = filtered_df[filtered_df["Course"] == course_filter]
filtered_df = filtered_df[(filtered_df["City"].isin(city_filter))]
filtered_df = filtered_df[(filtered_df["Marks"] >= min_marks)]
if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust the filters. 🧐")
    st.stop()

st.header("✨ Key Performance Indicators")
col1, col2, col3 = st.columns(3)

avg_marks = round(filtered_df["Marks"].mean(), 2)
avg_attendance = round(filtered_df["Attendance (%)"].mean(), 2)
total_students = filtered_df.shape[0]

with col1:
    st.metric("Total Students", total_students)
with col2:
    st.metric("Average Marks", avg_marks)
with col3:
    st.metric("Average Attendance (%)", avg_attendance)

st.markdown("---")
if avg_marks > 85:
    st.balloons()
    st.success("🎉 **Excellent performance!** The average marks are above 85. Keep up the great work! 🏆")
elif avg_marks >= 70:
    st.info("🙂 **Good performance.** The average marks are between 70 and 85.")
else:
    st.warning("📉 **Needs improvement.** The average marks are below 70. Consider reviewing study plans.")
st.markdown("---")

st.header("📊 Performance Visualizations")
tab1, tab2, tab3 = st.tabs(["Marks & Attendance Overview", "Marks Distribution", "Detailed Data"])

with tab1:
    st.subheader("Marks and Attendance by Student")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("**Marks by Student**")
        marks_chart_df = filtered_df.set_index("Name")["Marks"].sort_values(ascending=False)
        st.bar_chart(marks_chart_df)
    with chart_col2:
        st.markdown("**Attendance Trend (%)**")
        attendance_chart_df = filtered_df.set_index("Name")["Attendance (%)"].sort_values(ascending=False)
        st.line_chart(attendance_chart_df)

with tab2:
    st.subheader("Marks Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(filtered_df["Marks"], bins=10, color='#1f77b4', edgecolor='white', alpha=0.7)
    ax.set_title("Distribution of Student Marks")
    ax.set_xlabel("Marks")
    ax.set_ylabel("Number of Students")
    ax.grid(axis='y', alpha=0.5)
    st.pyplot(fig)

with tab3:
    st.subheader("Filtered Student Data Table")
    st.dataframe(filtered_df, use_container_width=True)

st.header("🎯 Quick Actions and Search")
search_col, top_col, all_col = st.columns([3, 1, 1])

with search_col:
    st.markdown("**🔍 Search Student by Name**")
    search_name = st.text_input("Enter student name", label_visibility="collapsed")
    if search_name:
        result = df[df["Name"].str.contains(search_name, case=False, na=False)]
        if not result.empty:
            st.table(result)
        else:
            st.error("No student found with this name 👀")

with top_col:
    st.markdown("**Top Performers**")
    if st.button("Show Top Performers 🏅", use_container_width=True):
        top_students = df[df["Marks"] > 90].sort_values(by="Marks", ascending=False)
        st.success("Showing all students with Marks > 90!")
        st.dataframe(top_students, use_container_width=True)

with all_col:
    st.markdown("**Full Dataset**")
    if st.button("Show All Data 📖", use_container_width=True):
        st.dataframe(df, use_container_width=True)
