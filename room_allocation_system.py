from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        group_csv = request.files['group_csv']
        hostel_csv = request.files['hostel_csv']
        group_df = pd.read_csv(group_csv)
        hostel_df = pd.read_csv(hostel_csv)
        allocation = allocate_rooms(group_df, hostel_df)
        return render_template('index.html', allocation=allocation)
    return render_template('index.html')

def allocate_rooms(group_df, hostel_df):
    hostel_rooms = {}
    for index, row in hostel_df.iterrows():
        hostel_name = row['Hostel Name']
        room_number = row['Room Number']
        capacity = row['Capacity']
        gender = row['Gender']
        if hostel_name not in hostel_rooms:
            hostel_rooms[hostel_name] = []
        hostel_rooms[hostel_name].append({'room_number': room_number, 'capacity': capacity, 'gender': gender})

    allocation = []
    for index, row in group_df.iterrows():
        group_id = row['Group ID']
        members = row['Members']
        gender = row['Gender']
        possible_rooms = []
        for hostel_name, rooms in hostel_rooms.items():
            if gender == 'Boys' and 'Boys' in hostel_name:
                possible_rooms.extend(rooms)
            elif gender == 'Girls' and 'Girls' in hostel_name:
                possible_rooms.extend(rooms)
        possible_rooms.sort(key=lambda x: x['capacity'], reverse=True)
        allocated = 0
        for room in possible_rooms:
            if room['capacity'] >= members - allocated:
                allocation.append({'Group ID': group_id, 'Hostel Name': hostel_name, 'Room Number': room['room_number'], 'Members Allocated': members - allocated})
                allocated += room['capacity']
                break
            else:
                allocation.append({'Group ID': group_id, 'Hostel Name': hostel_name, 'Room Number': room['room_number'], 'Members Allocated': room['capacity']})
                allocated += room['capacity']

    return allocation

if __name__ == '__main__':
    app.run(debug=True)
