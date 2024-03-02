from entities.History_Search_Model import History_app, History_db, HistoryRecord
from entities.User_Model import User, User_db, User_app
from entities.Session_Model import Session, Session_db, Session_app
from flask import Flask
from app import app

with User_app.app_context():
    User_db.metadata.reflect(bind=User_db.engine)

    print("User Table Columns:")
    for table in User_db.metadata.tables.values():
        print(f"Table: {table.name}")
        for column in table.columns:
            print(f"\tColumn: {column.name} - {column.type}")
            # print value in the table
    for row in User.query.all():
        print(row)
        print(row.username)
        print(row.password)
        print(row.email)
        print(row.date_created)

with Session_app.app_context():
    Session_db.metadata.reflect(bind=Session_db.engine)

    print("\nSession Table Columns:")
    for table in Session_db.metadata.tables.values():
        print(f"Table: {table.name}")
        for column in table.columns:
            print(f"\tColumn: {column.name} - {column.type}")
            # print value in the table
    for row in Session.query.all():
        print(row)
        print(row.session_id)
        print(row.date_created)
        print(row.is_logged_in)

with History_app.app_context():
    History_db.metadata.reflect(bind=History_db.engine)

    print("\nSession Table Columns:")
    for table in History_db.metadata.tables.values():
        print(f"Table: {table.name}")
        for column in table.columns:
            print(f"\tColumn: {column.name} - {column.type}")
            # print value in the table
    for row in HistoryRecord.query.all():
        print(row)
        print(row.username)
        print(row.date_created)
        print(row.data)



