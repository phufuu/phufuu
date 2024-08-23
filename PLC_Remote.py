import tkinter as tk
from tkinter import ttk, messagebox
from pymcprotocol import Type3E
import os

# สร้างหน้าต่างหลักและกำหนดขนาด
root = tk.Tk()
root.title("PLC Monitor & Control")
root.geometry("800x600")

# กำหนดธีมโทนมืด
style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background="#2e2e2e")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
style.configure("TButton", background="#444444", foreground="#ffffff")
style.configure("TEntry", background="#444444", foreground="#ffffff", fieldbackground="#444444")
style.configure("TLabelframe", background="#2e2e2e", foreground="#ffffff")
style.configure("TLabelframe.Label", background="#2e2e2e", foreground="#ffffff")
style.configure("Green.TLabel", background="green", foreground="white")
style.configure("Red.TLabel", background="red", foreground="white")
style.configure("Green.TButton", background="green", foreground="white")
style.configure("Red.TButton", background="red", foreground="white")

plc = None

# สร้าง Label สำหรับแสดงสถานะการเชื่อมต่อและข้อผิดพลาด
status_label = ttk.Label(root, text="Status: Not connected", font=("Segoe UI", 12), foreground="red", background="#2e2e2e")
status_label.pack(pady=10)

def ping_ip(ip):
    response = os.system(f"ping -c 1 {ip}" if os.name != 'nt' else f"ping -n 1 {ip}")
    
    if response == 0:
        messagebox.showinfo("Ping Result", f"Successfully reached {ip}.")
    else:
        messagebox.showerror("Ping Result", f"Failed to reach {ip}. Please check the IP address or network connection.")

def connect_to_plc():
    global plc
    ip = ip_entry.get()
    port = int(port_entry.get())
    plc = Type3E()
    plc.setaccessopt(commtype="binary")

    # แสดงข้อความขณะพยายามเชื่อมต่อ
    status_label.config(text=f"Attempting to connect to PLC at {ip}:{port}...", foreground="orange")
    root.update_idletasks()
    
    try:
        plc.connect(ip, port)
        status_label.config(text="Connected to PLC successfully!", foreground="green")
    except Exception as e:
        status_label.config(text=f"Connection Error: {e}", foreground="red")

def disconnect_from_plc():
    global plc
    if plc is not None:
        try:
            plc.close()
            status_label.config(text="Disconnected from PLC successfully!", foreground="green")
            plc = None
        except Exception as e:
            status_label.config(text=f"Disconnection Error: {e}", foreground="red")

def update_lamps_and_buttons():
    if plc is not None:
        try:
            # อ่านสถานะของบิต M7001 ถึง M7030 จาก PLC
            lamp_status = plc.batchread_bitunits(headdevice="M7001", readsize=30)
            print(f"Lamp Status: {lamp_status}")  # แสดงสถานะที่อ่านมาเพื่อดีบัก

            # อ่านสถานะของบิต M7201 ถึง M7230 จาก PLC
            button_status = plc.batchread_bitunits(headdevice="M7201", readsize=30)
            print(f"Button Status: {button_status}")  # แสดงสถานะที่อ่านมาเพื่อดีบัก

            # อัปเดตสถานะของหลอดไฟใน GUI ตามสถานะบิตที่อ่านมา
            for i in range(30):
                if lamp_status[i]:
                    lamps[i].config(style='Green.TLabel')
                else:
                    lamps[i].config(style='Red.TLabel')

                # อัปเดตสถานะของปุ่มควบคุมใน GUI ตามสถานะบิตที่อ่านมา
                if button_status[i]:
                    buttons[i].config(style='Green.TButton')
                    buttons[i].config(text=f'M720{i+1}: ON')
                else:
                    buttons[i].config(style='Red.TButton')
                    buttons[i].config(text=f'M720{i+1}: OFF')

        except Exception as e:
            status_label.config(text=f"Error reading PLC data: {e}", foreground="red")

    # เรียกใช้ฟังก์ชันนี้อีกครั้งหลังจาก 1 วินาที
    root.after(1000, update_lamps_and_buttons)

