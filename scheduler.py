import pandas as pd

def NPLJF_scheduler(processes):               #ฟังก์ชันหลักในการคํานวน NPLJF

  n = len(processes)                 #นับจํานวน process
  processes = processes.copy()       #copy ข้อมูลมาใส่ใน processes

                                     #สร้างคอลัมน์ใหม่เพื่อเตรียมเก็บข้อมูล
  processes['Completion_Time'] = 0
  processes['Turnaround_Time'] = 0
  processes['Waiting_Time'] = 0
  processes['Response_Time'] = 0

  completed = [False] * n            #สร้าง list เพื่อเก็บสถานะของข้อมูลว่าเสร็จแล้ว (True) หรือยัง (False)
  current_time = 0                   #เวลาปัจจุบันของ CPU
  completed_count = 0                #จํานวน process ที่เสร็จ

  execution_order = []               #เก็บลําดับการทํางาน

  while completed_count < n:         #ลูปการทํางาน
    available = []                   #สร้าง list เพื่อเก็บ process ที่สามารถทํางานได้
    for i in range(n):
      if not completed[i] and processes['Arrival_Time'][i] <= current_time:
        available.append(i)
    """
    ลูปเช็คเงื่อนไข process ทุกตัว ถ้า process นั้นยังไม่เสร็จและมาถึงเวลาปัจจุบันแล้ว
    ให้เพิ่ม process นั้นลงใน list available
    """

    if not available:
      current_time = processes[~completed]['Arrival_Time'].min()
      continue
    """
    ถ้าไม่มี process ที่สามารถทํางานได้
    ให้กระโดดไปหา process ที่จะมาถึงถัดไป
    """

    longest_jop = max(available, key=lambda i: processes.iloc[i]['Burst_Time'])     #หาค่า Burst_Time ที่มากที่สุด
    
    process = processes.iloc[longest_jop]       #ดึงข้อมูล process ที่เลือกมาทํา
    start_time = current_time                   #บันทึกเวลาเริ่มการทํางาน
    current_time += process['Burst_Time']       #บวกเวลาในการทํางาน

    processes.at[longest_jop, 'Completion_Time'] = current_time                                #เวลาที่ทํา Process นั้นเสร็จ
    processes.at[longest_jop, 'Turnaround_Time'] = current_time - process['Arrival_Time']      #เวลาที่ใช้ในการทํา Process นั้น
    processes.at[longest_jop, 'Waiting_Time'] = (                                              #เวลาที่รอในการทํา Process นั้น
        processes.at[longest_jop, 'Turnaround_Time'] - process['Burst_Time']
    )
    processes.at[longest_jop, 'Response_Time'] = start_time - process['Arrival_Time']          #เวลาตั้งแต่มาจนถึงเริ่มทํา Process นั้นครั้งแรก

    completed[longest_jop] = True               #เปลี่ยนสถานะของ process นั้นเป็นเสร็จ (True)
    completed_count += 1                        #เพิ่มจํานวน process ที่เสร็จ
    execution_order.append({                    #เก็บลําดับการทํางานของ process
        'Process': longest_jop + 1,
        'Start': start_time,
        'End': current_time
    })
    

  return processes, execution_order             #คืนค่า process และลําดับการทํางาน

#ข้อมูลตัวอย่าง
def get_sample_data():
  return pd.DataFrame({
      'Process': ['P1', 'P2', 'P3', 'P4', 'P5'],
      'Arrival_Time': [0, 1, 2, 3, 4],
      'Burst_Time': [8, 4, 9, 5, 2]
  })