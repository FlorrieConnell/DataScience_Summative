import pandas as pd
import numpy as np 
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from shiny import App, render, ui, render, reactive

# Load attendance data
df = pd.read_csv("/Users/user/data_science/datascience/summative/attendance_anonymised-1.csv")
df.rename(columns={"Unit Instance Code": "Module Code", 
                   "Calocc Code": "Year", "Long Description": "Module Name", 
                   "Register Event ID": "Event ID",
                   "Register Event Slot ID": "Event Slot ID",
                   "Planned Start Date": "Date",
                   "is Positive": "Has Attended",
                   "Positive Marks": "Attended",
                   "Negative Marks": "NotAttended",
                   "Usage Code": "Attendance Code"}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
history_df = df[df['Module Name']=='History']
history_df['Has Attended'] = history_df['Has Attended'].replace({'Y':'1', 'N':'0', '~':'0'}).astype(int)
history_df = history_df.dropna()


# UI
app_ui = ui.page_fluid(
    ui.h1("Attendance Data Dashboard"),
    ui.input_slider("slider1", "Attendance Levels", min=0, max=1, step=0.05, value=0.5, animate=True),
    ui.h2("Attendance Over Time"),
    ui.output_plot('attendance_plot')
)

def server(input, output, session):
    @output
    @render.plot(alt="Attendance Histogram")
    def attendance_plot():
        history_df = df[df['Module Name']=='History']
        attendance_time = (history_df.groupby('Date')['Has Attended'].mean().reset_index())
        fig, ax = plt.subplots()
        sns.lineplot(data=attendance_time, x='Date', y='Has Attended' , ax=ax)
        #ax.plot(pd.to_datetime(df['Date']), df['Has Attended'], marker='o', linestyle='')
        ax.set_title('Attendance Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Attendance Rate')
        fig.autofmt_xdate()
        return fig
    
app = App(app_ui, server)