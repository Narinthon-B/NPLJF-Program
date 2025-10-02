def CalculateMetrics(process, total_time):
  n = len(process)                              #นับจํานวน process ทั้งหมด
  total_burst = process['Burst_Time'].sum()     #ผลรวมของเวลาที่ CPU ทํางาน

  metrics = {
    'CPU_Utilization': (total_burst / total_time * 100) if total_time > 0 else 0,     #หา % การทํางานของ CPU ((เวลาที่ CPU ทำงานจริง / เวลาทั้งหมด) × 100%)
    'Throughput': n / total_time if total_time > 0 else 0,                            #หาจํานวน process ที่ทํางานเสร็จต่อวินาที (จำนวน process / เวลาทั้งหมด)
    'Avg_Turnaround_Time': process['Turnaround_Time'].mean(),                         #เวลาที่ใช้ในการรัน process ทั้งหมด
    'Avg_Waiting_Time': process['Waiting_Time'].mean(),                               #เวลาที่ process อยู่ใน queue
    'Avg_Response_Time': process['Response_Time'].mean()                              #เวลาที่ใช้ตั้งแต่ส่งคําขอจนถึงการตอบสนองครั้งแรก
  }

  return metrics

def get_individual_matrics(process):                                                  #จัดกลุ่ม metrics ของ process ทั้งหมด
  return {
    'Turnaround': process[['Process', 'Turnaround_Time']].to_dict('records'),
    'Waiting': process[['Process', 'Waiting_Time']].to_dict('records'),
    'Response': process[['Process', 'Response_Time']].to_dict('records')
  }