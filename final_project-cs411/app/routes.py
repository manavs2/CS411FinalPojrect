import json
from tkinter import EXCEPTION
from app import app 
from flask import render_template, jsonify, request
from app import database as db_helper


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route('/add_customer', methods=['POST'])
def my_form_post():
    netID = request.form['netid']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    db_helper.insert_new_customer(netID, name, email, password)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route('/delete_netid', methods=['POST'])
def delete():
    netid = request.form['delete_netid1'] 
    try:
        db_helper.remove_customer_by_netid(netid)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    
    return jsonify(result)

@app.route('/edit_email', methods=['POST'])
def update():
    netid = request.form['update_netid']
    email = request.form['update_email']
    try:
        db_helper.update_customer_email(email, netid)
        result = {'success': True, 'response': 'Status Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    
    return jsonify(result)

@app.route('/edit_password', methods=['POST'])
def update_password():
    netid = request.form['pupdate_netid']
    password = request.form['update_password']
    try:
        db_helper.update_customer_password(password, netid)
        result = {'success': True, 'response': 'Status Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    
    return jsonify(result)

@app.route('/get_restaurants', methods=['GET'])
def search_cuisine():
    cuisine = request.args.get('cuisine')
    print(cuisine)
    try: 
       items =  db_helper.search_restuarant(cuisine)
       return items
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    
    return jsonify(result)

@app.route('/query1', methods=['GET'])
def queryone():
    try:
        items =  db_helper.search_restuarants_average()
        return render_template("table.html", table_content=items)

    except:
        result = {'success': False, 'response': 'Something went wrong'}
    
    return jsonify(result)

@app.route('/query2', methods=['GET'])
def querytwo():
    try:
        items =  db_helper.find_good_restaurants()
        return render_template("table.html", table_content=items)
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    
    return jsonify(result)

@app.route('/query3', methods=['GET'])
def querythree():
    try:
        items =  db_helper.find_popular_dish()
        return render_template("table.html", table_content=items)
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    
    return jsonify(result)


@app.route('/get_restaurantid', methods=['GET'])
def getRestaurantId():
    restaurant_name = request.args.get('get_restaurantname')
    try:
        items =  db_helper.get_restaurant_id(restaurant_name)
        return items
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)
        
@app.route('/add_purchase', methods=['POST'])
def addPurchase():
    restaurant_name = request.form['purchase_restaurantname']
    netid = request.form['purchase_netid']
    dish_name = request.form['purchase_dishname']
    cuisine = request.form['purchase_cuisine']
    calories = request.form['purchase_calories']
    price = request.form['purchase_price']
    rating = request.form['review_rating']
    title = request.form['review_title']
    description = request.form['review_description']
    
    try:
        items =  db_helper.add_purchase_review(restaurant_name, netid, dish_name, cuisine, calories, price, rating, title, description)
        result = {'success': True, 'response': 'Done'}
    except Exception as E:
        print (E)
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route('/get_credibility', methods=['GET'])
def getCredibility():
    netid = request.args.get('cred_netid')

    try:
        items = db_helper.get_credibility(netid)
        return items
    except Exception as E:
        print (E)
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)



        