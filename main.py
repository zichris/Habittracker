import tkinter as tk
from tkinter import ttk as tt
import sqlite3 as sq
from datetime import date as da
from datetime import datetime as dt
from _datetime import timedelta as tdelta


class Gui:
    def __init__(self):
        """
        Creates the main window of the application and initializes the main frame as None type.
        """
        self.root = tk.Tk()
        self.root.geometry("330x610+200+100")
        self.root.title("Habit Tracker")
        self.main_frame = None
        self.main_menu()

    def create_main_frame(self):
        """
        Creates the main frame, on which all buttons and other field are placed.
        This method is executed at the beginning of all other methods within the Gui class to first empty the frame
        and then place the new objects on it.
        """
        # Deletes the content that is currently displayed on the main frame
        if self.main_frame:
            self.main_frame.pack_forget()
        # Create new interface
        self.main_frame = tk.Frame(self.root, width=330, height=610)
        self.main_frame.pack()
        # Fixes the frame size, so that it does not change with the main window
        self.main_frame.propagate(0)

    def main_menu(self):
        """
        Initializes the main menu buttons and corresponding functions.
        """
        self.create_main_frame()

        # Define button names and functions
        self.new_habit_button = tk.Button(self.main_frame, text="New habit", command=self.new_habit)
        self.my_habits_button = tk.Button(self.main_frame, text="My habits", command=self.my_habits)
        self.delete_habit_button = tk.Button(self.main_frame, text="Delete habit", command=self.delete_habits)
        self.check_off_habit_button = tk.Button(self.main_frame, text="Check off habits", command=self.check_off_habits)
        self.quit_button = tk.Button(self.main_frame, text="Quit", command=self.root.quit)

        # Display and adjust button size and positions
        self.new_habit_button.place(height=50, width=150, x=10, y=10)
        self.my_habits_button.place(height=50, width=150, x=10, y=70)
        self.delete_habit_button.place(height=50, width=150, x=10, y=130)
        self.check_off_habit_button.place(height=50, width=150, x=10, y=190)
        self.quit_button.place(height=50, width=150, x=10, y=250)

    def information_window(self, var_text, var_x_init_geometry):
        """
        Creates a popup window to display the specified text.
        :param var_text: The lines of text that are to be shown in a separate window, passed in as a list.
        :type var_text: list
        :param var_x_init_geometry: The initial width of the window, will be automatically adjusted if the text is
            longer than the initial value.
        :type var_x_init_geometry: int
        """
        # Creates the second window with the given initial width and height depending on the number of items in the
        # var_text list.
        self.second_window = tk.Tk()
        self.second_window.title("Information")
        var_label_size = 220
        self.second_window.geometry(f"{var_x_init_geometry}x{45 + 35 * len(var_text)}+400+150")
        # Loops through the items of the var_text list and places them in the second window line by line.
        for i, current_text in enumerate(var_text):
            new_label = tk.Label(self.second_window, text=current_text)
            new_label.place(height=25, x=10, y=10 + i * 35)
            self.second_window.update()
            # Stores the length of the longest text within var_text
            if new_label.winfo_width() > var_label_size:
                var_label_size = new_label.winfo_width()
        # Readjusts the window width
        self.second_window.geometry(f"{var_label_size + 20}x{45 + 35 * len(var_text)}")
        self.back_button = tk.Button(self.second_window, text="Close", command=self.second_window.destroy)
        self.back_button.place(width=50, height=25, x=(var_label_size - 50) / 2, y=10 + 35 * len(var_text))

    def new_habit(self):
        """
        Initializes the menu in which new habits are created.
        The send_data function first checks whether the habit name entered by the user is valid and then passes all
        relevant variables to the new_habit_entry method of the Database class.
        """
        # This function is executed when the "Create Habit" button is pressed.
        def send_data():
            var_name = self.enter_habit_name.get()
            # Ensures the name field is not empty or consists only of spaces.
            if var_name and var_name.isspace() is False:
                # Ensures a habit of the same name does not exist.
                if not Database.check_exisiting(self, var_name):
                    # Checks the duration and type (days or weeks) of the periodicity.
                    var_number = int(self.enter_number_periodicity.get())
                    var_multiplier = self.enter_daysweeks_periodicity.get()
                    if var_multiplier == "days":
                        dayweek_flag = "d"
                        var_periodicity = var_number
                    elif var_multiplier == "weeks":
                        dayweek_flag = "w"
                        var_periodicity = var_number * 7
                    # Sends the data to the new_habit_entry method of the Database class to create the new habit.
                    Database.new_habit_entry(self, var_name, var_periodicity, dayweek_flag)
                    # Empties the habit name field and resets the periodicity combobox.
                    self.enter_habit_name.delete(0, "end")
                    self.enter_daysweeks_periodicity.current(0)
                    # Creates a confirmation for the user.
                    self.information_window(["Success!", f"Habit {var_name} created successfully!"], 300)
                # Creates a warning message for the user in case a habit of the same name already exists.
                else:
                    self.enter_habit_name.delete(0, "end")
                    self.enter_daysweeks_periodicity.current(0)
                    self.information_window([f"The habit {var_name} already exists, please choose other name!"], 300)
            # Creates a warning message for the user in case the habit name is left empty or consists only of spaces.
            else:
                self.information_window(["The habit name cannot be empty!"], 300)

        self.create_main_frame()

        # Define button and text entry field names and functions
        self.new_habit_create_habit_button = tk.Button(self.main_frame, text="Create Habit", command=send_data)
        self.new_habit_back_button = tk.Button(self.main_frame, text="back", command=self.main_menu)
        self.enter_habit_name = tk.Entry(self.main_frame, width=20)
        self.enter_habit_name_text = tk.Label(self.main_frame, anchor='w', text="Habit name:")
        self.enter_habit_periodicity_text = tk.Label(self.main_frame, anchor='w', text="Select periodicity: every")

        # Display and adjust button and text entry field size and positions
        self.enter_habit_name.place(height=25, width=150, x=170, y=10)
        self.enter_habit_name_text.place(height=25, width=150, x=10, y=10)
        self.enter_habit_periodicity_text.place(height=25, width=150, x=10, y=50)
        self.new_habit_create_habit_button.place(height=50, width=150, x=10, y=85)
        self.new_habit_back_button.place(height=50, width=150, x=170, y=85)

        # Creates a spinbox where the periodicity is entered, value range from 1 to 52
        self.enter_number_periodicity = tk.Spinbox(self.main_frame, from_=1, to=52, state='readonly')
        self.enter_number_periodicity.place(height=25, width=50, x=170, y=50)

        # Creates a combobox to specify whether a habit is due daily or weekly
        self.enter_daysweeks_periodicity = tt.Combobox(self.main_frame, state='readonly', values=["days", "weeks"])
        self.enter_daysweeks_periodicity.current(0)
        self.enter_daysweeks_periodicity.place(height=25, width=90, x=230, y=50)

    def my_habits(self):
        """
        Creates the menu to view information about the current habits as well as the functions to return
        the requested information.
        """
        # Defines the variables for querying the database for newest habits, oldest habits etc. using the single query
        # method of the Database class.

        var_today = da.today().strftime('%y%j')
        var_due_today = Database.return_habits_due_today(self)
        var_coming_up_names, var_coming_up_dates = Database.return_habits_coming_up(self)
        var_overdue_names, var_overdue_dates = Database.return_overdue_habits(self)
        var_newest = Database.single_query(self, "habit_name", "created", "DESC")
        var_newest_date = Database.single_query(self, "created", "created", "DESC")
        var_oldest = Database.single_query(self, "habit_name", "created", "ASC")
        var_oldest_date = Database.single_query(self, "created", "created", "ASC")
        var_longest = Database.single_query(self, "habit_name", "longest_streak", "DESC", "created", "DESC")
        var_longest_length = Database.single_query(self, "longest_streak", "longest_streak", "DESC", "created", "DESC")
        var_most_broken = Database.single_query(self, "habit_name", "number_streak_broken", "DESC", "created", "DESC")
        var_most_broken_number = Database.single_query(self, "number_streak_broken", "number_streak_broken", "DESC",
                                                       "created", "DESC")

        self.create_main_frame()

        self.my_habits_habit_information_button = tk.Button(self.main_frame, text="Habit details",
                                                            command=self.habit_details)
        self.my_habits_view_all_habits_button = tk.Button(self.main_frame, text="View all habits",
                                                          command=self.view_all_habits)
        # If any habit(s) currently exist, a list of the newest, oldest etc. is created and displayed to the user.
        if var_newest:
            newest_list = ["Your newest habits are:"]
            # Adds the items from the single query into to a list which is later passed to the information_window
            # method, pretty much the same for all following lists (oldest, longest etc.)
            for i, (current_text, current_date) in enumerate(zip(var_newest, var_newest_date)):
                # Converts the date from YYYY-MM-DD HH-MM-SS format into Day. Month Year Format, calculation of the
                # order is otherwise occasionally wrong.
                newest_list.append(f"{i + 1}. {current_text}, created on "
                                   f"{dt.strptime(str(current_date), '%Y-%m-%d %H:%M:%S').strftime('%d. %B %Y')}")
            self.my_habits_newest_habit_button = tk.Button(self.main_frame, wraplength=140,
                                                           text="What are my newest habits?",
                                                           command=lambda: self.information_window(newest_list, 300))
        else:
            # Displays the correct message if no habit is currently stored.
            self.my_habits_newest_habit_button = tk.Button(self.main_frame, wraplength=140,
                                                           text="What are my newest habits?",
                                                           command=lambda: self.information_window(
                                                               ["You don't have any current habits."], 300))

        if var_oldest:
            oldest_list = ["Your oldest habits are:"]
            for i, (current_text, current_date) in enumerate(zip(var_oldest, var_oldest_date)):
                oldest_list.append(f"{i + 1}. {current_text}, created on "
                                   f"{dt.strptime(str(current_date), '%Y-%m-%d %H:%M:%S').strftime('%d. %B %Y')}")
            self.my_habits_oldest_habit_button = tk.Button(self.main_frame, wraplength=140,
                                                           text="What are my oldest habits?",
                                                           command=lambda: self.information_window(oldest_list, 300))
        else:
            self.my_habits_oldest_habit_button = tk.Button(self.main_frame, wraplength=140,
                                                           text="What are my oldest habits?",
                                                           command=lambda: self.information_window(
                                                               ["You don't have any current habits."], 300))

        if var_longest and var_longest_length[0] != 0:
            longest_list = ["Your longest streaks are:"]
            for i, (current_text, current_length) in enumerate(zip(var_longest, var_longest_length)):
                if current_length != 0:
                    longest_list.append(f"{i + 1}. {current_text}, running for {current_length} days.")
            self.my_habits_longest_streak_button = tk.Button(self.main_frame, wraplength=140,
                                                             text="What are my longest streaks?",
                                                             command=lambda: self.information_window(
                                                                 longest_list, 300))
        else:
            self.my_habits_longest_streak_button = tk.Button(self.main_frame, wraplength=140,
                                                             text="What are my longest streaks?",
                                                             command=lambda: self.information_window(
                                                                 ["You don't have any current streaks."], 300))

        if var_most_broken and var_most_broken_number[0] != 0:
            most_broken_list = ["The following habits were most broken:"]
            for i, (current_text, current_length) in enumerate(zip(var_most_broken, var_most_broken_number)):
                if current_length != 0:
                    most_broken_list.append(f"{i + 1}. The streak of {current_text} was broken {current_length} times.")
            self.my_habits_most_broken_button = tk.Button(self.main_frame, wraplength=140,
                                                          text="Which habits did I break most often?",
                                                          command=lambda: self.information_window(most_broken_list,
                                                                                                  300))
        else:
            self.my_habits_most_broken_button = tk.Button(self.main_frame, wraplength=140,
                                                          text="Which habits did I break most often?",
                                                          command=lambda: self.information_window(
                                                              ["You didn't break any habits, good job!"], 300))

        if var_due_today:
            due_today_list = ["The following habits are due today:"]
            for i, current_text in enumerate(var_due_today):
                due_today_list.append(f"{i + 1}. {current_text}")
            self.my_habits_due_today_button = tk.Button(self.main_frame, text="What's due today?",
                                                        command=lambda: self.information_window(due_today_list, 300))
        else:
            self.my_habits_due_today_button = tk.Button(self.main_frame, text="What's due today?",
                                                        command=lambda: self.information_window(
                                                            ["No habits are due today!"], 300))

        if var_coming_up_names:
            coming_up_list = ["The following habits are due in the next days:"]
            for i, (current_text, current_date) in enumerate(zip(var_coming_up_names, var_coming_up_dates)):
                # Calculates the time difference from today to the due date of the respective habit.
                var_cd = (dt.strptime(str(current_date), '%y%j').date() -
                          dt.strptime(str(var_today), '%y%j').date()).days
                coming_up_list.append(f"{i + 1}. {current_text} is due in {var_cd} days.")
            self.my_habits_coming_up_button = tk.Button(self.main_frame, wraplength=140,
                                                        text="What's due in the next days?",
                                                        command=lambda: self.information_window(coming_up_list,
                                                                                                300))
        else:
            self.my_habits_coming_up_button = tk.Button(self.main_frame, wraplength=140,
                                                        text="What's due in the next days?",
                                                        command=lambda: self.information_window(
                                                            ["Nothing is due in the next days!"], 300))
        if var_overdue_names:
            overdue_list = ["You failed to complete the following habits in time:"]
            for i, (current_text, current_date) in enumerate(zip(var_overdue_names, var_overdue_dates)):
                # Calculates how many days have past since the due date.
                var_od = -(dt.strptime(str(var_overdue_dates[i]), '%y%j').date() -
                           dt.strptime(str(var_today), '%y%j').date()).days
                overdue_list.append(f"{i + 1}. {current_text} was due {var_od} days ago.")
            self.my_habits_overdue_button = tk.Button(self.main_frame, wraplength=140,
                                                      text="Which habits did I miss?",
                                                      command=lambda: self.information_window(overdue_list,
                                                                                              300))
        else:
            self.my_habits_overdue_button = tk.Button(self.main_frame, wraplength=140,
                                                      text="Which habits did I miss?",
                                                      command=lambda: self.information_window(
                                                          ["You missed no habits!"], 300))
        self.my_habits_back_button = tk.Button(self.main_frame, text="back", command=self.main_menu)

        # Creating and displaying buttons are separated, otherwise the get() method may return a 'NoneType'
        # AttributeError

        # Display menu contents
        self.my_habits_habit_information_button.place(height=50, width=150, x=10, y=10)
        self.my_habits_view_all_habits_button.place(height=50, width=150, x=10, y=70)
        self.my_habits_newest_habit_button.place(height=50, width=150, x=10, y=130)
        self.my_habits_oldest_habit_button.place(height=50, width=150, x=10, y=190)
        self.my_habits_longest_streak_button.place(height=50, width=150, x=10, y=250)
        self.my_habits_most_broken_button.place(height=50, width=150, x=10, y=310)
        self.my_habits_due_today_button.place(height=50, width=150, x=10, y=370)
        self.my_habits_coming_up_button.place(height=50, width=150, x=10, y=430)
        self.my_habits_overdue_button.place(height=50, width=150, x=10, y=490)
        self.my_habits_back_button.place(height=50, width=150, x=10, y=550)


    def view_all_habits(self):
        """
        Creates the menu to view all habits of a given periodicity.
        """
        # This function is executed when the "Show!" button is pressed.
        def show_habits():
            # Clears the table of old content.
            self.view_all_habits_table.delete(*self.view_all_habits_table.get_children())
            var_selector = self.view_habits_select_habit_periodicity.get()
            # Returns all habits.
            if var_selector == "all":
                var_list = Database.return_all_habit_names(self)
            # Returns only the habits of a given periodicity.
            else:
                var_list = Database.get_all_habits_of_a_periodicity(self, var_selector)
            for i in var_list:
                # Replace is used to display habit names which include spaces completely, not only the first part.
                self.view_all_habits_table.insert("", tk.END, values=i.replace(" ", "\ "))

        self.create_main_frame()

        # Creates a list of all periodicities in the database, set() removes duplicate entries.
        var_all_periodicities = Database.single_query(self, "habit_periodicity", "habit_periodicity", "ASC")
        var_periodicity_list = list(set(var_all_periodicities)) + ["all"]

        # Create menu content.
        self.view_habits_back_button = tk.Button(self.main_frame, text="back", command=self.my_habits)
        self.view_habits_select_habit_periodicity = tt.Combobox(self.main_frame, values=var_periodicity_list)
        try:
            self.view_habits_select_habit_periodicity.current(len(var_periodicity_list)-1)
        except:
            pass
        self.view_habits_show_habits = tk.Button(self.main_frame, text="Show!", command=show_habits)
        self.view_habits_label = tk.Label(self.main_frame, anchor='w', text="Select periodicity (in days):")

        self.view_all_habits_table = tt.Treeview(self.main_frame, height=10, column=("c1"), show='headings')
        self.ysb = tk.Scrollbar(self.main_frame, orient='vertical', command=self.view_all_habits_table.yview)
        self.view_all_habits_table_horizontal_scroll_bar = tt.Scrollbar(self.main_frame, orient="horizontal",
                                                                        command=self.view_all_habits_table.xview)
        self.view_all_habits_table.configure(yscrollcommand=self.ysb.set)
        self.view_all_habits_table.column("#1", anchor=tk.W, width=287)
        self.view_all_habits_table.heading("#1", text="Habit name")

        # Display menu content.
        self.view_habits_select_habit_periodicity.place(height=25, width=150, x=170, y=245)
        self.view_habits_label.place(height=25, width=150, x=10, y=245)
        self.view_habits_show_habits.place(height=50, width=150, x=10, y=280)
        self.view_habits_back_button.place(height=50, width=150, x=170, y=280)
        self.view_all_habits_table.place(x=10, y=10)
        self.ysb.place(height=225, width=20, x=300, y=11)

    def habit_details(self):
        """
        Creates the menu to view the details of a single habit.
        """
        # This function runs when the "Ok!" button is pressed.
        def get_info():
            # Ensures the habit list is not empty.
            if Database.return_all_habit_names(self):
                var_habit_name = self.habit_details_select_habit.get()
                items = Database.get_habit_details(self, var_habit_name)
                var_start_date = str(items[3])
                var_start_date = dt.strptime(var_start_date, "%y%j").strftime("%d. %B %Y")
                var_created = dt.strptime(str(items[2]), "%Y-%m-%d %H:%M:%S").strftime("%d. %B %Y %H:%M:%S")
                if items[4] != 0:
                    var_end_date = str(items[4])
                    var_end_date = dt.strptime(var_end_date, "%y%j").strftime("%d. %B %Y")
                    # Information for any habit.
                    self.information_window(
                        [f"The habit {items[0]} was created on {var_created} and is due every {items[1]} days.",
                         f"The current streak started on {var_start_date}, is running for {items[7]} days,",
                         f"and the habit was completed {items[9]} times during this period, last on {var_end_date}.",
                         f"The longest streak for this habit is {items[8]} days.",
                         f"In total, you broke your streak for this habit {items[11]} times."], 300)
                # Information for any new habit.
                else:
                    self.information_window(
                        [f"The habit {items[0]} was created on {var_created} and is due every {items[1]} days.",
                         f"So far, it has never been checked off..."], 300)
            # Information if no habits exist.
            else:
                self.information_window([f"You have no current habits!"], 300)

        items = Database.return_all_habit_names(self)

        self.create_main_frame()
        # Create
        self.habit_details_select_habit = tt.Combobox(self.main_frame, values=items)
        self.habit_details_ok_button = tk.Button(self.main_frame, text="Ok!", command=get_info)
        self.habit_details_back_button = tk.Button(self.main_frame, text="back", command=self.my_habits)

        try:
            self.habit_details_select_habit.current(0)
        except:
            pass

        # Create and display are separated so that the get() method will not return 'NoneType' AttributeError

        # Display
        self.habit_details_select_habit.place(height=25, width=310, x=10, y=10)
        self.habit_details_ok_button.place(height=50, width=150, x=10, y=45)
        self.habit_details_back_button.place(height=50, width=150, x=170, y=45)
        pass

    def delete_habits(self):
        def confirm_deletion():
            var_get_habit = self.delete_habits_select_habit.get()
            if var_get_habit != "":
                message = f"Do you want to delete the habit {var_get_habit}?"

                self.popup = tk.Tk()
                self.popup.geometry("300x80+400+150")
                self.popup.title("Please confirm")
                var_label_size = 100
                new_label = tk.Label(self.popup, text=message)
                new_label.place(height=25, x=10, y=10)
                self.popup.update()
                if new_label.winfo_width() > var_label_size:
                    var_label_size = new_label.winfo_width()
                self.popup.geometry(f"{var_label_size + 20}x80")
                self.yes_button = tk.Button(self.popup, text="Yes", command=lambda: delete_habit(var_get_habit)).place(
                    height=25, width=50, x=50, y=45)
                self.no_button = tk.Button(self.popup, text="No", command=self.popup.destroy).place(
                    height=25, width=50, x=var_label_size - 80, y=45)

            else:
                pass

        def delete_habit(var):
            Database.delete_a_habit(self, var)
            self.popup.destroy()
            self.delete_habits()

        items = Database.return_all_habit_names(self)

        self.create_main_frame()

        # Create menu content.
        self.delete_habits_select_habit = tt.Combobox(self.main_frame, values=items)
        try:
            self.delete_habits_select_habit.current(0)
        except:
            pass
        self.delete_habits_delete_habit = tk.Button(self.main_frame, text="Delete this habit", command=confirm_deletion)
        self.delete_habits_back_button = tk.Button(self.main_frame, text="back", command=self.main_menu)

        # Display menu content.
        self.delete_habits_select_habit.place(height=25, width=310, x=10, y=10)
        self.delete_habits_delete_habit.place(height=50, width=150, x=10, y=45)
        self.delete_habits_back_button.place(height=50, width=150, x=170, y=45)

    def check_off_habits(self):
        """
        Creates the menu to check off a given habit.
        """
        # This function is executed when the "Check off!" button is pressed.
        def check_off():
            habit_name = self.check_off_habits_select_habit.get()
            if not habit_name == "No more habits due today!":
                var_response = Database.check_off_a_habit(self, habit_name)
                self.information_window(var_response, 300)

        # Returns a list of all habits in the database.
        items = Database.return_all_habit_names(self)
        if not items:
            items = ["No more habits due today!"]

        self.create_main_frame()

        # Create menu content.
        self.check_off_habits_back_button = tk.Button(self.main_frame, text="back", command=self.main_menu)
        self.check_off_habits_select_habit = tt.Combobox(self.main_frame, values=items)
        self.check_off_habits_check_off_button = tk.Button(self.main_frame, text="Check off!", command=check_off)
        try:
            self.check_off_habits_select_habit.current(0)
        except:
            pass

        # Display menu content.
        self.check_off_habits_select_habit.place(height=25, width=310, x=10, y=10)
        self.check_off_habits_check_off_button.place(height=50, width=150, x=10, y=45)
        self.check_off_habits_back_button.place(height=50, width=150, x=170, y=45)


