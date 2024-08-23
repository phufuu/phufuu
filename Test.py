
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import telnetlib



def main(ip_address, port):
    global tn  
    global connection_error_occurred  
        
    data =  '''
            R0lGODlhgACAAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr
            /wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCq
            mQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMA
            MzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV
            /zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPV
            mTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYr
            M2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA
            /2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/
            mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlV
            M5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq
            /5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswA
            mcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyA
            M8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV
            /8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8r
            mf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+q
            M/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP//
            /wAAAAAAAAAAAAAAACH5BAEAAPwALAAAAACAAIAAAAj/APcJHEiwoMGDCBMqXMiw
            ocOHECNKnEixosWLGDNq3Mixo8ePIEOKHEmypMmTKFOqXMmypcuXMGPKnEmzps2b
            OHPq3Mmzp8+fQIMKHUq0qNGjSJMqXcq0qVOBmcTEAEC1qtWrWLNq3cp1awwxmW4q
            E9O1rNmzaLOKgTYTTdq3cONiFQNy0o0YMW5MUqhsqty/gM/GULZxrNawBpUFXsyY
            K+GLxG50pUtQ2YrGmDNTtZjJb1k0BD1rHh144iS49QSSJc0aMGiHhuOChsY1RqbH
            PJV1dswwMuAY+1ZnRSw001bKCHcv3reVmFHFWg9CO/3W9uHDSI0Prywc7Q3nzNVm
            /wWeVHRVyr7fisEdHqt5qsSPar9q+33Z+APTsn/O2HbCtEwF9t1CAC7113oNFahU
            XHs9pGBSafkX0YNInTXgRBQeVRaCFWVoFFcNXuRhUdhpNCJR0W104lApmohWgFlx
            tKJQLWY0Y1A1YnQjUDmK+KKBMar444JBungWjFjJOCSERdq4ZIVN6vikhlH6eCSQ
            SQp5JZFZGmkWklcpuSWTXTo5JpRlSnkmlWla+SWWYWr5JpdxelkWmFaJOSeZdZq5
            J5p9qvknm4G6eSececp5KJ2J2tkVnlXpuSifjfo5KaCVCnopoZka+iiikSr6KaOh
            OsoVpJuJeiqoqZq6FaoA4GNn0Y4/cYXcrFN+ONl+E+ZKolk3yOoQrT5FKCyBvqII
            1yS8/pcsi3JxiOyauv51obNnNTsUdIFJeJBW9h1b3HjKpYVGagVp1V1V5CF12VwC
            pZeWtO1dNd9VIRZ1r1XxQbMusOCmRbeVtj4R8+pBaLyLlnUx/ltVvkDta9WtBpUL
            2D7cjsesT8pMYl9VbC0kb1zkudXayXBRrJC/cr22z8cox0zfRAm/la7MOGtFMEMW
            g1hQxjnnnNHIaiEEc9CaDbYRy9sl5DDSmbnckV14geXQ01ADJga6NUV1dNZd3WD1
            U2SXbfbZaKet9tpst+3223DHLffcdNdt991456333nz37fffgAcuuNwBAQA7
        '''


    def send_command(cmd):
        if not connection_error_occurred:
            tn.write(cmd.encode("utf-8")) 
            response = tn.read_some().decode("utf-8") 


    def send_pr():
        if not connection_error_occurred:
            tn.write("PR\r\n".encode("utf-8"))
            response = tn.read_some().decode("utf-8")
            nnn_value.set("No. " + response[5:7])
            global nnn_num
            nnn_num = int(response[5:7])

    def receive_data():
        global rdat
        if not connection_error_occurred:
            rdat = tn.read_until(b"\r\n").decode("utf-8")
            rgb_classification(rdat)
            

    def rgb_classification(rdat): 

        if nnn_num == 3:

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
            
            in_color_value.set(Hcolor)
            in_color_rgb.set(str(R) + ", " + str(G) + ", " + str(B))

            Lcolor = '#{:02x}{:02x}{:02x}'.format(R, G, B)
            input_color_a.config(bg=Lcolor)

        elif nnn_num == 10:
 
            H, S, V = map(int, rdat.split(','))
            clrb=int(clr_b.get())
            clrc=int(clr_c.get())
            clrd=int(clr_d.get())
            clre=int(clr_e.get())

            if H > 0 and H < clrb: 
                Hcolor = 'red'
            elif H >= clrb and H < clrc: 
                Hcolor = 'yellow'
            elif H >= clrc and H < clrd:
                Hcolor = 'green'
            elif H >= clrd and H < clre:
                Hcolor = 'blue'
            elif H >= clre and H <= 256:
                Hcolor = 'red'
            else:
                Hcolor = 'error' 
            
            in_color_value.set(Hcolor)
            if Hcolor == "error":
                input_color_a.config(bg="white")
            else:
                input_color_a.config(bg=Hcolor)
                in_color_rgb.set("H:" + str(H))



    root = tk.Tk()
    root.title("VS Smart Camera Remote")
    img = tk.PhotoImage(data=data,master=root) 
    root.iconphoto(False, img)

    nnn_value = tk.StringVar()
 
    in_color_value =  tk.StringVar()
    in_color_rgb =  tk.StringVar()

    clr_b =  tk.StringVar()
    clr_c =  tk.StringVar()
    clr_d =  tk.StringVar()
    clr_e =  tk.StringVar()


    frame = tk.Frame(root)
    frame.grid(padx=20,pady=10)

    set_frame = tk.LabelFrame(frame, text='Setting', bd=2, relief=tk.RIDGE)
    set_frame.grid(row=0, column=0, sticky="nsew")

    nnn_label = tk.Label(set_frame, width=6, font=("Arial", 40),  textvariable=nnn_value)
    nnn_label.grid(row=0, column=0, rowspan=2 ,sticky="nsew", padx=5, pady=5)
    nnn_label_dummy= tk.Label(set_frame, text="").grid(row=0,column=1,columnspan=2)


    numbers = list(range(100))
    combo = ttk.Combobox(set_frame, values=numbers, width=3, justify='center')
    combo.current(0)
    combo.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    set_button = tk.Button(set_frame, text="SET", command=lambda: set_btn_clicked())
    set_button.grid(row=1, column=2, sticky="nsew")

    trg_frame = tk.LabelFrame(frame, text='Trigger', bd=2, relief=tk.RIDGE)
    trg_frame.grid(row=1, column=0, sticky="nsew", pady=20)

    start_button = tk.Button(trg_frame, text="START (s)", image=img, compound="top", command=lambda: start_btn_clicked(), width=300 )#,height=5)
    start_button.grid(row=0, column=0, columnspan=3, padx=20, pady=10)

    reset_button = tk.Button(trg_frame, text="Reset (r)", command=lambda: reset_btn_clicked())
    reset_button.grid(row=1, column=2, sticky="nsew", padx=20, pady=10)

    clr_frame = tk.LabelFrame(frame, text='Color', bd=2, relief=tk.RIDGE)
    clr_frame.grid(row=4, column=0, sticky="nsew", padx=50,pady=20)
    input_color_a = tk.Label(clr_frame,font=("Arial", 30),text="       ")
    input_color_a.grid(row=0, column=0, sticky="nsew", padx=10)
    input_color_b = tk.Label(clr_frame, font=("Arial", 20),textvariable=in_color_value)
    input_color_b.grid(row=0, column=1, sticky="nsew")
    input_color_c = tk.Label(clr_frame, textvariable=in_color_rgb)
    input_color_c.grid(row=0, column=2, sticky="nsew", padx=10)

    clb_frame = tk.LabelFrame(frame, text='Color setting', bd=2, relief=tk.RIDGE)
    clb_frame.grid(row=5, column=0, sticky="nsew", padx=50,pady=20)

    bar_a = tk.Label(clb_frame,bg="red")
    bar_a.grid(row=0, column=0,columnspan=2, sticky="nsew")
    bar_b = tk.Label(clb_frame,bg="yellow")
    bar_b.grid(row=0, column=2,columnspan=2, sticky="nsew")
    bar_c = tk.Label(clb_frame,bg="green")
    bar_c.grid(row=0, column=4,columnspan=2, sticky="nsew")
    bar_d = tk.Label(clb_frame,bg="blue")
    bar_d.grid(row=0, column=6,columnspan=2, sticky="nsew")
    bar_e = tk.Label(clb_frame,bg="red")
    bar_e.grid(row=0, column=8,columnspan=2, sticky="nsew")

    clr_ent_a = tk.Entry(clb_frame,width=3)
    clr_ent_a.grid(row=1, column=0, sticky="nsew")
    clr_ent_a.insert(0,"0")
    clr_ent_b = tk.Entry(clb_frame, justify="center", textvariable=clr_b,width=6)
    clr_ent_b.grid(row=1, column=1,columnspan=2, sticky="nsew")
    clr_ent_b.insert(0,"35")
    clr_ent_c = tk.Entry(clb_frame, justify="center", textvariable=clr_c,width=6)
    clr_ent_c.grid(row=1, column=3,columnspan=2, sticky="nsew")
    clr_ent_c.insert(0,"70")
    clr_ent_d = tk.Entry(clb_frame, justify="center", textvariable=clr_d,width=6)
    clr_ent_d.grid(row=1, column=5,columnspan=2, sticky="nsew")
    clr_ent_d.insert(0,"120")
    clr_ent_e = tk.Entry(clb_frame, justify="center", textvariable=clr_e,width=6)
    clr_ent_e.grid(row=1, column=7,columnspan=2, sticky="nsew")
    clr_ent_e.insert(0,"210")
    clr_ent_f = tk.Entry(clb_frame, justify="right",width=3)
    clr_ent_f.grid(row=1, column=9, sticky="nsew")
    clr_ent_f.insert(0,"255")


    HOST = str(ip_address)
    PORT = int(port)

    try:
        tn = telnetlib.Telnet(HOST, PORT, 10)
    except Exception as e:
        messagebox.showerror("Error", "Connection failed. detail：" + str(e))
        tn = None
        connection_error_occurred = True
    else:
        connection_error_occurred = False 


    if not connection_error_occurred:

        cmd = "RUN\r\n"
        send_command(cmd)

        send_pr()



    def set_btn_clicked():
        number = str(combo.get())
        cmd = "PL,2," + number + "\r\n"        
        send_command(cmd)
        send_pr()

    def reset_btn_clicked():
        cmd = "RS\r\n"        
        send_command(cmd)

    def start_btn_clicked():
        cmd = "TRG\r\n"
        send_command(cmd)
        receive_data()


    def key_pressed(event):
        if event.char == 's':
            start_btn_clicked()
        if event.char == 'r':
            reset_btn_clicked()

    root.bind("<Key>", key_pressed)


    root.protocol("WM_DELETE_WINDOW", lambda: on_closing())

    def on_closing():
        root.quit()
        if not connection_error_occurred:

            cmd ="SET\r\n" 
            send_command(cmd)
            tn.close()

    root.mainloop()

if __name__ == "__main__":

    ip_address = simpledialog.askstring(title="IP address input",
                                        prompt="Enter the IP address of the camera to connect:",
                                        initialvalue="192.168.3.10")
    port = simpledialog.askstring(title="Port input",
                                  prompt="Enter the port of the camera to connect:",
                                  initialvalue="8500")


    if ip_address and port:
        main(ip_address, port)
    else:
        print("Invalid IP address or Port")