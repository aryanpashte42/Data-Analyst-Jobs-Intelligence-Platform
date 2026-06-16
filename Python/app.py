import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Data Analyst Job Market Dashboard",
    layout="wide"
)

st.title("📊 Data Analyst Job Market Intelligence Dashboard")

df = pd.read_csv("cleaned_data.csv")

st.sidebar.header("Filters")

selected_location = st.sidebar.selectbox(
    "Location",
    ["All"] + sorted(df['Location'].dropna().unique().tolist())
)

selected_industry = st.sidebar.selectbox(
    "Industry",
    ["All"] + sorted(df['Industry'].dropna().unique().tolist())
)

filtered_df = df.copy()

if selected_location != "All":
    filtered_df = filtered_df[
        filtered_df['Location'] == selected_location
    ]

if selected_industry != "All":
    filtered_df = filtered_df[
        filtered_df['Industry'] == selected_industry
    ]

total_jobs = len(filtered_df)

avg_salary = round(
    filtered_df['AvgSalary'].mean(),2
)

remote_jobs = filtered_df['Remote'].sum()

skill_salary = {

    'Python':
    filtered_df[
        filtered_df['Python']==1
    ]['AvgSalary'].mean(),

    'SQL':
    filtered_df[
        filtered_df['SQL']==1
    ]['AvgSalary'].mean(),

    'Power BI':
    filtered_df[
        filtered_df['Power BI']==1
    ]['AvgSalary'].mean(),

    'Tableau':
    filtered_df[
        filtered_df['Tableau']==1
    ]['AvgSalary'].mean()
}

highest_skill = max(
    skill_salary,
    key=skill_salary.get
)

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Jobs", total_jobs)

col2.metric(
    "Average Salary",
    f"${avg_salary:.0f}K"
)

col3.metric(
    "Remote Jobs",
    remote_jobs
)

col4.metric(
    "Highest Paying Skill",
    highest_skill
)


st.subheader("Demand For Skills")

skill_demand = pd.DataFrame({

'Skill':['Python','SQL','Power BI','Tableau'],

'Count':[

filtered_df['Python'].sum(),

filtered_df['SQL'].sum(),

filtered_df['Power BI'].sum(),

filtered_df['Tableau'].sum()
]
})

fig,ax = plt.subplots(figsize=(8,4))

sns.barplot(
data=skill_demand,
x='Skill',
y='Count',
ax=ax
)

st.pyplot(fig)

st.subheader("Highest Paying Skills")

skills_salary = pd.DataFrame({

'Skill':['Python','SQL','Power BI','Tableau'],

'Salary':[

filtered_df[
filtered_df['Python']==1
]['AvgSalary'].mean(),

filtered_df[
filtered_df['SQL']==1
]['AvgSalary'].mean(),

filtered_df[
filtered_df['Power BI']==1
]['AvgSalary'].mean(),

filtered_df[
filtered_df['Tableau']==1
]['AvgSalary'].mean()
]
})

fig,ax = plt.subplots(figsize=(8,4))

sns.barplot(
data=skills_salary,
x='Skill',
y='Salary',
ax=ax
)

st.pyplot(fig)

st.subheader("Salary Distribution")

fig,ax = plt.subplots(figsize=(10,4))

sns.histplot(
filtered_df['AvgSalary'],
bins=30,
kde=True,
ax=ax
)

st.pyplot(fig)

st.subheader("Remote vs Non Remote Jobs")

remote_data = filtered_df['Remote'].value_counts()

label_map = {
    0: 'Non Remote',
    1: 'Remote'
}

labels = [label_map.get(x, str(x)) for x in remote_data.index]

fig, ax = plt.subplots()

ax.pie(
    remote_data,
    labels=labels,
    autopct='%1.1f%%'
)

ax.set_title("Distribution of Remote and Non-Remote Jobs")

st.pyplot(fig)

st.subheader("Top Hiring Locations")

top_locations = (
filtered_df['Location']
.value_counts()
.head(10)
)

fig,ax = plt.subplots(figsize=(10,5))

top_locations.plot(
kind='barh',
ax=ax
)

st.pyplot(fig)

st.subheader("Top Hiring Companies")

top_companies = (
filtered_df['Company Name']
.value_counts()
.head(10)
)

fig,ax = plt.subplots(figsize=(10,5))

top_companies.plot(
kind='barh',
ax=ax
)

st.pyplot(fig)

st.subheader("Highest Paying Industries")

industry_salary = (

filtered_df
.groupby('Industry')['AvgSalary']
.mean()
.sort_values(
ascending=False
)
.head(10)

)

fig,ax = plt.subplots(figsize=(10,5))

industry_salary.plot(
kind='bar',
ax=ax
)

st.pyplot(fig)

st.subheader("Rating vs Salary")

fig,ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
data=filtered_df,
x='Rating',
y='AvgSalary',
ax=ax
)

st.pyplot(fig)

st.subheader("Company Size vs Salary")

size_salary = (

filtered_df
.groupby('Size')['AvgSalary']
.mean()
.sort_values(
ascending=False
)
.head(10)

)

fig,ax = plt.subplots(figsize=(12,5))

size_salary.plot(
kind='bar',
ax=ax
)

st.pyplot(fig)

st.subheader("Python + SQL Demand")

python_sql = len(

filtered_df[

(filtered_df['Python']==1)

&

(filtered_df['SQL']==1)

]

)

st.metric(
"Jobs Requiring Python + SQL",
python_sql
)

st.subheader("Python + SQL Average Salary")

python_sql_salary = (

filtered_df[

(filtered_df['Python']==1)

&

(filtered_df['SQL']==1)

]['AvgSalary']

.mean()

)

st.metric(
"Average Salary",
f"${python_sql_salary:.0f}K"
)