def toggle_device(index):
    if plc is not None:
        try:
            # กำหนดแอดเดรสของ M7201-M7230
            device_address = f"M720{index+1}"

            # อ่านสถานะปัจจุบันของบิต
            current_state = plc.batchread_bitunits(headdevice=device_address, readsize=1)[0]
            new_state = not current_state
            word_value = 1 if new_state else 0  # กำหนดค่า word เป็น 1 สำหรับ ON และ 0 สำหรับ OFF

            print(f"Current state of {device_address}: {current_state}, attempting to set to {new_state}")
            
            # เขียนค่า word ใหม่ลงในแอดเดรสของบิต
            response = plc.batchwrite_wordunits(headdevice=device_address, values=[word_value])
            print(f"Write response for {device_address}: {response}")
            
            # อัปเดตข้อความและสีของปุ่มควบคุม
            if new_state:
                buttons[index].config(style='Green.TButton', text=f'{device_address}: ON')
            else:
                buttons[index].config(style='Red.TButton', text=f'{device_address}: OFF')

        except Exception as e:
            status_label.config(text=f"Error writing to PLC: {e}", foreground="red")
            print(f"Failed to write to {device_address}: {e}")

# สร้างส่วนสำหรับกำหนด IP และ Port
connection_frame = ttk.Labelframe(root, text="Connection Settings", padding=10)
connection_frame.pack(pady=10, fill="x")

ttk.Label(connection_frame, text="IP Address:", font=("Segoe UI", 14)).grid(row=0, column=0, padx=5, pady=5)
ip_entry = ttk.Entry(connection_frame, width=15, font=("Segoe UI", 12))
ip_entry.grid(row=0, column=1, padx=5, pady=5)
ip_entry.insert(0, "192.168.3.39")  # ปรับค่าเริ่มต้นเป็น 192.168.3.39

ttk.Label(connection_frame, text="Port:", font=("Segoe UI", 14)).grid(row=1, column=0, padx=5, pady=5)
port_entry = ttk.Entry(connection_frame, width=10, font=("Segoe UI", 12))
port_entry.grid(row=1, column=1, padx=5, pady=5)
port_entry.insert(0, "2500")  # ปรับค่าเริ่มต้นเป็น 2500

button_frame = ttk.Frame(connection_frame)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)
connect_button = ttk.Button(button_frame, text="Connect", command=connect_to_plc, width=10)
connect_button.pack(side="left", padx=5)

disconnect_button = ttk.Button(button_frame, text="Disconnect", command=disconnect_from_plc, width=10)
disconnect_button.pack(side="right", padx=5)

# เพิ่มปุ่ม Ping
ping_button = ttk.Button(connection_frame, text="Ping", command=lambda: ping_ip(ip_entry.get()), width=10)
ping_button.grid(row=2, column=2, padx=5)

# สร้างปุ่มและหลอดไฟใน GUI

# สร้างหลอดไฟสำหรับ M7001-M7030
lamps_frame = ttk.Labelframe(root, text="Lamp Status (M7001-M7030)", padding=10)
lamps_frame.pack(pady=10, fill="x")

lamps = []
for i in range(30):
    address = f"M700{i+1}"
    lamp = ttk.Label(lamps_frame, text=address, style='Red.TLabel', width=8, anchor='center')
    lamp.grid(row=i // 10, column=i % 10, padx=5, pady=5)
    lamps.append(lamp)

# สร้างปุ่มสำหรับควบคุม M7201-M7230
buttons_frame = ttk.Labelframe(root, text="Control Buttons (M7201-M7230)", padding=10)
buttons_frame.pack(pady=10, fill="x")

buttons = []
for i in range(30):
    address = f"M720{i+1}"
    btn = ttk.Button(buttons_frame, text=f'{address}: OFF', style='Red.TButton', width=8, command=lambda i=i: toggle_device(i))
    btn.grid(row=i // 10, column=i % 10, padx=5, pady=5)
    buttons.append(btn)

update_lamps_and_buttons()
root.mainloop()

# ปิดการเชื่อมต่อเมื่อปิดโปรแกรม
def on_closing():
    if plc is not None:
        try:
            plc.close()
        except Exception as e:
            status_label.config(text=f"Error closing PLC connection: {e}", foreground="red")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)