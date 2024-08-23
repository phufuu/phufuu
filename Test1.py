import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import telnetlib
from pymcprotocol import Type3E

# Create main window
root = tk.Tk()
root.title("PLC & Smart Camera Remote Control")
root.geometry("1400x800")  # ขยายขนาดหน้าต่างให้พอเหมาะ

# Configure styles for dark theme
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

# Global variables
tn = None
connection_error_occurred = False
plc_connected = False
camera_connected = False

# Initial names for M7001-M7030 and M7201-M7230
m7001_names = [f"M70{i+1:02}" for i in range(30)]
m7201_names = [f"M72{i+1:02}" for i in range(30)]

# Adjust grid weights to allow resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# ---- PLC CONTROL SECTION ----
plc = Type3E()

def plc_connect():
    global plc_connected
    ip = plc_ip_entry.get()
    port = int(plc_port_entry.get())
    try:
        plc.connect(ip, port)
        plc_connected = True
        plc_status_label.config(text="PLC Connected", background="green")
    except Exception as e:
        plc_connected = False
        plc_status_label.config(text="PLC Disconnected", background="red")
        messagebox.showerror("PLC Connection", f"Failed to connect to PLC: {str(e)}")

def plc_send_command():
    if not plc_connected:
        messagebox.showerror("PLC Command", "PLC is not connected.")
        return

    command = plc_command_entry.get()
    try:
        response = plc.batchread_wordunits(headdevice=command, readsize=1)
        plc_response.set(f"Response: {response}")
    except Exception as e:
        messagebox.showerror("PLC Command", f"Failed to send command: {str(e)}")

def read_m_status(start_m, count):
    if not plc_connected:
        return [False] * count  # Return a list of False (indicating OFF status) if not connected

    try:
        statuses = plc.batchread_bitunits(headdevice=start_m, readsize=count)
        return statuses
    except Exception as e:
        messagebox.showerror("PLC Status", f"Failed to read status: {str(e)}")
        return [False] * count

def update_m_status_labels():
    m7001_statuses = read_m_status("M7001", 30)
    m7201_statuses = read_m_status("M7201", 30)
    
    for i, status in enumerate(m7001_statuses):
        m7001_labels[i].config(text=f"{m7001_names[i]}: {'ON' if status else 'OFF'}", background="green" if status else "red")
        
    for i, status in enumerate(m7201_statuses):
        m7201_labels[i].config(text=f"{m7201_names[i]}: {'ON' if status else 'OFF'}", background="green" if status else "red")

def toggle_m7201_status(index):
    if not plc_connected:
        messagebox.showerror("PLC Command", "PLC is not connected.")
        return

    current_status = read_m_status(f"M72{index+1:02}", 1)[0]
    new_status = not current_status  # Toggle the status
    try:
        plc.batchwrite_bitunits(headdevice=f"M72{index+1:02}", values=[new_status])
        update_m_status_labels()  # Refresh the UI
    except Exception as e:
        messagebox.showerror("PLC Command", f"Failed to toggle M72{index+1:02} status: {str(e)}")

# PLC Frame
plc_frame = ttk.LabelFrame(root, text="PLC Control", padding=(10, 10))
plc_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

plc_frame.grid_columnconfigure(0, weight=1)
plc_frame.grid_columnconfigure(1, weight=1)
plc_frame.grid_rowconfigure(7, weight=1)
plc_frame.grid_rowconfigure(8, weight=1)

# PLC Connection Section
plc_connection_frame = ttk.LabelFrame(plc_frame, text="PLC Connection", padding=(10, 10))
plc_connection_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

plc_ip_label = ttk.Label(plc_connection_frame, text="PLC IP Address:")
plc_ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
plc_ip_entry = ttk.Entry(plc_connection_frame, width=20)
plc_ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

plc_port_label = ttk.Label(plc_connection_frame, text="PLC Port:")
plc_port_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
plc_port_entry = ttk.Entry(plc_connection_frame, width=20)
plc_port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

plc_connect_button = ttk.Button(plc_connection_frame, text="Connect", command=plc_connect)
plc_connect_button.grid(row=0, column=2, rowspan=2, padx=5, pady=10, sticky="ns")

plc_status_label = ttk.Label(plc_connection_frame, text="PLC Disconnected", background="red", font=("Arial", 12), width=20)
plc_status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

# PLC Command Section
plc_command_frame = ttk.LabelFrame(plc_frame, text="PLC Command", padding=(10, 10))
plc_command_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

plc_command_label = ttk.Label(plc_command_frame, text="Command:")
plc_command_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
plc_command_entry = ttk.Entry(plc_command_frame, width=30)
plc_command_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

