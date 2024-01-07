from time import sleep
import tkinter as tk
from tkinter import ttk
from customtkinter import *
from tkinter import filedialog as fd
from PIL import Image
import sqlite3
from tkcalendar import Calendar, DateEntry
from time import strftime
from plyer import notification
import pygame
import threading
from datetime import datetime, timedelta
from tkinter import messagebox


class App:
    def __init__(self):
        self.root = CTk()
        self.root.overrideredirect(False) 
        # Setting title
        self.root.title("Alarm")
        # Setting window size
        self.root.config(bg="#343541")
        # Remove window border
        # self.root.overrideredirect(True) 

        self.root.iconbitmap("./img/menu/timermenu_d.ico") 
        self.root.iconphoto(True, tk.PhotoImage(file="./img/menu/timermenu_d.png"))
        
        self.loadDB()
        self.puppytest()
        self.alarms_data = self.retrieve_all_alarms()



        # Loop over appointments
        # for alarm in  self.alarms:
        #     alarm_id, time, day_weeks, active, song, repeat, note = alarm
        #     print(alarm_id, time, day_weeks, active, song, repeat, note)
        # Set border width and highlight thickness to make borders invisible
        self.root.configure(borderwidth=0, highlightthickness=0)
        # Ensure the window stays on top
        # self.root.attributes('-topmost', True)
        width = 700
        height = 230
        # width = 1000
        # height = 730
        set_appearance_mode("dark")
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # Variables for dragging
        self.start_x = None
        self.start_y = None
        self.i = 0
        self.remaining_time = 0
        self.timer_running = False
        self.timer_running_lap =False
        # Create a PanedWindow
        paned_window1 = tk.PanedWindow(self.root, orient=tk.VERTICAL, bg="#343541", sashwidth=1, sashrelief=tk.SUNKEN, sashcursor="arrow")

        # Create the first frame with a width of 100px
        self.windowtop = tk.Frame(paned_window1, width=80, bg="#2e2f38")
        paned_window1.add(self.windowtop)
        # Create the first frame with a width of 100px
        self.winmain = tk.Frame(paned_window1, bg="#414251")
        paned_window1.add(self.winmain)

        paned_window1.pack(fill=tk.BOTH, expand=True)
        # Create a PanedWindow
        paned_window2 = tk.PanedWindow(self.winmain, orient=tk.HORIZONTAL, bg="#343541", sashwidth=1, sashrelief=tk.SUNKEN, sashcursor="arrow")





        self.menu = CTkFrame( master = paned_window2, width=150, fg_color="#414251" , border_color="#1f1f24", border_width = 2  )
        self.loadmenu()

        paned_window2.add(self.menu, padx=3)
        # Create the second frame with the remaining width
        self.content = CTkFrame(master = paned_window2, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)
        paned_window2.add(self.content)
        self.isclock = True
        self.runing = False
        self.clockshow()
        paned_window2.pack(fill=tk.BOTH, expand=True)

    def start(self):
        self.root.mainloop()


    def start_drag(self, event):
        self.start_x = event.x_root - self.root.winfo_x()
        self.start_y = event.y_root - self.root.winfo_y()

    def dragging(self, event):
        new_x = event.x_root - self.start_x
        new_y = event.y_root - self.start_y
        self.root.geometry(f"+{new_x}+{new_y}")


    def close_window1(self):
        self.root.destroy()
    def close_window(self):
        self.root.destroy()
    def close_window2(self, event):
        self.root.destroy()

    def hide_window2(self, event):
        self.root.iconify() # This will minimize the window
        # Alternatively, you can use self.windowtop.withdraw() to completely hide the window
    def hide_window(self):
        self.root.withdraw() # This will minimize the window
        # Alternatively, you can use self.windowtop.withdraw() to completely hide the window

    def show_window(self):
        self.root.deiconify()

    def loadmenu(self):
        # Store references to PhotoImage objects
        self.image_references = []

        self.runing = False

        # Load image using Tkinter's PhotoImage
        imaged = Image.open('./img/menu/timermenu_d.png')
        imagel = Image.open('./img/menu/timermenu_l.png')
        self.image_references.append(imaged)
        self.image_references.append(imagel)
        button = CTkButton(master = self.menu, image=CTkImage(dark_image= imaged,light_image= imagel),text = "Ztimer", anchor="w", fg_color="#414251",hover_color="#414251", border_color="#414251", border_width=2, command=self.close_window1, cursor="hand2" ,font=("Helvetica",20) )
        button.pack(side="top", pady=10,padx=3)

        # Create and add custom buttons with icons and text to frame1
        button_icons = [
            {
                "icond":'./img/menu/clock_d.png',
                "iconl":'./img/menu/clock_l.png',
                "text":'clock',
                "cmd": lambda event : self.clockshow_e(event=event)
            },
            {
                "icond":'./img/menu/calendar_d.png',
                "iconl":'./img/menu/calendar_l.png',
                "text":'agenda',
                "cmd": lambda event : self.agendashow_e(event=event)
            },
            {
                "icond":'./img/menu/timer_d.png',
                "iconl":'./img/menu/timer_l.png',
                "text":'timer',
                "cmd": lambda event : self.timershow_e(event=event) 
            },
            {
                "icond":'./img/menu/stopwatch_d.png',
                "iconl":'./img/menu/stopwatch_l.png',
                "text":'stopwatch',
                "cmd": lambda event : self.stopwatchshow_e(event=event)
            },
        ]


        for icon_path in button_icons:
            imaged = Image.open(icon_path["icond"])
            imagel = Image.open(icon_path["iconl"])
            self.image_references.append(imaged)
            self.image_references.append(imagel)
            button = CTkButton(master = self.menu, image=CTkImage(dark_image= imaged,light_image= imagel),text = icon_path["text"], anchor="w", fg_color="#2c2d37",hover_color="#343540", border_color="#16161c", border_width=2, cursor="hand2" ,font=("Helvetica",20) )
            button.bind("<Button-1>", icon_path["cmd"])
            button.pack(side="top", pady=5,padx=9)
    
    def clockshow_e(self,event = None):
        if (self.runing) :
            self.timer_running = False
            self.timer_running_lap = False
            self.clean(event=None)
            self.clockshow()
    def agendashow_e(self,event = None):
        if (self.runing) :
            self.timer_running = False
            self.timer_running_lap = False
            self.clean(event=None)
            self.agendashow()
    def timershow_e(self,event = None):
        if (self.runing) :
            self.timer_running_lap = False
            self.clean(event=None)
            self.timershow()
    def stopwatchshow_e(self,event = None):
        if (self.runing) :
            self.timer_running = False
            self.clean(event=None)
            self.stopwatchshow()

    def update_time(self):
        if(self.i >= 10):
            self.i  = 0
            time_string = strftime('%H:%M:%S')
            time_string2 = strftime('%H:%M')
            # Get the current date
            current_date = datetime.now()

            # Get the day of the week (Monday is 0, Sunday is 6)
            day_of_week = current_date.weekday()

            # Adjust the result to make Sunday 0 and Saturday 6
            adjusted_day_of_week = (day_of_week + 1) % 7
            if (self.isclock) :  self.label.configure(text=time_string)
            for a in self.alarms_data:
                alarm_id, time, day_weeks, active, song, repeat, note = a
                # print(alarm_id,day_weeks , adjusted_day_of_week,day_weeks[adjusted_day_of_week])
                if(str(active) == '1' and str(time) == time_string2 and str(day_weeks[adjusted_day_of_week]) == "1"):
                    # open_tkinter_window_with_buttons( f"{note}", f"{song}")
                    threading.Thread(target=open_tkinter_window_with_buttons, args=(note, song,self.root)).start()
                    self.alarms_data.remove(a)
            if self.remaining_time > 0 and  self.timer_running:
                self.remaining_time -= 1
                self.update_timer_display()
            elif (self.remaining_time == 0 and  self.timer_running  and self.natural):
                # launch alert
                self.natural = False
                threading.Thread(target=open_tkinter_window_with_buttons, args=("Time is UP!!!", "alarm.mp3",self.root)).start()
                self.timer_running = False
            elif self.timer_running_lap:
                elapsed_time = datetime.now() - self.start_time
                formatted_time = (str(elapsed_time).split(".")[0]+":"+str(elapsed_time).split(".")[1][0:2])[2:]  # Remove microseconds
                self.clock_label.config(text=formatted_time)
        else:
            self.i +=1
            if self.timer_running_lap:
                elapsed_time = datetime.now() - self.start_time
                formatted_time =  (str(elapsed_time).split(".")[0]+":"+str(elapsed_time).split(".")[1][0:2])[2:]  # Remove microseconds
                self.clock_label.config(text=formatted_time)

        self.root.after(100, self.update_time)

    def stopwatchshow(self):
        # Create a PanedWindow
        self.mainholder = tk.PanedWindow(self.content, orient=tk.HORIZONTAL, bg="#343541", sashwidth=1,
                                         sashrelief=tk.SUNKEN, sashcursor="arrow", borderwidth=2)

        # Create the frame for the timer display
        self.clock_frame = CTkFrame(self.mainholder , width=150, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)
        self.clock_label = tk.Label(self.clock_frame, text="00:00:00", font=("Terminal",21), pady=50, padx=15, bg="#343541", fg="white")
        self.clock_label.pack(padx=15, pady=45)

        # Create the frame for buttons and entry
        self.controls_frame = CTkFrame(self.mainholder , width=150, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)

        self.start_button = CTkButton(self.controls_frame, text="Start", command=self.start_timer_lap)
        self.lap_button = CTkButton(self.controls_frame, text="Lap", command=self.lap_timer)
        self.pause_button = CTkButton(self.controls_frame, text="Pause", command=self.pause_timer_lap)
        self.reset_button = CTkButton(self.controls_frame, text="Reset", command=self.reset_timer_lap)

        # Create the third frame with a scrollable frame for laps
        self.laps_frame = CTkFrame(self.mainholder , width=150, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)
        self.ls_laps_holder = tk.Frame(self.laps_frame, bg="#343541", borderwidth=2)
        self.ls_laps_holder.pack(side="top", fill="both", expand=True)

        self.laps_all = CTkTextbox(self.ls_laps_holder, fg_color="#343541" ,border_color="#1f1f24", border_width = 2)
        self.laps_all.pack(fill="both", expand=True)

        self.start_button.pack(side=tk.TOP, pady=10 , padx=6)
        self.lap_button.pack(side=tk.TOP, pady=10 , padx=6)
        self.pause_button.pack(side=tk.TOP, pady=10 , padx=6)
        self.reset_button.pack(side=tk.TOP, pady=10 , padx=6)

        # Pack frames in the mainholder using pack
        self.mainholder.add(self.clock_frame, padx=23)
        self.mainholder.add(self.controls_frame, padx=3)
        self.mainholder.add(self.laps_frame, padx=5)
        self.mainholder.pack(fill=tk.BOTH, expand=True)
        # Timer variables
        self.timer_running_lap = False
        self.start_time =  datetime.now()
        self.lap_times = []

    def start_timer_lap(self):
        if not self.timer_running_lap:
            self.timer_running_lap = True
            self.count_lap = 0
            self.start_time = datetime.now()

    def lap_timer(self):
        if self.timer_running_lap:
            self.count_lap +=1
            lap_time = datetime.now() - self.start_time
            self.lap_times.append(lap_time)
            # self.laps_all.insert(tk.END, (str(lap_time).split(".")[0]+":"+str(lap_time).split(".")[1][0:2])[2:])
            self.laps_all.insert("0.0", str(self.count_lap)+" | "+(str(lap_time).split(".")[0]+":"+str(lap_time).split(".")[1][0:2])[2:]+"\n") 

    def pause_timer_lap(self):
        self.timer_running_lap = False

    def reset_timer_lap(self):
        self.timer_running_lap = False
        self.start_time = None
        self.lap_times = []
        self.clock_label.config(text="00:00:00")
        self.laps_all.delete("0.0", "end") 



    def timershow(self):
        # Create a PanedWindow
        self.mainholder = tk.PanedWindow(self.content, orient=tk.HORIZONTAL, bg="#343541", sashwidth=1, sashrelief=tk.SUNKEN, sashcursor="arrow"  , borderwidth=2)
                # Create the frame for the timer display
        self.clock_frame = CTkFrame(self.mainholder , width=150, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)
        self.clock_label = CTkLabel(self.clock_frame, text="00:00", font=("Terminal", 34), pady=50,padx= 15)
        self.clock_label.pack(padx= 15 , pady= 45)

        # Create the frame for buttons and entry
        self.controls_frame =  CTkFrame(self.mainholder ,width=150, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)
        self.time_entry_label = CTkLabel(self.controls_frame, text="Set Time :" )
        self.time_entry = CTkEntry(self.controls_frame , placeholder_text="10:00")
        self.time_entry.insert(0, "10:00")
        self.start_button = CTkButton(self.controls_frame, text="Start", command=self.start_timer)
        self.pause_button = CTkButton(self.controls_frame, text="Pause", command=self.pause_timer)
        self.reset_button = CTkButton(self.controls_frame, text="Reset", command=self.reset_timer)

        # Pack widgets in the controls frame
        self.time_entry_label.grid(row=0, column=0, pady=30 , padx=25)
        self.time_entry.grid(row=0, column=1, pady=5)
        self.start_button.grid(row=1, column=1, pady=5)
        self.pause_button.grid(row=2, column=1, pady=5)
        self.reset_button.grid(row=3, column=1, pady=5)

        # Pack frames in the mainholder
        self.mainholder.add(self.clock_frame, padx=23)
        self.mainholder.add(self.controls_frame, padx=3)
        self.mainholder.pack(fill=tk.BOTH, expand=True)

        # Timer variables
        self.natural = False
        self.timer_running = False
        self.remaining_time = 0
        self.after_id = None

    def start_timer(self,txt = None):
        if not self.timer_running:
            try:
                time_str = self.time_entry.get()
                if txt != None : time_str =txt
                if(self.validate_mins_format(time_str)): 
                    hours, minutes = map(int, time_str.split(':'))
                    self.remaining_time = hours * 60 + minutes 
                    self.update_timer_display()
                    self.timer_running = True
                    self.natural = True

            except ValueError:
                print("Invalid input. Please enter a valid time in HH:MM format.")
    def validate_mins_format(self,time_str):
        try:
            # Split the time string into hours and minutes
            hours, minutes = map(int, time_str.split(':'))

            # Check if hours and minutes are within valid ranges
            if 0 <= hours <100 and 0 <= minutes < 60:
                return True
            else:
                print("Error: Hours must be between 0 and 23, and minutes must be between 0 and 59.")
                return False
        except ValueError:
            print("Error: Invalid time format. Please use 'hours:minutes'.")
            return False
    def validate_time_format(self,time_str):
        try:
            # Split the time string into hours and minutes
            hours, minutes = map(int, time_str.split(':'))

            # Check if hours and minutes are within valid ranges
            if 0 <= hours < 24 and 0 <= minutes < 60:
                return True
            else:
                print("Error: Hours must be between 0 and 23, and minutes must be between 0 and 59.")
                return False
        except ValueError:
            print("Error: Invalid time format. Please use 'hours:minutes'.")
            return False
    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            if (self.remaining_time > 0) : 
                self.natural = True
                self.pause_button.configure(text="Continue")
        elif( (not self.timer_running ) and self.remaining_time > 0):
            self.timer_running = True
            self.pause_button.configure(text="Pause")

    def reset_timer(self):
        self.natural = False
        self.remaining_time = 0
        self.update_timer_display()
        self.timer_running = False


    def update_timer_display(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.clock_label.configure(text=time_str)



    
    def agendashow(self):
        # Create a PanedWindow
        self.mainholder = tk.PanedWindow(self.content, orient=tk.HORIZONTAL, bg="#343541", sashwidth=1, sashrelief=tk.SUNKEN, sashcursor="arrow")



        # Create the second frame with the remaining width
        self.clock = CTkFrame(master = self.mainholder,width=150, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)
        # self.alarms = CTkFrame(master = self.mainholder,width=150, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)
        
        self.mainholder.add(self.clock, padx=3 , pady=9)
        # self.mainholder.add(self.alarms, padx=3)
        self.mainholder.pack(fill=tk.BOTH, expand=False , ipady=22)
        # Calendar
        self.cal = Calendar(self.clock, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=10)



    def clockshow(self):
        # Create a PanedWindow
        self.mainholder = tk.PanedWindow(self.content, orient=tk.HORIZONTAL, bg="#343541", sashwidth=1, sashrelief=tk.SUNKEN, sashcursor="arrow")

        # Create the second frame with the remaining width
        self.clock = CTkFrame(master = self.mainholder,width=150, fg_color="#343541" ,  border_color="#343541", border_width = 2)
        self.alarms = CTkFrame(master = self.mainholder,width=150, fg_color="#343541" ,  border_color="#1f1f24", border_width = 2)
        
        self.mainholder.add(self.clock, padx=23)
        self.mainholder.add(self.alarms, padx=3)
        self.mainholder.pack(fill=tk.BOTH, expand=False , padx=14 ,  pady=14)
        # Calendar
        # self.cal = Calendar(self.clock, selectmode="day", date_pattern="yyyy-mm-dd")
        # self.cal.pack(pady=0)

        self.label = CTkLabel(self.clock, font=('Terminal', 35) , text = "00:00:00", fg_color='#343541', text_color='#ffffff',compound="center",pady=80  ,corner_radius=20)
        self.label.pack(anchor='center')
        self.isclock = True

        self.alarms_items=[]
        self.alarms_data = self.retrieve_all_alarms()
        if (not self.runing) :
            self.update_time()
            self.runing = True


        self.alarms_main = tk.PanedWindow(self.alarms, orient=tk.VERTICAL, bg="#343541", sashwidth=1, sashrelief=tk.SUNKEN, sashcursor="arrow")

        # Create the first frame
        self.add_alarm = CTkFrame(master=self.alarms_main, fg_color="#343541", border_color="#1f1f24", border_width=2)
        self.alarms_main.add(self.add_alarm, pady=13)

        # Create the second frame with a scrollable frame
        self.ls_alarms_holder = CTkFrame(master=self.alarms_main, fg_color="#343541", border_color="#343541", border_width=2)
        # self.ls_alarms = CTkScrollableFrame(master=self.ls_alarms_holder, fg_color="#1f1f24" ,width=200, border_color="#1f1f24", border_width=2, orientation="vertical")
        self.ls_alarms_holder.pack(side="top", fill="both", expand=True)
        self.alarms_main.add(self.ls_alarms_holder, padx=0)
        # default vertical

        self.frame_all = CTkScrollableFrame(self.ls_alarms_holder,fg_color="#343541"  ,border_color="#1f1f24", border_width=2)

        self.alarms_main.pack(fill=tk.BOTH, expand=True)



  
        imagel = Image.open('./img/menu/time_add_l.png')
        self.image_references.append(imagel)
        button = CTkButton(master = self.add_alarm, image=CTkImage(dark_image= imagel,light_image= imagel),text = "ADD ALARM", anchor="w", fg_color="#414251",hover_color="#37374a", border_color="#414251", border_width=2, command=self.open_alarm_settings, cursor="hand2" ,font=("Helvetica",18) )
        button.bind("<Button-1>", self.hide_window2)
        button.pack(side="left", pady=6,padx=30)


        for alarm in  self.alarms_data:
            alarm_id, time, day_weeks, active, song, repeat, note = alarm
            item = CTkFrame(master=self.frame_all, fg_color='#343541', border_color="#1f1f24", border_width=2)
            imaged = Image.open('./img/menu/delete.png')
            self.image_references.append(imaged)
            button = CTkLabel(master = item, image=CTkImage(dark_image= imaged,light_image= imaged),text = "", anchor="w", fg_color="#343541", cursor="hand2" ,font=("Helvetica",20) , padx=5 )
            button.bind("<Button-1>", lambda event, id=alarm_id : self.delete_alarm_eve(event, id))
            button.pack(side="right", pady=10,padx=6)

            imaged = Image.open('./img/menu/switch-off.png')
            newac = "1"
            if str(active) == "1" :
                newac = "0"
                imaged = Image.open('./img/menu/switch-on.png')
            self.image_references.append(imaged)
            button = CTkLabel(master = item, image=CTkImage(dark_image= imaged,light_image= imaged),text = "", anchor="w", fg_color="#343541", cursor="hand2" ,font=("Helvetica",20) , padx=5 )
            button.bind("<Button-1>", lambda event, id=alarm_id , newac=newac: self.disable_alarm(event, id, newac))
            # button.bind("<Button-1>", self.disable_alarm(alarm_id,newac))
            button.pack(side="right", pady=0,padx=6)
            
            # Load image using Tkinter's PhotoImage
            imaged = Image.open('./img/menu/cog.png')
            self.image_references.append(imaged)
            button = CTkLabel(master = item, image=CTkImage(dark_image= imaged,light_image= imaged),text = "", anchor="w", fg_color="#343541", cursor="hand2" ,font=("Helvetica",20) , padx=5 )
            button.bind("<Button-1>", lambda event ,a = alarm : self.open_alarm_u_settings(self,alarm=a))
            button.pack(side="right", pady=10,padx=6)
            
            # Load image using Tkinter's PhotoImage


            button = CTkLabel(master = item,text = time , anchor="w", fg_color="#2c2d37", cursor="hand2" ,font=("Helvetica",20) , padx=5 )
            # button.bind("<Button-1>", self.hide_window2)
            button.pack(side="right", pady=10,padx=13)
            
            self.alarms_items.append(
                {
                    "id": alarm_id,
                    "item" : item ,
                }
            )
            item.pack()
        self.frame_all.pack()

    def refresh_alarms(self):
        self.ls_alarms_holder = CTkFrame(master=self.alarms_main, fg_color="#343541", border_color="#343541", border_width=2)
        self.ls_alarms_holder.pack(side="top", fill="both", expand=True)
        self.alarms_main.add(self.ls_alarms_holder, padx=0)
        self.frame_all = CTkScrollableFrame(self.ls_alarms_holder,fg_color="#343541" ,border_color="#1f1f24", border_width=2)

        self.alarms_items=[]
        self.alarms_data = self.retrieve_all_alarms()
        for alarm in  self.alarms_data:
            alarm_id, time, day_weeks, active, song, repeat, note = alarm
            item = CTkFrame(master=self.frame_all, fg_color='#343541', border_color="#1f1f24", border_width=2)
            # button.bind("<Button-1>", self.hide_window2)
            # button.pack(side="right", pady=10,padx=3)
            # Load image using Tkinter's PhotoImage
            imaged = Image.open('./img/menu/delete.png')
            self.image_references.append(imaged)
            button = CTkLabel(master = item, image=CTkImage(dark_image= imaged,light_image= imaged),text = "", anchor="w", fg_color="#343541", cursor="hand2" ,font=("Helvetica",20) , padx=5 )
            button.bind("<Button-1>", lambda event, id=alarm_id : self.delete_alarm_eve(event, id))
            # button.bind("<Button-1>", self.clean)
            button.pack(side="right", pady=10,padx=6)

            imaged = Image.open('./img/menu/switch-off.png')
            newac = "1"
            if str(active) == "1" :
                newac = "0"
                imaged = Image.open('./img/menu/switch-on.png')
            self.image_references.append(imaged)
            button = CTkLabel(master = item, image=CTkImage(dark_image= imaged,light_image= imaged),text = "", anchor="w", fg_color="#343541", cursor="hand2" ,font=("Helvetica",20) , padx=5 )
            button.bind("<Button-1>", lambda event, id=alarm_id , newac=newac: self.disable_alarm(event, id, newac))
            # button.bind("<Button-1>", self.disable_alarm(alarm_id,newac))
            button.pack(side="right", pady=0,padx=6)
            
            # Load image using Tkinter's PhotoImage
            imaged = Image.open('./img/menu/cog.png')
            self.image_references.append(imaged)
            button = CTkLabel(master = item, image=CTkImage(dark_image= imaged,light_image= imaged),text = "", anchor="w", fg_color="#343541", cursor="hand2" ,font=("Helvetica",20) , padx=5 )
            button.bind("<Button-1>", lambda event ,a = alarm : self.open_alarm_u_settings(self,alarm=a))
            button.pack(side="right", pady=10,padx=6)
            
            # Load image using Tkinter's PhotoImage


            button = CTkLabel(master = item,text = time , anchor="w", fg_color="#2c2d37", cursor="hand2" ,font=("Helvetica",20) , padx=5 )
            # button.bind("<Button-1>", self.hide_window2)
            button.pack(side="right", pady=10,padx=13)
            
            self.alarms_items.append(
                {
                    "id": alarm_id,
                    "item" : item ,
                }
            )
            item.pack()
        self.frame_all.pack()
        self.alarms_main.pack(fill=tk.BOTH, expand=True)

    def open_alarm_u_settings(self , event ,alarm):
        alarm_id, time, day_weeks, active, song, repeat, note = alarm
        # Create a new window for alarm settings
        alarm_settings_window = tk.Toplevel(self.root,width=200,height=200,bg="#343541")
        alarm_settings_window.title("Alarm Settings")

        # Make the window non-resizable
        alarm_settings_window.resizable(False, False)
        # Calculate the x, y position to center the window
        window_width = 280
        window_height = 500
        screen_width = alarm_settings_window.winfo_screenwidth()
        screen_height = alarm_settings_window.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set the window position
        alarm_settings_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Time input    
        time_label = CTkLabel(alarm_settings_window, text="Set Time:")
        time_label.pack(pady=5)

        time_entry = CTkEntry(alarm_settings_window , placeholder_text='00:00')
        time_entry.pack(pady=5)
        time_entry.insert(0, time)
        # Songs combobox and add song button
        songs_label = CTkLabel(alarm_settings_window, text="Select Song:")
        songs_label.pack(pady=5)
        self.s_names= []
        self.songs_all= self.retrieve_all_songs()
        for s in self.songs_all:
            id,name,path = s
            self.s_names.append(name)
        self.songs_combobox = CTkComboBox(alarm_settings_window, values= self.s_names, command= lambda s: self.get_song_id(s))
        self.songs_combobox.pack(pady=5)
        self.get_song_id(self.s_names[0])
        add_song_button = CTkButton(alarm_settings_window, text="Add Song", command=self.add_song)
        add_song_button.pack(pady=5)

        # repeate input    
        repeate_label = CTkLabel(alarm_settings_window, text="Repeate:")
        repeate_label.pack(pady=5)

        repeate_entry = CTkEntry(alarm_settings_window,placeholder_text='1')
        repeate_entry.insert(0, repeat)
        repeate_entry.pack(pady=5)

        # Note input    
        note_label = CTkLabel(alarm_settings_window, text="Note:")
        note_label.pack(pady=5)

        note_entry = CTkEntry(alarm_settings_window , placeholder_text="note")
        note_entry.pack(pady=5)
        note_entry.insert(0, note)
        # Save button
        img = Image.open("./img/menu/save.png")
        save_button = CTkButton(alarm_settings_window, text="Save" , anchor='center' ,image=CTkImage(dark_image= img,light_image= img),width=111, command=lambda: self.update_and_dip(
            alarm_settings_window,
            alarm_id,
            time_entry.get(),
            f"{self.daych[6].get()}{self.daych[5].get()}{self.daych[4].get()}{self.daych[3].get()}{self.daych[2].get()}{self.daych[1].get()}{self.daych[0].get()}",
            "1",
            self.songs_combobox.get(),
            repeate_entry.get(),
            note_entry.get()
        ))
        save_button.pack(pady=10,padx=50)
        days=['S','M','T','W','T','F','S']
        days.reverse()
        self.daych= [] 
        i = 6
        for d in days:
            checkbox = CTkCheckBox(alarm_settings_window, text=d, onvalue="1", offvalue="0",width=12)
            if(str(day_weeks[i])=="1"):checkbox.select()
            i-=1
            checkbox.pack(side='right',pady=5)
            self.daych.append(checkbox)

    def open_alarm_settings(self):
        # Create a new window for alarm settings
        alarm_settings_window = tk.Toplevel(self.root,width=200,height=200,bg="#343541")
        alarm_settings_window.title("Alarm Settings")

        # Make the window non-resizable
        alarm_settings_window.resizable(False, False)
        # Calculate the x, y position to center the window
        window_width = 280
        window_height = 500
        screen_width = alarm_settings_window.winfo_screenwidth()
        screen_height = alarm_settings_window.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set the window position
        alarm_settings_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Time input    
        time_label = CTkLabel(alarm_settings_window, text="Set Time:")
        time_label.pack(pady=5)

        time_entry = CTkEntry(alarm_settings_window , placeholder_text='00:00')
        time_entry.pack(pady=5)

        # Songs combobox and add song button
        songs_label = CTkLabel(alarm_settings_window, text="Select Song:")
        songs_label.pack(pady=5)
        self.s_names= []
        self.songs_all= self.retrieve_all_songs()
        for s in self.songs_all:
            id,name,path = s
            self.s_names.append(name)
        self.songs_combobox = CTkComboBox(alarm_settings_window, values= self.s_names, command= lambda s: self.get_song_id(s))
        self.songs_combobox.pack(pady=5)
        self.get_song_id(self.s_names[0])
        add_song_button = CTkButton(alarm_settings_window, text="Add Song", command=self.add_song)
        add_song_button.pack(pady=5)

        # repeate input    
        repeate_label = CTkLabel(alarm_settings_window, text="Repeate:")
        repeate_label.pack(pady=5)

        repeate_entry = CTkEntry(alarm_settings_window,placeholder_text='1')
        repeate_entry.insert(0, "1")
        repeate_entry.pack(pady=5)

        # Note input    
        note_label = CTkLabel(alarm_settings_window, text="Note:")
        note_label.pack(pady=5)

        note_entry = CTkEntry(alarm_settings_window , placeholder_text="note")
        note_entry.pack(pady=5)

        # Save button
        img = Image.open("./img/menu/save.png")
        save_button = CTkButton(alarm_settings_window, text="Save" , anchor='center' ,image=CTkImage(dark_image= img,light_image= img),width=111, command=lambda: self.insert_and_dip(
            alarm_settings_window,
            time_entry.get(),
            f"{self.daych[6].get()}{self.daych[5].get()}{self.daych[4].get()}{self.daych[3].get()}{self.daych[2].get()}{self.daych[1].get()}{self.daych[0].get()}",
            "1",
            self.songs_combobox.get(),
            repeate_entry.get(),
            note_entry.get()
        ))
        save_button.pack(pady=10,padx=50)
        days=['S','M','T','W','T','F','S']
        days.reverse()
        self.daych= [] 
        for d in days:
            checkbox = CTkCheckBox(alarm_settings_window, text=d, onvalue="1", offvalue="0",width=12)
            checkbox.select()
            checkbox.pack(side='right',pady=5)
            self.daych.append(checkbox)



    def get_song_id(self,choice):
        for s in self.songs_all:
            id,name,path = s
            dd = id
            if(str(name) ==  str(choice)):
                return id
        return dd
    def get_song_path(self,id):
        for s in self.songs_all:
            id,name,path = s
            dd = path
            if(str(id) ==  str(id)):
                return path
        return dd

    def update_and_dip(self,dad,id,time,dayweek,active,songid,rpeats,note):
        path = self.get_song_path(songid)
        self.update_alarm(id,time,dayweek,active,path,rpeats,note)
        dad.destroy()
        self.root.deiconify()
        self.clean_alarams(event=None)
        self.refresh_alarms()

    def insert_and_dip(self,dad,time,dayweek,active,songid,rpeats,note):
        if(self.validate_time_format(time)):
            path = self.get_song_path(songid)
            self.insert_alarm(time,dayweek,active,path,rpeats,note)
            dad.destroy()
            self.root.deiconify()
            self.clean_alarams(event=None)
            self.refresh_alarms()


    def disable_alarm(self,event,id,newac):
        self.update_alarm_active(id,newac)
        self.clean_alarams(event)
        self.refresh_alarms()
        
    def delete_alarm_eve(self,event,id):
        self.delete_alarm(id)
        self.clean_alarams(event)
        self.refresh_alarms()

    def add_song(self):

        # Function to add a song - you can implement this as needed
        self.run_song_crud_app()

    def run_song_crud_app(self):
        def insert_song():
            name = entry_name.get()
            path = entry_path.get()

            if name and path:
                cursor.execute("INSERT INTO song (name, path) VALUES (?, ?)", (name, path))
                conn.commit()
                refresh_list()
                clear_entries()

        def refresh_list():
            # Clear the treeview
            for row in tree.get_children():
                tree.delete(row)

            # Retrieve all songs from the database
            songs = retrieve_all_songs()

            # Insert songs into the treeview
            for song in songs:
                tree.insert("", "end", values=song)
            self.s_names= []
            self.songs_all= retrieve_all_songs()
            for s in self.songs_all:
                id,name,path = s
                self.s_names.append(name)
            self.songs_combobox.configure( values= self.s_names)

            

        def retrieve_all_songs():
            cursor.execute("SELECT * FROM song")
            return cursor.fetchall()

        def delete_song():
            selected_item = tree.selection()
            if selected_item:
                song_id = tree.item(selected_item, 'values')[0]
                cursor.execute("DELETE FROM song WHERE id=?", (song_id,))
                conn.commit()
                refresh_list()

        def clear_entries():
            entry_name.delete(0, tk.END)
            entry_path.delete(0, tk.END)

        def select_file():
            filetypes = (
                ('text files', '*.mp3'),
                ('All files', '*.*')
            )
            filename = fd.askopenfilename(
                title='Open a Song',
                initialdir='/',
                filetypes=filetypes
            )
            entry_path.delete(0, tk.END)
            entry_path.insert(0, filename)
        def open_dialog_in_thread():
            thread = threading.Thread(target=select_file)
            thread.start()

        def open_toplevel(rooter):
            if rooter is None or not rooter.winfo_exists():
                rooter = ToplevelWindow(self)  # create window if its None or destroyed
            else:
                rooter.focus()  # if window exists focus it
        root = CTkToplevel(self.root)
        root.title("Song CRUD Application")

        # Create database and table if not exists
        conn = sqlite3.connect("appointments.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS song (id INTEGER PRIMARY KEY, name TEXT, path TEXT)")
        conn.commit()

        # Create GUI components
        label_name = CTkLabel(root, text="Song Name:")
        label_name.grid(row=0, column=0, padx=10, pady=10)
        entry_name = CTkEntry(root)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        # label_path = CTkLabel(root, text="Song Path:")
        # label_path.grid(row=1, column=0, padx=10, pady=10)
        entry_path = CTkEntry(root)
        entry_path.grid(row=1, column=0, padx=10, pady=10)

        # img = Image.open("./img/menu/openfolder.png")

        open_button = CTkButton(
            root,
            text='Open File',
            # image= CTkImage(dark_image= img,light_image= img),
            command=open_dialog_in_thread
        )
        open_button.grid(row=1, column=1, padx=10, pady=10)
        # img = Image.open("./img/menu/add.png")
        button_insert = CTkButton(root, text="Insert Song",command=insert_song)
        button_insert.grid(row=2, column=0, columnspan=2, pady=10)

        tree = ttk.Treeview(root, columns=("ID", "Name", "Path"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Path", text="Path")
        tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        
        button_refresh = CTkButton(root, text="Refresh List" ,command=refresh_list)
        button_refresh.grid(row=4, column=0, columnspan=2, pady=10)

        
        button_delete = CTkButton(root, text="Delete Song", command=delete_song)
        button_delete.grid(row=5, column=0, columnspan=2, pady=10)

        # Populate the treeview with existing songs
        refresh_list()

        open_toplevel(root)


    def clean_alarams(self, event):
        self.ls_alarms_holder.destroy()

    def clean(self, event):
        self.isclock = False
        self.mainholder.destroy()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig("self.frame", width=canvas_width)
            

    


    # db functions
    def puppytest(self):
        print("seeded")
        # self.insert_alarm('07:00', '1111111', '1', 'alarm.mp3', 3, 'wow')
        # self.insert_alarm('03:00', '1111111', '1', 'alarm.mp3', 3, 'wow')
        # self.insert_alarm('08:00', '1111111', '1', 'alarm.mp3', 3, 'wow')
        # self.insert_alarm('06:00', '1111111', '1', 'alarm.mp3', 3, 'wow')
        # self.insert_alarm('04:00', '1111111', '1', 'alarm.mp3', 3, 'wow')
        # self.insert_alarm('04:00', '1111111', '1', 'alarm.mp3', 3, 'wow')
        # self.insert_song('dada','alarm.mp3')
        # self.insert_song('dada1','alarm.mp3')
        # self.insert_song('dada2','alarm.mp3')
        # self.insert_song('dada3','alarm.mp3')


    def loadDB(self):
        
        # Create database and appointments table
        self.conn = sqlite3.connect("appointments.db")
        self.cursor = self.conn.cursor()

        # Create appointments table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments
                           (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, event TEXT)''')
        self.conn.commit()

        self.cursor = self.conn.cursor()

        # Create alarms table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS alarms
                           (id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, day_weeks TEXT,
                            active INTEGER, song TEXT, repeat INTEGER, note TEXT)''')
        self.conn.commit()
        self.cursor = self.conn.cursor()

        # Create alarms table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS song
                           (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT ,path TEXT)''')
        self.conn.commit()
    # appointement
    def insert_appointment(self, date, event):
        """
        Insert a new appointment into the database.

        Args:
            date (str): Date of the appointment.
            event (str): Description of the appointment.
        """
        self.cursor.execute("INSERT INTO appointments (date, event) VALUES (?, ?)", (date, event))
        self.conn.commit()

    def retrieve_all_appointments(self):
        """
        Retrieve all appointments from the database.

        Returns:
            list: List of tuples containing (id, date, event) for each appointment.
        """
        self.cursor.execute("SELECT * FROM appointments")
        return self.cursor.fetchall()

    def delete_appointment(self, appointment_id):
        """
        Delete an appointment from the database.

        Args:
            appointment_id (int): ID of the appointment to be deleted.
        """
        self.cursor.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
        self.conn.commit()

    def update_appointment(self, appointment_id, new_date, new_event):
        """
        Update an existing appointment in the database.

        Args:
            appointment_id (int): ID of the appointment to be updated.
            new_date (str): New date for the appointment.
            new_event (str): New description for the appointment.
        """
        self.cursor.execute("UPDATE appointments SET date=?, event=? WHERE id=?",
                            (new_date, new_event, appointment_id))
        self.conn.commit()
    # songs
    def insert_song(self, name, path):
        """
        Insert a new song into the database.

        Args:
            name (str): Name of the song.
            path (str): Path to the song file.
        """
        self.cursor.execute("INSERT INTO song (name, path) VALUES (?, ?)", (name, path))
        self.conn.commit()

    def retrieve_all_songs(self):
        """
        Retrieve all songs from the database.

        Returns:
            list: List of tuples containing (id, name, path) for each song.
        """
        self.cursor.execute("SELECT * FROM song")
        return self.cursor.fetchall()

    def delete_song(self, song_id):
        """
        Delete a song from the database.

        Args:
            song_id (int): ID of the song to be deleted.
        """
        self.cursor.execute("DELETE FROM song WHERE id=?", (song_id,))
        self.conn.commit()

    def update_song(self, song_id, new_name, new_path):
        """
        Update an existing song in the database.

        Args:
            song_id (int): ID of the song to be updated.
            new_name (str): New name for the song.
            new_path (str): New path for the song file.
        """
        self.cursor.execute("UPDATE song SET name=?, path=? WHERE id=?", (new_name, new_path, song_id))
        self.conn.commit()
    # alaram
    def insert_alarm(self, time, day_weeks, active, song, repeat, note):
        """
        Insert a new alarm into the database.

        Args:
            time (str): Time of the alarm.
            day_weeks (str): Binary representation of days of the week (e.g., "01111110").
            active (int): 1 if the alarm is active, 0 otherwise.
            song (str): Path to the alarm sound file.
            repeat (int): 1 if the alarm should repeat, 0 otherwise.
            note (str): Additional note for the alarm.
        """
        self.cursor.execute("INSERT INTO alarms (time, day_weeks, active, song, repeat, note) VALUES (?, ?, ?, ?, ?, ?)",
                            (time, day_weeks, active, song, repeat, note))
        self.conn.commit()
        self.alarms_data = self.retrieve_all_alarms()

    def retrieve_all_alarms(self):
        """
        Retrieve all alarms from the database.

        Returns:
            list: List of tuples containing (id, time, day_weeks, active, song, repeat, note) for each alarm.
        """
        self.cursor.execute("SELECT * FROM alarms")
        return self.cursor.fetchall()

    def delete_alarm(self, alarm_id):
        """
        Delete an alarm from the database.

        Args:
            alarm_id (int): ID of the alarm to be deleted.
        """
        self.cursor.execute("DELETE FROM alarms WHERE id=?", (alarm_id,))
        self.conn.commit()
        self.alarms_data = self.retrieve_all_alarms()

    def update_alarm(self, alarm_id, new_time, new_day_weeks, new_active, new_song, new_repeat, new_note):
        """
        Update an existing alarm in the database.

        Args:
            alarm_id (int): ID of the alarm to be updated.
            new_time (str): New time for the alarm.
            new_day_weeks (str): New binary representation of days of the week.
            new_active (int): New status of the alarm (1 for active, 0 for inactive).
            new_song (str): New path to the alarm sound file.
            new_repeat (int): New status of alarm repetition (1 for repeat, 0 for no repeat).
            new_note (str): New additional note for the alarm.
        """
        self.cursor.execute("UPDATE alarms SET time=?, day_weeks=?, active=?, song=?, repeat=?, note=? WHERE id=?",
                            (new_time, new_day_weeks, new_active, new_song, new_repeat, new_note, alarm_id))
        self.conn.commit()
        self.alarms_data = self.retrieve_all_alarms()
    def update_alarm_active(self, alarm_id, new_active):
        """
        Update active state of an existing alarm in the database.

        Args:
            alarm_id (int): ID of the alarm to be updated.  
            new_active (int): New status of the alarm (1 for active, 0 for inactive).
        """
        self.cursor.execute("UPDATE alarms SET active=? WHERE id=?",
                            (new_active, alarm_id))
        self.conn.commit()
        self.alarms_data = self.retrieve_all_alarms()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()


def open_tkinter_window_with_buttons( msg,mp3_path,rooter):
    def play_music(r,file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)
        r.after(60000, lambda: stop_music(r))
    def stop_music(root):
        pygame.mixer.music.stop()
        root.destroy()

    def snooze_notification(root):
        stop_music(root)
        sleep(300)  # Snooze for 5 minutes (300 seconds)
        threading.Thread(target=open_tkinter_window_with_buttons, args=(msg, mp3_path,root)).start()
        # show_notification("Alarm", msg, mp3_path)
    def open_toplevel(toplevel_window):
        if toplevel_window is None or not toplevel_window.winfo_exists():
            toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            toplevel_window.focus()  # if window exists focus it
    def show_notification(title, message, song_path):
        # play_music(song_path)

        # Add snooze and stop buttons to the notification window
        notification.notify(
            title="Alarm",
            message=msg,
            timeout=10,
            app_icon=None
        )

        root = CTkToplevel(rooter)
        
        # Make the window not resizable
        root.resizable(False, False)
        
        # Register a callback to handle the window close event
        root.protocol("WM_DELETE_WINDOW", lambda: stop_music(root))
        play_music(root ,song_path)
        root.title("Alarm")
        label = CTkLabel(root, text=msg)
        label.pack()

        snooze_button = CTkButton(root, text="Snooze", command= lambda r = root : snooze_notification(r))
        snooze_button.pack()

        stop_button = CTkButton(root, text="Stop", command= lambda r = root : stop_music(r))
        stop_button.pack()

        open_toplevel(root)

    show_notification("Alarm", msg, mp3_path)

def appinit():
    app = App()
    return app
def start(app):
    app.start()
def restor(app):
    app.show_window()
def close(app):
    app.close_window()

# Example of usage:
if __name__ == "__main__":
    app = appinit()
    start(app)