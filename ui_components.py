import streamlit as st
import pandas as pd

def display_header():
  st.set_page_config(page_title="NPLJF Scheduler", layout="wide")          #ชื่อ tab browser
  st.title("Non-Preemptive Longest Job First (NPLJF) Scheduler")           #ชื่อหัวข้อ
  st.markdown("---")

def display_file_format_guide():                                           #คําแนะนําตาราง
  with st.expander("File Format Guide", expanded=True):
    st.write("Your Excel file should have the following columns:")
    st.write("Process, Arrival Time, Burst Time")
    st.write("Example:")
    sample_df = pd.DataFrame({
      'Process': ['P1', 'P2', 'P3', 'P4', 'P5'],
      'Arrival Time': [0, 1, 2, 3, 4],
      'Burst Time': [8, 4, 9, 5, 2]
    })
    st.dataframe(sample_df)

def display_system_metrics(matrics, total_time):                           #แสดงรายละเอียด
  st.subheader("System Metrics")
  col1, col2, col3 = st.columns(3)

  with col1:
    st.metric("CPU Utilization", f"{matrics['CPU_Utilization']:.2f}%")
    st.metric("Throughput", f"{matrics['Throughput']:.2f}")

  with col2:
    st.metric("Average Turnaround Time", f"{matrics['Avg_Turnaround_Time']:.2f}")
    st.metric("Average Waiting Time", f"{matrics['Avg_Waiting_Time']:.2f}")

  with col3:
    st.metric("Average Response Time", f"{matrics['Avg_Response_Time']:.2f}")
    st.metric("Total Time", f"{total_time:.2f}")

def display_process_details(result_df):                                    #ตารางแสดงผล
  st.subheader("Process Details")
  display_df = result_df[['Process', 'Arrival_Time', 'Burst_Time', 'Completion_Time', 'Turnaround_Time', 'Waiting_Time', 'Response_Time']]
  display_df.index = range(1, len(display_df) + 1)
  st.dataframe(display_df, use_container_width=True)

def display_individual_metrics(result_df):                                 #แสดงรายละเอียด
  st.subheader("Individual Metrics")
  col1, col2, col3 = st.columns(3)

  with col1:
    st.write("Turnaround")
    for _, row in result_df.iterrows():
      st.write(f"{row['Process']}: {row['Turnaround_Time']:.2f}")

  with col2:
    st.write("Waiting")
    for _, row in result_df.iterrows():
      st.write(f"{row['Process']}: {row['Waiting_Time']:.2f}")

  with col3:
    st.write("Response")
    for _, row in result_df.iterrows():
      st.write(f"{row['Process']}: {row['Response_Time']:.2f}")

def diaplay_gantt_chart(execution_order):                                   #แสดงลําดับการทํางานเป็นกราฟ
  st.subheader("Execution Timeline")
  timeline_text = " → ".join([F"{item['Process']}({item['Start']}-{item['End']})" 
                              for item in execution_order])
  st.code(timeline_text)

  st.write("Gantt Chart")
  gantt_html = "<div style='display: flex; align-items: center; justify-content: center;'>"
  for item in execution_order:
    width = (item['End'] - item['Start']) * 40
    gantt_html += (
      f"<div style='background-color: #90A9D7; border: 1px solid #333;"
      f"padding: 10px; margin: 2px; width: {width}px; text-align: center;'>"
      f"{item['Process']}</div>"
    )
  gantt_html += "</div>"
  st.write(gantt_html, unsafe_allow_html=True)

def display_dowload_button(result_df):                                       #ปุ่ม download
  csv = result_df.to_csv(index=False)
  st.download_button(
    label="Download CSV",
    data=csv,
    file_name="result.csv",
    mime="text/csv"
  )