class Database():
    def __init__(self):
        """
        Creates the database table if it does not exist and fills it with the initial 5 demo habits.
        All fields that are used for calculations are of type INTEGER.
        """
        conn = sq.connect("main.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS database(
            habit_name TEXT,
            habit_periodicity INTEGER,
            created TEXT,
            start_streak INTEGER,
            end_streak INTEGER,
            due_date INTEGER,
            day_week_flag TEXT,
            days_running INTEGER,
            longest_streak INTEGER,
            accomplished INTEGER,
            accomplished_max INTEGER,
            number_streak_broken INTEGER
            )
            """)
        c.execute("SELECT * FROM database")
        # If the database is empty, the 5 demo habits are created and inserted.
        if not c.fetchall():
            c.execute("INSERT INTO database VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (
                          "Do the laundry - Sample",
                          3,
                          (dt.now() - tdelta(days=35)).strftime("%Y-%m-%d 11:08:00"),
                          int((da.today() - tdelta(days=10)).strftime("%y%j")),
                          int(da.today().strftime("%y%j")),
                          int((da.today() + tdelta(days=3)).strftime("%y%j")),
                          "d",
                          11,
                          17,
                          6,
                          8,
                          2
                      ))
            c.execute("INSERT INTO database VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (
                          "Go for a jog - Sample",
                          2,
                          (dt.now() - tdelta(days=34)).strftime("%Y-%m-%d 09:32:00"),
                          int((da.today() - tdelta(days=2)).strftime("%y%j")),
                          int(da.today().strftime("%y%j")),
                          int((da.today() + tdelta(days=2)).strftime("%y%j")),
                          "d",
                          3,
                          7,
                          3,
                          5,
                          5
                      ))
            c.execute("INSERT INTO database VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (
                          "Eat vegetables - Sample",
                          1,
                          (dt.now() - tdelta(days=33)).strftime("%Y-%m-%d 17:45:00"),
                          int((da.today() - tdelta(days=4)).strftime("%y%j")),
                          int((da.today() - tdelta(days=1)).strftime("%y%j")),
                          int(da.today().strftime("%y%j")),
                          "d",
                          5,
                          6,
                          5,
                          6,
                          6
                      ))
            c.execute("INSERT INTO database VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (
                          "Clean the apartment - Sample",
                          7,
                          (dt.now() - tdelta(days=32)).strftime("%Y-%m-%d 15:09:00"),
                          int((da.today() - tdelta(days=32)).strftime("%y%j")),
                          int((da.today() - tdelta(days=3)).strftime("%y%j")),
                          int((da.today() + tdelta(days=4)).strftime("%y%j")),
                          "w",
                          33,
                          33,
                          6,
                          6,
                          0
                      ))
            c.execute("INSERT INTO database VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (
                          "Go to the gym - Sample",
                          2,
                          (dt.now() - tdelta(days=31)).strftime("%Y-%m-%d 18:56:00"),
                          int((da.today() - tdelta(days=5)).strftime("%y%j")),
                          int((da.today() - tdelta(days=5)).strftime("%y%j")),
                          int((da.today() - tdelta(days=4)).strftime("%y%j")),
                          "d",
                          1,
                          1,
                          1,
                          1,
                          6
                      ))
        conn.commit()
        conn.close()

    def new_habit_entry(self, var_habit_name, var_habit_periodicity, var_habit_dayweek):
        """
        Used to enter a new habit into the database table.
        """
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        # Inserts the name, periodicity and whether the periodicity is given in days or weeks into the database and
        # sets the default values for the other fields.
        c.execute("""INSERT INTO database VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (
                      var_habit_name,
                      var_habit_periodicity,
                      dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                      int(da.today().strftime("%y%j")),
                      0,
                      int(da.today().strftime("%y%j")),
                      var_habit_dayweek,
                      0,
                      0,
                      0,
                      0,
                      0)
                  )
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()

    def check_off_a_habit(self, var_habit_name):
        """
        Used to mark a habit as completed for the day.
        Checks whether or not a habit has already been completed today.
        Then checks whether the habit was completed in time, i.e. before the due date.
        Returns a response accordingly, which can be used in the Gui.information_window method.
        """
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()

        # Queries the database for the values of the habit to be checked off.
        c.execute("""SELECT due_date, habit_periodicity, days_running, longest_streak, accomplished, accomplished_max, 
            number_streak_broken, end_streak, day_week_flag FROM database WHERE habit_name = :habitname""",
            {"habitname": var_habit_name})
        var_due_date, var_periodicity, var_days_running, var_longest_streak, var_accomplished, var_accomplished_max,\
            var_number_broken, var_end_streak, var_day_week_flag = c.fetchall()[0]

        # Defines additional variables.
        var_response = []
        var_julian_today = da.today().strftime("%y%j")

        # Integer values of due date, end streak date and current date are converted into datetime.date class objects
        if var_due_date != 0:
            var_due_date = dt.strptime(str(var_due_date), "%y%j").date()
        if var_end_streak != 0:
            var_end_streak = dt.strptime(str(var_end_streak), "%y%j").date()
        var_julian_today = dt.strptime(str(var_julian_today), "%y%j").date()

        # First, it is checked whether the habit has not been completed today.
        if var_end_streak != var_julian_today:
            # Checks if a habit is completed for the first time after creation and updates values accordingly.
            if var_end_streak == 0:
                var_response = [f"Congratulations, you completed {var_habit_name} for the first time!"]
                c.execute("""UPDATE database SET
                        start_streak = :startstreak,
                        end_streak = :endstreak,
                        due_date = :duedate,
                        days_running = :daysrunning,
                        longest_streak = :longeststreak,
                        accomplished = :accomplished,
                        accomplished_max = :accomplished_max
                    WHERE habit_name = :habitname""",
                          {
                              "startstreak": var_julian_today.strftime("%y%j"),
                              "endstreak": var_julian_today.strftime("%y%j"),
                              "duedate": (var_julian_today + tdelta(days=var_periodicity)).strftime("%y%j"),
                              "daysrunning": 1,
                              "longeststreak": 1,
                              "accomplished": 1,
                              "accomplished_max": 1,
                              "habitname": var_habit_name
                          })
            # Checks if a habit is completed in time and updates values accordingly.
            elif var_due_date >= var_julian_today:
                var_response = [f"Congratulations for maintaining your {var_days_running + 1} day streak!"]
                c.execute("""UPDATE database SET
                        end_streak = :endstreak,
                        due_date = :duedate,
                        days_running = :daysrunning,
                        accomplished = :accomplished
                    WHERE habit_name = :habitname""",
                          {
                              "endstreak": var_julian_today.strftime("%y%j"),  # Als Julian date
                              "duedate": (var_julian_today + tdelta(days=var_periodicity)).strftime("%y%j"),
                              "daysrunning": var_days_running + 1,
                              "accomplished": var_accomplished + 1,
                              "habitname": var_habit_name
                          })
                if var_days_running + 1 > var_longest_streak:
                    c.execute("""UPDATE database SET
                            longest_streak = :longeststreak
                        WHERE habit_name = :habitname""",
                              {
                                  "longeststreak": var_longest_streak + 1,
                                  "habitname": var_habit_name
                              })
                if var_accomplished + 1 > var_accomplished_max:
                    c.execute("""UPDATE database SET
                            accomplished_max = :accomplished_max
                        WHERE habit_name = :habitname""",
                              {
                                  "accomplished_max": var_accomplished + 1,
                                  "habitname": var_habit_name
                              })
            # Checks if the streak is broken and updates values accordingly.
            elif var_due_date < var_julian_today:
                var_response = [f"Congratulations for completing this habit! Unfortunately, you broke your "
                                f"{var_days_running} day streak."]
                c.execute("""UPDATE database SET
                        start_streak = :startstreak,
                        end_streak = :endstreak,
                        due_date = :duedate,
                        days_running = :daysrunning,
                        accomplished = :accomplished,
                        number_streak_broken = :number_broken
                    WHERE habit_name = :habitname""",
                          {
                              "startstreak": var_julian_today.strftime("%y%j"),
                              "endstreak": var_julian_today.strftime("%y%j"),
                              "duedate": (var_julian_today + tdelta(days=var_periodicity)).strftime("%y%j"),
                              "daysrunning": 1,
                              "accomplished": 1,
                              "number_broken": var_number_broken + 1,
                              "habitname": var_habit_name
                          })
        # Returns only a message if the habit has already been completed today.
        else:
            var_response = [f"You already completed {var_habit_name} today!"]
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()
        return var_response

    def return_all_habit_names(self):
        """Returns the names of all habits in the database table."""
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        c.execute("SELECT habit_name FROM database ORDER BY created")
        items = [i[0] for i in c.fetchall()]
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()
        return items

    def delete_a_habit(self, var_habit_name):
        """Deletes a specified habit from the database table."""
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        c.execute("DELETE FROM database WHERE habit_name = (?)", [var_habit_name])
        conn.commit()
        conn.close()

    def return_habits_due_today(self):
        """
        Returns the names of all habits where the due date is today.
        """
        var_julian_today = int(da.today().strftime("%y%j"))
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        c.execute("SELECT habit_name FROM database WHERE due_date = (?) ORDER BY created", [var_julian_today])
        items = [i[0] for i in c.fetchall()]
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()
        return items

    def return_habits_coming_up(self):
        """
        Returns the names and due dates of all habits where the due date is greater than the current date.
        """
        var_julian_today = int(da.today().strftime("%y%j"))
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        c.execute("SELECT habit_name FROM database WHERE due_date > (?) ORDER BY due_date",
                  [var_julian_today])
        var_names = [i[0] for i in c.fetchall()]
        c.execute("SELECT due_date FROM database WHERE due_date > (?) ORDER BY due_date", [var_julian_today])
        var_due_date = [i[0] for i in c.fetchall()]
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()
        return var_names, var_due_date

    def return_overdue_habits(self):
        """Returns the names and due dates of all habits where the due date is in the past."""
        var_julian_today = int(da.today().strftime("%y%j"))
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        c.execute("SELECT habit_name FROM database WHERE due_date < (?) ORDER BY due_date",
                  [var_julian_today])
        var_names = [i[0] for i in c.fetchall()]
        c.execute("SELECT due_date FROM database WHERE due_date < (?) ORDER BY due_date", [var_julian_today])
        var_due_date = [i[0] for i in c.fetchall()]
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()
        return var_names, var_due_date

    def single_query(self, var_return, var_order_1, var_asc_desc_1="DESC", var_order_2="created",
                     var_asc_desc_2="DESC"):
        """
        Sorts the table by 2 columns and returns a specified value.
        :param var_return: The return variable.
        :type var_return: str
        :param var_order_1: The first variable to sort by.
        :type var_order_1: str
        :param var_asc_desc_1: The first sort order. (Optional)
        :type var_asc_desc_1: str
        :param var_order_2: The second variable to sort by. (Optional)
        :type var_order_2: str
        :param var_asc_desc_2: The second sort order. (Optional)
        :type var_asc_desc_2: str
        """
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        c.execute(
            f"SELECT {var_return} FROM database ORDER BY {var_order_1} {var_asc_desc_1}, {var_order_2} "
            f"{var_asc_desc_2}")
        items = [i[0] for i in c.fetchall()]
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()
        return items

    def get_habit_details(self, var_habit_name):
        """
        Returns all data fields of a given habit.
        :param var_habit_name: The requested habit.
        :type var_habit_name: str
        """
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        # Fetches the information of the requested habit.
        c.execute(f"SELECT * FROM database WHERE habit_name = '{var_habit_name}'")
        items = c.fetchall()[0]
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()
        return items

    def get_all_habits_of_a_periodicity(self, var_habit_periodicity):
        """
        Returns the habit names of all habits with a given periodicity.
        :param var_habit_periodicity: The requested periodicity.
        :type var_habit_periodicity: int
        """
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        # Creates a list of all habits with the given periodicity.
        c.execute(f"SELECT habit_name FROM database WHERE habit_periodicity = '{var_habit_periodicity}'")
        items = [i[0] for i in c.fetchall()]
        # Saves the changes to the database and closes the connection.
        conn.commit()
        conn.close()
        return items

    def check_exisiting(self, var_habit_name):
        """This method is used to check whether or not a habit already exists, returns True or False."""
        # Establishes a connection to the database.
        conn = sq.connect("main.db")
        c = conn.cursor()
        c.execute(f"SELECT * FROM database WHERE habit_name = '{var_habit_name}'")
        # Saves the changes to the database, closes the connection and returns True (habit exists) or False.
        if c.fetchone():
            conn.commit()
            conn.close()
            return True
        else:
            conn.commit()
            conn.close()
            return False


# The main function, Database() runs first to fill the database with the initial values if it is empty.
def main():
    Database()
    Gui()
    tk.mainloop()


# Runs the main function.
if __name__ == "__main__":
    main()