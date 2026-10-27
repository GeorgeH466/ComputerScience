import tkinter
from tkinter import ttk
import mysql.connector

def db_connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hello",
        database="project"
    )