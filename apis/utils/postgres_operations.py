from core.settings import POSTGRES_USER, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_PASSWORD, POSTGRES_DBNAME
from core.postgres_connection import DatabaseManager, user_table, events_table, copouns, buy_copouns, items
from sqlalchemy import func,text, desc,cast, String, Date, and_, delete
import json

db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
db_manager = DatabaseManager(db_url)
db_manager.create_tables()
session = db_manager.get_session()

def find_user(roll_number, password):
    return session.query(user_table).filter(user_table.roll_no==roll_number).filter(user_table.password==password).first()

def get_user_by_roll_number(roll_number):
    print(roll_number)
    user = session.query(user_table).filter(user_table.roll_no==roll_number).first()
    if user:
        return {'name': user.name, 'email': user.email_id, 'contact_number': user.contact_no, 'roll_no': user.roll_no}
    else:
        return None

def add_event(roll_number,name, description,image,website_link,sub_events):
    session.add(events_table(roll_no=roll_number,name=name,description=description,image=image,website_link=website_link,sub_events=sub_events))
    session.commit()

def addSaleItem(roll_number, category, item_name, cost, images):
    session.add(items(roll_no=roll_number, category=category, item_name=item_name, cost=cost, images=images))
    session.commit()


def get_all_events():
    return session.query(events_table).all()

def get_events_by_event_name(event_name):
    return session.query(events_table).filter(events_table.name==event_name).first()

def add_coupon(roll_no,category):
    session.add(copouns(roll_no=roll_no,category=category))
    session.commit()

def add_buy_coupon(roll_no,category):
    session.add(buy_copouns(roll_no=roll_no,category=category))
    session.commit()

def getSellerEmailID(good_number):
    item_details = session.query(items).filter(items.unique_good_number==good_number).first()

    if item_details:
        # Get the roll number from item_details
        roll_number = item_details.roll_no

        # Query the user_table to get the seller's details
        seller_details = session.query(user_table).filter(user_table.roll_no==roll_number).first()

        if seller_details:
            # Return item name, seller's email id, and seller's name
            return item_details.item_name, seller_details.email_id, seller_details.name
        else:
            print(f"Seller not found for roll number: {roll_number}")
            return None
    else:
        print(f"Item not found for good number: {good_number}")
        return None
  
def delete_item_with_good_number(good_number):
    delete_stmt=delete(items).where(items.unique_good_number==good_number)
    session.execute(delete_stmt)
    session.commit()

def delete_coupon_with_rollno_and_category(roll_no, category):
    conditionV =  and_(copouns.roll_no == roll_no, copouns.category == category)
    delete_stmt=delete(copouns).where(conditionV)
    session.execute(delete_stmt)
    session.commit()

def delete_event_by_name_and_rollno(roll_no, name):
    conditionVy = and_(events_table.name == name)
    delete_stmt=delete(events_table).where(conditionVy)
    session.execute(delete_stmt)
    session.commit()

def filter_items_by_category(category):
    get_category_data_with_users=session.query(items, user_table).filter(items.category==category).join(items, user_table.roll_no == items.roll_no)
    item_details =get_category_data_with_users.all()
    return item_details

def coupons_data():
    return session.query(copouns).all()