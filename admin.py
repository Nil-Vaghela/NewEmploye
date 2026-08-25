import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
from flask import Flask, render_template
# Read the clock-in data into a DataFrame
df = pd.read_excel('2023-05-31.xlsx')

def generate_report(df):
    report = df[['Name', 'Total Working Hours']]
    return report.to_html()

def generate_chart(df):
    chart_data = df.groupby('Name')['Total Working Hours'].sum().reset_index()

    fig = px.bar(chart_data, x='Name', y='Total Working Hours', labels={'Total Working Hours': 'Total Hours Worked'})
    chart_div = plt.plot(fig, output_type='div')

    return chart_div

app = Flask(__name__)

@app.route('/')
def home():
    report = generate_report(df)
    chart_div = generate_chart(df)
    return render_template('index.html', report=report, chart_div=chart_div)

if __name__ == '__main__':
    app.run(debug=True)
