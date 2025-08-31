#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 23:15:07 2025

@author: luca
"""

import sqlite3

login = []

def sign_in():
    conn = sqlite3.connect("user_db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM user")
    
    result = cur.fetchall()
    
    if not result:
        print("\nThere are no signed up users.\n")
    
    else:
        email = input("E-mail: ")
        password = input("Password: ")
        
        # checking if the user exists in the database and if the credentials are correct
        for row in result:
            if row[2] == password and row[3] == email:
                username = row[1]
                user_id = row[0]
                login.append(username)
                login.append(email)
                login.append(user_id)
                break
        if not login:
            print("\nUser not found. Please try again.\n")

    conn.close()

def add_user():
    username = input("Username: ")
    email = input("E-mail: ")
    password = input("Password: ")
    
    conn = sqlite3.connect("user_db")
    cur = conn.cursor()
    
    cur.execute("SELECT user_id FROM user ORDER BY user_id")
    
    result = cur.fetchall()
    
    new_id = 1
    # creating a new id for the user, so that they don't all have the same id
    for i in result:
        if new_id == i[0]:
            new_id += 1
        else:
            break
    print(new_id)
    cur.execute(f"INSERT INTO user VALUES ({new_id}, '{username}', '{password}', '{email}')")
    conn.commit()
    
    conn.close()
    
    print(f"\nUser {username} has been added.\n")

def view_all_users():
    print("\nUsers:")
    
    conn = sqlite3.connect("user_db")
    cur = conn.cursor()
    
    for row in cur.execute("SELECT * FROM user ORDER BY user_id"):
        print(f"ID: {row[0]}, username: {row[1]}")
    
    conn.close()
    
    print("")
choice = 0

def delete_user():
    conn = sqlite3.connect("user_db")
    
    result = conn.execute("SELECT * FROM user ORDER BY user_id")
    
    print("\nUsers:")
    
    # display the users in the database
    for row in result:
        print(f"ID: {row[0]}, username: {row[1]}")
    
    conn.close()
    
    user_id = 0
    
    while user_id != -1: # -1 is used to cancel the operation.
        user_found = False
        
        conn = sqlite3.connect("user_db")
        cur = conn.cursor()
        
        result = conn.execute("SELECT * FROM user")
        
        user_id = int(input("\nInsert the ID of the user you'd like to remove. Insert -1 to cancel."))
        
        if user_id == -1:
            break
        
        # finding the user
        for row in result:
            x = 0
            
            if user_id == row[x]:
                user_found = True
                break
            x += 1
            
        if user_found:
            result = cur.execute(f"SELECT username FROM user WHERE user_id = {user_id}")
            
            name = cur.fetchall()
            
            cur.execute(f"DELETE FROM user WHERE user_id = {user_id}")
            conn.commit()
            
            print(f"\nUser {name[0][0]} has been removed.\n")
            
            user_id = -1
            break
            
        else:
            print("\nUser not found.\n")

        
        conn.close()

def view_profile():
    conn = sqlite3.connect("user_db")
    cur = conn.cursor()
    
    cur.execute(f"SELECT user_id, username, email FROM user WHERE user_id = {login[2]}")
    result = cur.fetchall()
    
    print("\nProfile:")
    print(f"ID: {result[0][0]}")
    print(f"Username: {result[0][1]}")
    print(f"E-mail: {result[0][2]}\n")
    
    conn.close()

while choice != 5:
    if not login: # if the user hasn't logged in
        choice = int(input("Select an option.\n1. Sign in\n2. Sign up\n3. Quit\n"))
        
        match(choice):
            case 1:
                sign_in()
            
            case 2:
                add_user()
                
            case 3:
                print("\nQuitting..")
        
    else:
        choice = int(input(f"Hello, {login[0]}.\nSelect an option.\n1. Add user\n2. View all users\n3. Delete user\n4. View profile\n5. Quit\n"))
        
        match(choice):
            case 1:
                add_user()
            
            case 2:
                view_all_users()
            
            case 3:
                delete_user()
            
            case 4:
                view_profile()
            
            case 5:
                print("\nQuitting...")
            
            case _:
                print("\nInvalid option.\n")