plc_send_button = ttk.Button(plc_command_frame, text="Send", command=plc_send_command)
plc_send_button.grid(row=0, column=2, padx=5, pady=10)

plc_response = tk.StringVar()
plc_response_label = ttk.Label(plc_command_frame, textvariable=plc_response)
plc_response_label.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

# M7001-M7030 Status Frame
m7001_frame = ttk.LabelFrame(plc_frame, text="M7001-M7030 Status", padding=(10, 10))
m7001_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

m7001_frame.grid_columnconfigure(0, weight=1)
m7001_frame.grid_columnconfigure(1, weight=1)
m7001_frame.grid_columnconfigure(2, weight=1)
m7001_frame.grid_columnconfigure(3, weight=1)
m7001_frame.grid_columnconfigure(4, weight=1)
m7001_frame.grid_columnconfigure(5, weight=1)
m7001_frame.grid_columnconfigure(6, weight=1)
m7001_frame.grid_columnconfigure(7, weight=1)
m7001_frame.grid_columnconfigure(8, weight=1)
m7001_frame.grid_columnconfigure(9, weight=1)

m7001_labels = []
for i in range(30):
    label = tk.Button(m7001_frame, text=f"{m7001_names[i]}: OFF", background="red", width=7, height=2)
    label.grid(row=i//10, column=i%10, padx=2, pady=2, sticky="nsew")
    m7001_labels.append(label)

# M7201-M7230 Status Frame
m7201_frame = ttk.LabelFrame(plc_frame, text="M7201-M7230 Control", padding=(10, 10))
m7201_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

m7201_frame.grid_columnconfigure(0, weight=1)
m7201_frame.grid_columnconfigure(1, weight=1)
m7201_frame.grid_columnconfigure(2, weight=1)
m7201_frame.grid_columnconfigure(3, weight=1)
m7201_frame.grid_columnconfigure(4, weight=1)
m7201_frame.grid_columnconfigure(5, weight=1)
m7201_frame.grid_columnconfigure(6, weight=1)
m7201_frame.grid_columnconfigure(7, weight=1)
m7201_frame.grid_columnconfigure(8, weight=1)
m7201_frame.grid_columnconfigure(9, weight=1)

m7201_labels = []
for i in range(30):
    index = i  # Store the index for the button command
    label = tk.Button(m7201_frame, text=f"{m7201_names[i]}: OFF", background="red", width=7, height=2, command=lambda idx=index: toggle_m7201_status(idx))
    label.grid(row=i//10, column=i%10, padx=2, pady=2, sticky="nsew")
    m7201_labels.append(label)

# Button to update statuses
update_status_button = ttk.Button(plc_frame, text="Update M Status", command=update_m_status_labels)
update_status_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# ---- SMART CAMERA CONTROL SECTION ----

def camera_connect(ip_address, port):
    global tn, connection_error_occurred, camera_connected
    try:
        tn = telnetlib.Telnet(ip_address, port, 10)
        connection_error_occurred = False
        camera_connected = True
        camera_status_label.config(text="Camera Connected", background="green")
    except Exception as e:
        camera_connected = False
        camera_status_label.config(text="Camera Disconnected", background="red")
        messagebox.showerror("Camera Connection", f"Failed to connect to Camera: {str(e)}")
        tn = None

def camera_send_command(cmd):
    if not camera_connected:
        messagebox.showerror("Camera Command", "Camera is not connected.")
        return ""
    
    tn.write(cmd.encode("utf-8"))
    response = tn.read_some().decode("utf-8")
    return response

def camera_receive_data():
    if not camera_connected:
        messagebox.showerror("Camera Data", "Camera is not connected.")
        return
    
    rdat = tn.read_until(b"\r\n").decode("utf-8")
    camera_rgb_classification(rdat)

def camera_rgb_classification(rdat):
    R, G, B = map(int, rdat.split(','))
    if abs(R - G) < 30 and R > B and G > B:
        Hcolor = 'YELLOW'
    elif R > G and R > B:
        Hcolor = 'RED'
    elif G > R and G > B:
        Hcolor = 'GREEN'
    elif B > R and B > G:
        Hcolor = 'BLUE'
    else:
        Hcolor = 'NG'

    camera_color_value.set(Hcolor)
    camera_color_rgb.set(f"{R}, {G}, {B}")
    Lcolor = f'#{R:02x}{G:02x}{B:02x}'
    camera_color_display.config(bg=Lcolor)

def camera_take_photo():
    if not camera_connected:
        messagebox.showerror("Camera Command", "Camera is not connected.")
        return
    
    camera_send_command("SNAP\r\n")
    camera_receive_data()

# Camera Frame
camera_frame = ttk.LabelFrame(root, text="Smart Camera Control", padding=(10, 10))
camera_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

camera_frame.grid_columnconfigure(0, weight=1)
camera_frame.grid_columnconfigure(1, weight=1)

# Camera Connection Section
camera_connection_frame = ttk.LabelFrame(camera_frame, text="Camera Connection", padding=(10, 10))
camera_connection_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

camera_ip_label = ttk.Label(camera_connection_frame, text="Camera IP Address:")
camera_ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
camera_ip_entry = ttk.Entry(camera_connection_frame, width=20)
camera_ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

camera_port_label = ttk.Label(camera_connection_frame, text="Camera Port:")
camera_port_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
camera_port_entry = ttk.Entry(camera_connection_frame, width=20)
camera_port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

camera_connect_button = ttk.Button(camera_connection_frame, text="Connect", command=lambda: camera_connect(camera_ip_entry.get(), int(camera_port_entry.get())))
camera_connect_button.grid(row=0, column=2, rowspan=2, padx=5, pady=10, sticky="ns")

camera_status_label = ttk.Label(camera_connection_frame, text="Camera Disconnected", background="red", font=("Arial", 12), width=20)
camera_status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

# Camera Command Section
camera_command_frame = ttk.LabelFrame(camera_frame, text="Camera Command", padding=(10, 10))
camera_command_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

camera_command_label = ttk.Label(camera_command_frame, text="Command:")
camera_command_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
camera_command_entry = ttk.Entry(camera_command_frame, width=30)
camera_command_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

camera_send_button = ttk.Button(camera_command_frame, text="Send", command=lambda: camera_send_command(camera_command_entry.get()))
camera_send_button.grid(row=0, column=2, padx=5, pady=10)

camera_color_display = tk.Label(camera_command_frame, text="       ", font=("Arial", 30))
camera_color_display.grid(row=1, column=0, padx=5, pady=5, sticky="w")

camera_color_value = tk.StringVar()
camera_color_label = ttk.Label(camera_command_frame, textvariable=camera_color_value, font=("Arial", 20))
camera_color_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

camera_color_rgb = tk.StringVar()
camera_color_rgb_label = ttk.Label(camera_command_frame, textvariable=camera_color_rgb)
camera_color_rgb_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

camera_start_button = ttk.Button(camera_command_frame, text="Start", command=camera_receive_data)
camera_start_button.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

camera_snap_button = ttk.Button(camera_command_frame, text="Take Photo", command=camera_take_photo)
camera_snap_button.grid(row=4, column=0, columnspan=3, padx=5, pady=10)

# Settings Window for Renaming Lamps and Buttons
def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("600x600")

    def save_settings():
        for i in range(30):
            m7001_names[i] = m7001_entries[i].get() or m7001_names[i]
            m7201_names[i] = m7201_entries[i].get() or m7201_names[i]
        settings_window.destroy()
        update_m_status_labels()  # Refresh the UI after renaming

    m7001_frame = ttk.LabelFrame(settings_window, text="Rename M7001-M7030 Lamps", padding=(10, 10))
    m7001_frame.pack(fill="x", padx=10, pady=10)

    m7001_entries = []
    for i in range(30):
        label = ttk.Label(m7001_frame, text=f"M700{i+1:03}:")
        label.grid(row=i//10, column=(i%10)*2, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(m7001_frame)
        entry.grid(row=i//10, column=(i%10)*2+1, padx=5, pady=5, sticky="w")
        entry.insert(0, m7001_names[i])
        m7001_entries.append(entry)

    m7201_frame = ttk.LabelFrame(settings_window, text="Rename M7201-M7230 Buttons", padding=(10, 10))
    m7201_frame.pack(fill="x", padx=10, pady=10)

    m7201_entries = []
    for i in range(30):
        label = ttk.Label(m7201_frame, text=f"M72{i+1:02}:")
        label.grid(row=i//10, column=(i%10)*2, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(m7201_frame)
        entry.grid(row=i//10, column=(i%10)*2+1, padx=5, pady=5, sticky="w")
        entry.insert(0, m7201_names[i])
        m7201_entries.append(entry)

    save_button = ttk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack(pady=20)

settings_button = ttk.Button(root, text="Settings", command=open_settings_window)
settings_button.grid(row=1, column=1, padx=20, pady=10, sticky="e")

# Run the main loop
root.mainloop()
