# This file is part of Open Juice Calc.
#
# Open Juice Calc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Open Juice Calc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YourProjectName. If not, see <https://www.gnu.org/licenses/>.


import os
import customtkinter as CTk
global frame_window


def get_values_from_gui():
    """Gets the values from the gui entries. Returns them as a list to be used by calculate_recipe()"""

    values = [total_entry.get(), desired_strength_entry.get(), desired_pg_entry.get(), desired_vg_entry.get(),
              nicotine_base_strength_entry.get(), nicotine_pg_entry.get(), nicotine_vg_entry.get()]
    return values


def calculate_recipe():
    """Does all the math and creates the recipe string."""

    # Creates list of all the data needed for the recipe calculation
    values = get_values_from_gui()

    # Start of GUI code for recipe window
    # Creates the popup window for the recipe
    recipe_popup_window = CTk.CTkToplevel(app)
    recipe_popup_window.title("Recipe")
    recipe_popup_window.geometry(app.geometry())
    recipe_popup_window.resizable(height=False, width=False)

    recipe_popup_frame = CTk.CTkFrame(recipe_popup_window)
    recipe_popup_frame.pack(expand=True)

    # Waits for the popup window to fully open then locks the main window (app)
    recipe_popup_window.wait_visibility()
    recipe_popup_window.grab_set()

    # Creates a textbox for the recipe to be populated to
    recipe_box = CTk.CTkTextbox(recipe_popup_frame, width=300, height=400)
    recipe_box.pack(anchor=CTk.CENTER)

    # Creates the button to save the recipe - calls save_recipe.
    save_recipe_button = CTk.CTkButton(recipe_popup_frame, text="Save Recipe", command=lambda: save_recipe())
    save_recipe_button.pack(fill=CTk.X)

    def save_recipe():
        """Saves the recipe to a text document in .../'Recipes' and creates the directory if it doesn't exist."""

        def okay_button():
            """Creates the text document that the recipe will be saved in and destroys recipe_name_popup."""
            recipe_name = recipe_name_entry.get()
            recipe_name_popup.destroy()

            current_directory = os.getcwd()
            recipe_directory = os.path.join(current_directory, "Recipes")

            os.makedirs(recipe_directory, exist_ok=True)

            file_path = os.path.join(recipe_directory, f"{recipe_name}.txt")

            with open(file_path, "w") as file:
                file.write(recipe_box.get("1.0", "end-1c"))

        # Creates a popup window for the recipe name to be entered in
        recipe_name_popup = CTk.CTkToplevel(recipe_popup_window)
        recipe_name_popup.title("Recipe Name")
        recipe_name_popup.geometry("300x100")
        recipe_name_popup.resizable(height=False, width=False)

        # Creates the entry for the user to input the name of the recipe
        recipe_name_entry = CTk.CTkEntry(recipe_name_popup)
        recipe_name_entry.pack()

        ok_button = CTk.CTkButton(recipe_name_popup, text="OK", command=lambda: okay_button())
        ok_button.pack()

    # Math that calculates the final needed amount of each ingredient
    try:
        vg_needed = float(values[0]) * float(values[3]) / 100
        pg_needed = float(values[0]) * float(values[2]) / 100
        nicotine_base_needed = float(values[0]) * float(values[1]) / float(values[4])
        base_vg_amount = nicotine_base_needed * float(values[6]) / 100
        base_pg_amount = nicotine_base_needed * float(values[5]) / 100
        pg_needed -= base_pg_amount
        vg_needed -= base_vg_amount
        flavor_values = [flavor.get() for flavor in flavor_amounts] # Gets the flavor values from the list of entries

        for item in flavor_values:
            item = float(values[0]) * float(item) / 100
            pg_needed -= item

        recipe_string = f"VG: {vg_needed} ml ({round(vg_needed * 1.261, 2)} grams)\n" \
                        f"PG: {pg_needed} ml ({round(pg_needed * 1.038, 2)} grams)\n" \
                        f"Nicotine Base: {round(nicotine_base_needed, 2)} " \
                        f"ml ({round(base_vg_amount * 1.261 + base_pg_amount * 1.038, 2)} grams)\n"

        current_flavor = 0
        for item in flavor_values:
            item = float(values[0]) * float(item) / 100
            recipe_string += f"{names_of_flavors[current_flavor].get()}: {item} ml ({round(float(item) * 1.038, 2)} grams)\n"
            current_flavor += 1

        recipe_box.insert("end", text=recipe_string)

    except:
        # Triggers if any error is detected when making the recipe
        recipe_box.insert("end", text="Something has gone wrong.\nCheck your inputs and try again.")


