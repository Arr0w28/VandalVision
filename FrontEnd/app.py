import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Set up the SQLite engine and create a connection
engine = create_engine('sqlite:///users.db')
meta = MetaData()

# Define the users table
users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True),
    Column('password', String)
)

# Create the table if not exists
meta.create_all(engine)

# Set up session for database interaction
Session = sessionmaker(bind=engine)
session = Session()

# Function to add a new user to the database
def add_user(username, password):
    try:
        insert = users.insert().values(username=username, password=password)
        session.execute(insert)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # Rollback in case of error
        return False

# Function to authenticate the user
def authenticate(username, password):
    query = users.select().where(users.c.username == username).where(users.c.password == password)
    result = session.execute(query).fetchone()
    return result is not None

# Login Page
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state['page'] = 'live'
        else:
            st.error("Invalid credentials")

    # Add a button to redirect to the registration page
    if st.button("Register"):
        st.session_state['page'] = 'register'

# Register Page
def register():
    st.title("Register Page")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    
    if st.button("Register"):
        if add_user(new_username, new_password):
            st.success("User registered successfully!")
            st.session_state['page'] = 'login'
        else:
            st.error("Username already exists. Please choose another.")

    # Add a button to redirect to the login page
    if st.button("Back to Login"):
        st.session_state['page'] = 'login'

# Pages for after login
def live():
    st.title("Live Page")
    st.write("This is the live feed page.")
    if st.button("Go to Realtime"):
        st.session_state['page'] = 'realtime'

def realtime():
    st.title("Realtime Page")
    st.write("This is the real-time processing page.")
    if st.button("Go to Detect"):
        st.session_state['page'] = 'detect'

def detect():
    st.title("Detect Page")
    st.write("Detection in progress...")
    st.write("If vandalism is detected, a prompt will appear here.")
    if st.button("Go to Live Feed"):
        st.session_state['page'] = 'live'

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# Page routing
if st.session_state['page'] == 'login':
    login()
elif st.session_state['page'] == 'register':
    register()
elif st.session_state['page'] == 'live':
    live()
elif st.session_state['page'] == 'realtime':
    realtime()
elif st.session_state['page'] == 'detect':
    detect()
