import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

class EstonianPeople:
    def __init__(self, data):
        self.data = data

    def total_people(self):
        return len(self.data)

    def longest_name(self):
        longest_name = max(self.data, key=lambda x: len(x.get('nimi', '')))
        return longest_name['nimi'], len(longest_name['nimi'])

    def oldest_living(self):
        today = datetime.today()
        living_people = [p for p in self.data if p.get('surnud') == '0000-00-00']
        living_people = [p for p in living_people if 'sundinud' in p and p['sundinud']]
        if not living_people:
            return None, None, None
        oldest = min(living_people, key=lambda x: datetime.strptime(x['sundinud'], '%Y-%m-%d'))
        birth_date = datetime.strptime(oldest['sundinud'], '%Y-%m-%d')
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return oldest['nimi'], age, birth_date.strftime('%d.%m.%Y')

    def oldest_deceased(self):
        deceased_people = [p for p in self.data if p.get('surnud') != '0000-00-00']
        deceased_people = [p for p in deceased_people if 'sundinud' in p and p['sundinud']]
        if not deceased_people:
            return None, None, None, None
        oldest = min(deceased_people, key=lambda x: datetime.strptime(x['sundinud'], '%Y-%m-%d'))
        death_date = datetime.strptime(oldest['surnud'], '%Y-%m-%d')
        birth_date = datetime.strptime(oldest['sundinud'], '%Y-%m-%d')
        age = death_date.year - birth_date.year - ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
        return oldest['nimi'], age, birth_date.strftime('%d.%m.%Y'), death_date.strftime('%d.%m.%Y')

    def total_actors(self):
        return sum(1 for p in self.data if 'amet' in p and 'näitleja' in p['amet'])

    def born_in_year(self, year):
        return sum(1 for p in self.data if 'sundinud' in p and datetime.strptime(p['sundinud'], '%Y-%m-%d').year == year)

    def unique_professions(self):
        professions = set(prof for p in self.data if 'amet' in p for prof in p['amet'].split(', '))
        return len(professions)

    def names_with_more_than_two_parts(self):
        return sum(1 for p in self.data if 'nimi' in p and len(p['nimi'].split(" ")) > 2)

    def same_birth_and_death_day_except_year(self):
        return sum(1 for p in self.data if
                   'sundinud' in p and 'surnud' in p and p['surnud'] != '0000-00-00' and datetime.strptime(
                       p['sundinud'], '%Y-%m-%d').strftime('%m-%d') == datetime.strptime(p['surnud'],
                                                                                         '%Y-%m-%d').strftime('%m-%d'))

    def living_and_deceased_counts(self):
        living = sum(1 for p in self.data if p.get('surnud') == '0000-00-00')
        deceased = sum(1 for p in self.data if p.get('surnud') != '0000-00-00')
        return living, deceased

# Function to open a file dialog and load JSON data
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON file. Please select a valid JSON file.")
                return

        # Create instance of EstonianPeople
        estonian_people = EstonianPeople(data)

        # Display results in a new Tkinter window
        display_results(estonian_people)

# Function to display results in a GUI window
def display_results(estonian_people):
    # Create a new Tkinter window
    window = tk.Tk()
    window.title("Estonian People Statistics")

    # Create labels and display results
    label1 = tk.Label(window, text=f"Isikute arv kokku: {estonian_people.total_people()}")
    label1.pack()

    longest_name_str, longest_name_length = estonian_people.longest_name()
    label2 = tk.Label(window, text=f"Kõige pikem nimi ja tähemärkide arv: {longest_name_str} ({longest_name_length})")
    label2.pack()

    oldest_living_name, oldest_living_age, oldest_birth_date = estonian_people.oldest_living()
    if oldest_living_name:
        label3 = tk.Label(window, text=f"Kõige vanem elav inimene: {oldest_living_name} ({oldest_living_age} aastat), sündinud {oldest_birth_date}")
        label3.pack()
    else:
        label3 = tk.Label(window, text="Pole elavaid inimesi andmetes")
        label3.pack()

    oldest_deceased_name, oldest_deceased_age, oldest_birth_date, oldest_death_date = estonian_people.oldest_deceased()
    if oldest_deceased_name:
        label4 = tk.Label(window, text=f"Kõige vanem surnud inimene: {oldest_deceased_name} ({oldest_deceased_age} aastat), sündinud {oldest_birth_date}, surnud {oldest_death_date}")
        label4.pack()
    else:
        label4 = tk.Label(window, text="Pole surnud inimesi andmetes")
        label4.pack()

    label5 = tk.Label(window, text=f"Näitlejate koguarv: {estonian_people.total_actors()}")
    label5.pack()

    label6 = tk.Label(window, text=f"Sündinud 1997 aastal: {estonian_people.born_in_year(1997)}")
    label6.pack()

    label7 = tk.Label(window, text=f"Erinevaid elukutseid: {estonian_people.unique_professions()}")
    label7.pack()

    label8 = tk.Label(window, text=f"Nimi sisaldab rohkem kui kaks nime: {estonian_people.names_with_more_than_two_parts()}")
    label8.pack()

    label9 = tk.Label(window, text=f"Sünniaeg ja surmaaeg sama v.a. aasta: {estonian_people.same_birth_and_death_day_except_year()}")
    label9.pack()

    living_count, deceased_count = estonian_people.living_and_deceased_counts()
    label10 = tk.Label(window, text=f"Elavaid isikuid: {living_count}")
    label10.pack()

    label11 = tk.Label(window, text=f"Surnud isikuid: {deceased_count}")
    label11.pack()

    window.mainloop()

# Create a Tkinter window for file selection
root = tk.Tk()
root.title("Vali JSON fail")

# Button to open file dialog
open_button = tk.Button(root, text="Ava fail", command=open_file)
open_button.pack(pady=20)

root.mainloop()