def add_flavor_to_gui():
    """Adds Flavor Name and Flavor Amount entries to the gui -
    appends these entries to names_of_flavors and flavor_amounts to be accessed later."""

    flavor_name_entry = CTk.CTkEntry(frame)
    flavor_name_entry.pack(pady=(5, 0), side=CTk.TOP, fill=CTk.Y)
    flavor_name_entry.insert(0, "Flavor Name")
    flavor_name_entry.bind('<FocusIn>', lambda event: click_entry(event, flavor_name_entry, 'Flavor Name')) # Binds click_entry() to focusing the entry
    flavor_name_entry.bind('<FocusOut>', lambda event: leave_entry(event, flavor_name_entry, 'Flavor Name'))# Binds leave_entry() to unfocusing the entry
    names_of_flavors.append(flavor_name_entry)

    flavor_amount_entry = CTk.CTkEntry(frame)
    flavor_amount_entry.pack(pady=(0, 5), side=CTk.TOP, fill=CTk.Y)
    flavor_amount_entry.insert(0, "Flavor Amount")
    flavor_amounts.append(flavor_amount_entry)
    flavor_amount_entry.bind('<FocusIn>', lambda event: click_entry(event, flavor_amount_entry, 'Flavor Amount'))
    flavor_amount_entry.bind('<FocusOut>', lambda event: leave_entry(event, flavor_amount_entry, 'Flavor Amount'))

    e_juice_calc_canvas.configure(scrollregion=e_juice_calc_canvas.bbox("all"))


def remove_flavor_from_gui():
    """"Removes the last flavor added to the gui if there is one on screen.
    Also removes the flavor from names_of_flavors and flavor_amounts"""
    if len(names_of_flavors) > 0:
        name = names_of_flavors.pop()
        amount = flavor_amounts.pop()
        name.destroy()
        amount.destroy()


def click_entry(event, entry, placeholder_text):
    """"Removes placeholder text from entries when they are clicked."""

    if entry.get() == placeholder_text:
        entry.delete(0, "end")  # delete all the text in the entry


def leave_entry(event, entry, placeholder_text):
    """"Replaces placeholder text in entries if the user did not enter anything or entered only spaces in them. """
    # Repeats for each entry
    if entry.get().strip(" ") == '':
        entry.delete(0, "end")
        entry.insert(0, placeholder_text)


def center_frame(event=None):
    """"Keeps the CTk widgets centered"""
    global frame_window
    # Ensure 'frame_window' is defined before using, as <Configure> can trigger before its initialization.
    if 'frame_window' in globals():
        canvas_width = e_juice_calc_canvas.winfo_width()
        e_juice_calc_canvas.itemconfig(frame_window, anchor="n")
        e_juice_calc_canvas.coords(frame_window, canvas_width/2, 0)


# Config variable loading:
with open("cfg.txt") as cfg:
    DATA = cfg.readlines()
    THEME = DATA[0].strip("THEME=").replace("\n", "")

# Lists and variable to hold flavors and names:
names_of_flavors = []
flavor_amounts = []

# Start of GUI code for main window
app = CTk.CTk()
window_height = app.winfo_screenheight() - 100
app.geometry(f"400x{window_height}")
app.resizable(height=False, width=False)
app.title("Open Juice Calc")
CTk.set_appearance_mode(THEME)
theme_color = app.cget("background")

e_juice_calc_canvas = CTk.CTkCanvas(app, bg=theme_color)
e_juice_calc_canvas.bind("<Configure>", center_frame)
e_juice_calc_canvas.pack(side=CTk.LEFT, fill=CTk.BOTH, expand=True)

scrollbar = CTk.CTkScrollbar(app, command=e_juice_calc_canvas.yview)
scrollbar.configure(bg_color=theme_color)
scrollbar.pack(side=CTk.RIGHT, fill=CTk.Y)

e_juice_calc_canvas.configure(yscrollcommand=scrollbar.set, bg=theme_color, highlightthickness=0)

frame = CTk.CTkFrame(e_juice_calc_canvas, bg_color=theme_color)
frame_window = e_juice_calc_canvas.create_window((0, 0), window=frame, anchor="n")

