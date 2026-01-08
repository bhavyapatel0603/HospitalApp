import streamlit as st
import sqlite3
import re
st.set_page_config(page_title="OHMS", page_icon="Fevicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)
# Database Setup
def create_tables():
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        Utype TEXT, 
        Fname TEXT, 
        Lname TEXT, 
        Mname TEXT, 
        Email TEXT UNIQUE, 
        City TEXT, 
        Password TEXT,
        doctor_type TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        patient_email TEXT, 
        doctor_email TEXT, 
        date TEXT, 
        time TEXT, 
        status TEXT DEFAULT "Pending")''')

    c.execute('''CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        patient_email TEXT, 
        doctor_email TEXT, 
        prescription TEXT)''')

    conn.commit()
    conn.close()

create_tables()  # Run once

# User Functions
def add_user(Utype, Fname, Lname, Mname, Email, City, Password, doctor_type=None):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('INSERT INTO users (Utype, Fname, Lname, Mname, Email, City, Password, doctor_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (Utype, Fname, Lname, Mname, Email, City, Password, doctor_type))
    conn.commit()
    conn.close()

def login_user(Email, Password):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE Email = ? AND Password = ?', (Email, Password))
    data = c.fetchone()
    conn.close()
    return data

# Appointment Functions
def book_appointment(patient_email, doctor_email, date, time):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    
    # Convert time to string before inserting
    time_str = time.strftime("%H:%M:%S")
    
    c.execute('INSERT INTO appointments (patient_email, doctor_email, date, time) VALUES (?, ?, ?, ?)',
              (patient_email, doctor_email, date, time_str))
    
    conn.commit()
    conn.close()

def get_doctors_by_type(doctor_type):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('SELECT Email FROM users WHERE Utype = "Doctor" AND doctor_type = ?', (doctor_type,))
    doctors = [row[0] for row in c.fetchall()]
    conn.close()
    return doctors

def get_appointments(user_email):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('SELECT * FROM appointments WHERE patient_email = ?', (user_email,))
    data = c.fetchall()
    conn.close()
    return data

def get_doctor_appointments(doctor_email):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('SELECT * FROM appointments WHERE doctor_email = ?', (doctor_email,))
    data = c.fetchall()
    conn.close()
    return data

def update_appointment_status(appointment_id, status):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('UPDATE appointments SET status = ? WHERE id = ?', (status, appointment_id))
    conn.commit()
    conn.close()

def delete_appointment(appointment_id):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
    conn.commit()
    conn.close()

# Prescription Functions
def add_prescription(patient_email, doctor_email, prescription_text):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('INSERT INTO prescriptions (patient_email, doctor_email, prescription) VALUES (?, ?, ?)',
              (patient_email, doctor_email, prescription_text))
    conn.commit()
    conn.close()

def get_prescriptions(patient_email):
    conn = sqlite3.connect("perception.db")
    c = conn.cursor()
    c.execute('SELECT doctor_email, prescription FROM prescriptions WHERE patient_email = ?', (patient_email,))
    data = c.fetchall()
    conn.close()
    return data
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
          f"""
          <style>
          .stApp {{
              background: url("https://elixiraid.com/wp-content/uploads/2016/09/Hospital-Management-System-1-1024x328.png");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()


st.title('Online Hospital Management System')
menu = ["Home", "SignUp", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice=="Home":
    st.markdown(
    """
    <p align="justify">
    <b style="color:black">The Online Hospital Management System app provides and efficient method of storing the prescription details of patient. It assists the patient to view their medicine anytime, anywhere through their phone. This medicine reminder is a simple smartphone app, and one that can help manage numerous people’s medication thanks to multiple profiles. It also tracks your prescriptions and reminds you when it’s time for a refill. An App. has been developed for entering the prescription details which is sent to the prescription viewer app present in the patient’s phone. Three people have access to the web site admin, doctor and receptionist. They can access the website by logging in using their respective username and password. The receptionist enters the details of the patients for the first time into the website when the patients visit the hospital.</b>
    </p>
    """
    ,unsafe_allow_html=True)
    

if choice == "SignUp":
    st.subheader("Sign Up")
    Utype = st.selectbox("User Type", ["Doctor", "Patient"])
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password", type="password")
    CPassword = st.text_input("Confirm Password", type="password")

    doctor_type = None
    if Utype == "Doctor":
        doctor_type = st.selectbox("Select Specialization", ["Cardiologist", "Dermatologist", "General Physician", "Neurologist", "Orthopedic", "Pediatrician"])

    if st.button("SignUp"):
        if Password == CPassword:
            pattern = re.compile(r"(0|91)?[7-9][0-9]{9}")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if pattern.match(Mname) and re.fullmatch(regex, Email):
                add_user(Utype, Fname, Lname, Mname, Email, City, Password, doctor_type)
                st.success("SignUp Success! Go to Login Section.")
            else:
                st.warning("Invalid Email or Mobile Number")
        else:
            st.warning("Passwords Do Not Match")


elif choice == "Login":
    st.subheader("Login")
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.checkbox("Login"):
        user = login_user(Email, Password)
        if user:
            st.success(f"Welcome {user[2]}!")

            if user[1] == "Patient":
                st.subheader("Book Appointment")
                doctor_type = st.selectbox("Select Doctor Type", ["Cardiologist", "Dermatologist", "General Physician", "Neurologist", "Orthopedic", "Pediatrician"])
                doctors = get_doctors_by_type(doctor_type)
                doctor_email = st.selectbox("Select Doctor", doctors) if doctors else st.warning("No doctors available for this specialization.")
                date = st.date_input("Appointment Date")
                time = st.time_input("Appointment Time")
                
                if st.button("Book Appointment") and doctors:
                    book_appointment(user[5], doctor_email, date, time)
                    st.success("Appointment Booked Successfully!")


                st.subheader("Your Appointments")
                appointments = get_appointments(user[5])
                for appt in appointments:
                    st.write(f"📅 {appt[3]} at {appt[4]} with Dr. {appt[2]} (Status: {appt[5]})")

                st.subheader("Your Prescriptions")
                prescriptions = get_prescriptions(user[5])
                for pres in prescriptions:
                    st.write(f"🩺 Dr. {pres[0]}: {pres[1]}")

            elif user[1] == "Doctor":
                st.subheader("Pending Appointments")
                appointments = get_doctor_appointments(user[5])

                for appt in appointments:
                    col1, col2 = st.columns(2)
                    col1.write(f"📅 {appt[3]} at {appt[4]} - Patient: {appt[1]} (Status: {appt[5]})")
                    if col2.button("Approve", key=f"approve_{appt[0]}"):
                        update_appointment_status(appt[0], "Approved")
                        st.success("Appointment Approved!")
                    if col2.button("Delete", key=f"delete_{appt[0]}"):
                        delete_appointment(appt[0])
                        st.error("Appointment Deleted!")

                st.subheader("Give Prescription")
                patient_email = st.text_input("Patient Email")
                prescription_text = st.text_area("Enter Prescription")

                if st.button("Send Prescription"):
                    add_prescription(patient_email, user[5], prescription_text)
                    st.success("Prescription Sent Successfully!")
        else:
            st.error("Invalid Email or Password")
