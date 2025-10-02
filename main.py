import streamlit as st
import pandas as pd

#import function
from scheduler import NPLJF_scheduler, get_sample_data
from metrics import CalculateMetrics
from ui_components import (
  display_header,
  display_file_format_guide,
  display_system_metrics,
  display_process_details,
  display_individual_metrics,
  display_dowload_button,
  diaplay_gantt_chart
)

def main():
  display_header()

  # Upload file
  uploaded_file = st.file_uploader(
    "Upload Excel file with process data",
    type=['xlsx', 'xls']
  )

  display_file_format_guide()

  if st.button('Use Sample Data'):
    uploaded_file = 'sample'

  if uploaded_file:
    if uploaded_file == 'sample':
      df = get_sample_data()
      st.success('Sample data loaded!')
    else:
      try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip().str.replace(' ', '_')

        if 'Priority' in df.columns:
          df = df.drop('Priority', axis=1)

        st.success('File uploaded successfully!')
      except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return
      
    required_columns = ['Process', 'Arrival_Time', 'Burst_Time']
    if not all(col in df.columns for col in required_columns):
      st.error("Missing required columns. Required: {required_columns}")
      return

    st.subheader("Input Data")
    st.dataframe(df, use_container_width=True)

    try:
      result_df, excution_order = NPLJF_scheduler(df)
      total_time = result_df['Completion_Time'].max()
      matrics = CalculateMetrics(result_df, total_time)
    except Exception as e:
      st.error(f"Error processing file: {str(e)}")
      return
    
    st.markdown("----")

    display_system_metrics(matrics, total_time)
    st.markdown("----")
    display_process_details(result_df)
    display_individual_metrics(result_df)
    st.markdown("----")
    diaplay_gantt_chart(excution_order)
    st.markdown("----")
    display_dowload_button(result_df)
    
  else:
    st.info("Please upload an Excel file or use sample data to begin.")

  st.markdown("----")
  st.caption(
    "Non-Preemptive Longest Job First (NPLJF) Scheduler"
    " Processes are executed based on longest burst time among available processes"
  )

if __name__ == '__main__':
  main()