# Entry for the total amount of E juice to make in ml
total_entry = CTk.CTkEntry(frame)
total_entry.insert(0, "Total")
total_entry.bind('<FocusIn>', lambda event: click_entry(event, total_entry, 'Total')) # Binds click_entry() to focusing the entry
total_entry.bind('<FocusOut>', lambda event: leave_entry(event, total_entry, 'Total')) # Binds leave_entry() to unfocusing the entry
total_entry.pack(pady=(5, 5))

# Entry for the desired nicotine strength in mg/ml
desired_strength_entry = CTk.CTkEntry(frame)
desired_strength_entry.insert(0, "Desired Strength")
desired_strength_entry.bind('<FocusIn>', lambda event: click_entry(event, desired_strength_entry, 'Desired Strength'))
desired_strength_entry.bind('<FocusOut>', lambda event: leave_entry(event, desired_strength_entry, 'Desired Strength'))
desired_strength_entry.pack(pady=(5, 5))

# Entry for desired pg in %
desired_pg_entry = CTk.CTkEntry(frame)
desired_pg_entry.insert(0, "Desired PG")
desired_pg_entry.bind('<FocusIn>', lambda event: click_entry(event, desired_pg_entry, 'Desired PG'))
desired_pg_entry.bind('<FocusOut>', lambda event: leave_entry(event, desired_pg_entry, 'Desired PG'))
desired_pg_entry.pack(pady=(5, 5))

# Entry for desired vg in %
desired_vg_entry = CTk.CTkEntry(frame)
desired_vg_entry.insert(0, "Desired VG")
desired_vg_entry.bind('<FocusIn>', lambda event: click_entry(event, desired_vg_entry, 'Desired VG'))
desired_vg_entry.bind('<FocusOut>', lambda event: leave_entry(event, desired_vg_entry, 'Desired VG'))
desired_vg_entry.pack(pady=(5, 5))

# Entry for strength of the nicotine base in mg/ml
nicotine_base_strength_entry = CTk.CTkEntry(frame)
nicotine_base_strength_entry.insert(0, "Nicotine Base Strength")
nicotine_base_strength_entry.bind('<FocusIn>', lambda event: click_entry(event, nicotine_base_strength_entry, 'Nicotine Base Strength'))
nicotine_base_strength_entry.bind('<FocusOut>', lambda event: leave_entry(event, nicotine_base_strength_entry, 'Nicotine Base Strength'))
nicotine_base_strength_entry.pack(pady=(5, 5))

# Entry for amount of pg in nicotine base in %
nicotine_pg_entry = CTk.CTkEntry(frame)
nicotine_pg_entry.insert(0, "Nicotine Base PG")
nicotine_pg_entry.bind('<FocusIn>', lambda event: click_entry(event, nicotine_pg_entry, 'Nicotine Base PG'))
nicotine_pg_entry.bind('<FocusOut>', lambda event: leave_entry(event, nicotine_pg_entry, 'Nicotine Base PG'))
nicotine_pg_entry.pack(pady=(5, 5))

# Entry for amount of vg in nicotine base in %
nicotine_vg_entry = CTk.CTkEntry(frame)
nicotine_vg_entry.insert(0, "Nicotine Base VG")
nicotine_vg_entry.bind('<FocusIn>', lambda event: click_entry(event, nicotine_vg_entry, 'Nicotine Base VG'))
nicotine_vg_entry.bind('<FocusOut>', lambda event: leave_entry(event, nicotine_vg_entry, 'Nicotine Base VG'))
nicotine_vg_entry.pack(pady=(5, 5))


# Button triggers calculate_recipe() - Has extra padding to prevent buttons from going off-screen if a lot of flavors
# are added to the gui.
calculate_recipe_button = CTk.CTkButton(frame, text="Calculate Recipe", command=lambda: calculate_recipe())
calculate_recipe_button.pack(pady=(5, 80), side=CTk.BOTTOM, fill=CTk.Y)

# Button removes the last flavor from the gui
remove_flavors_button = CTk.CTkButton(frame, text="Remove Flavor", command=lambda: remove_flavor_from_gui())
remove_flavors_button.pack(pady=(5, 0), side=CTk.BOTTOM, fill=CTk.Y)

# Button adds a flavor to the  gui
add_flavors_button = CTk.CTkButton(frame, text="Add Flavor", command=lambda: add_flavor_to_gui())
add_flavors_button.pack(pady=(5, 0), side=CTk.BOTTOM, fill=CTk.Y)

app.update()  # Update the main window - keeps widgets centered

app.mainloop()
