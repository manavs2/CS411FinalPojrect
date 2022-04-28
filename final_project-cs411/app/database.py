import re
from app import db

def insert_new_customer(netID: str, name:str, email:str, password:str) -> int:
    conn = db.connect()
    query = 'Insert Into Customers (NetID, Name, Email, Password) VALUES ("{}", "{}","{}", "{}");'.format(
        netID, name, email, password)
    conn.execute(query)
    conn.close()
    return 1


def remove_customer_by_netid(netid: str) -> None:
    conn = db.connect()
    query = 'Delete From Customers where NetID="{}";'.format(netid)
    conn.execute(query)
    conn.close()

def update_customer_email(email: str, netid: str) -> None:
    conn = db.connect()
    query = 'Update Customers Set Email="{}" where NetID="{}";'.format(email, netid)
    conn.execute(query)
    conn.close()

def update_customer_password(password: str, netid: str) -> None:
    conn = db.connect()
    query = 'Update Customers Set Password="{}" where NetID="{}";'.format(password, netid)
    conn.execute(query)
    conn.close()

def search_restuarant(cuisine: str) -> str:
    conn = db.connect()
    query = 'Select Name from Restaurants where Cuisine="{}";'.format(cuisine)
    query_results = conn.execute(query).fetchall()
    conn.close()

    return_str = ""
    for result in query_results:
        return_str += result[0] + "<br>"
    
    return return_str[0:len(return_str)-2]

def find_good_restaurants() -> str:
    conn = db.connect()
    query = 'SELECT r.Name, temp.AvgRating FROM (SELECT p.RestaurantID, AVG(rev.Rating) AS AvgRating FROM Reviews rev LEFT JOIN Purchases p ON (rev.PurchaseID = p.PurchaseID)  GROUP BY p.RestaurantID) AS temp LEFT JOIN Restaurants r ON (r.RestaurantID = temp.RestaurantID) WHERE temp.AvgRating >= 4;'
    query_results = conn.execute(query).fetchall()
    conn.close()
    return create_table(['Name', 'Good Average Rating'], query_results)

def find_popular_dish() -> str:
    conn = db.connect()
    query = 'CALL TagPopularDishes();'
    query_results = conn.execute(query).fetchall()
    conn.close()
    return create_table(['Restaurant Name', 'Address', 'Popular Dish'], query_results)

def search_restuarants_average() -> str:
    conn = db.connect()
    query = 'SELECT r.Name, AVG(d.Price) FROM Restaurants r JOIN Dishes d ON (r.RestaurantID = d.RestaurantID) GROUP BY r.RestaurantID;'
    query_results = conn.execute(query).fetchall()
    conn.close()
    
    print(query_results)
    
    return create_table(['Name', 'Average Price'], query_results)


def get_restaurant_id_HELPER(restaurant_name: str) -> str:
    conn = db.connect()
    query = 'SELECT restaurantID FROM Restaurants WHERE name = "{}" LIMIT 1;'.format(restaurant_name)
    query_results = conn.execute(query).fetchall()
    conn.close()

    print(query_results)

    if (len(query_results) > 0):
        return query_results[0][0]
    else:
        return None

def get_restaurant_id(restaurant_name: str) -> str:
    potential_id = get_restaurant_id_HELPER(restaurant_name)

    if (potential_id is not None):
        return "Restaurant ID for {} found: {}".format(restaurant_name, potential_id)
    else:
        return "No Restaurant ID found for {}".format(restaurant_name)

def get_purchase_id_HELPER(restaurantID, netid, dish_name) -> str:
    conn = db.connect()
    query = 'SELECT purchaseID FROM Purchase WHERE (restaurantID = "{}" AND netID = "{}") AND dishName = "{}"  LIMIT 1;'.format(
        restaurantID, netid, dish_name
    )
    query_results = conn.execute(query).fetchall()
    conn.close()

    print(query_results)

    if (len(query_results) > 0):
        return query_results[0][0]
    else:
        return None

def add_purchase_review(restaurant_name: str, netid: str, dish_name: str, cuisine: str, calories: str, price: str, rating: str, title: str, description: str) -> None:
    conn = db.connect()

    # check if restaurant exists
    restaurant_id = get_restaurant_id_HELPER(restaurant_name)
    if (restaurant_name is None):
        return "Invalid Restaurant Name {}".format(restaurant_name)

    # query = 'Insert Into Customers (NetID, Name, Email, Password) VALUES ("{}", "{}","{}", "{}");'.format(
    #     netID, name, email, password)

    # INSERT IGNORE will do nothing if the PK already exists (restaurant ID and dishname)
    insert_dish = 'INSERT IGNORE INTO Dishes (RestaurantID, Name, Cuisine, Calories, Price) VALUES ("{}", "{}","{}", "{}", "{}");'.format(
        restaurant_id, dish_name, cuisine, calories, price
    )
   
    conn.execute(insert_dish)
    



    # insert the purchase of the dish
    new_purchase_id = get_new_purchase_id_HELPER()
    insert_purchase = 'INSERT INTO Purchases (PurchaseID, DishName, RestaurantID, NetID) VALUES ("{}", "{}", "{}", "{}");'.format(
        new_purchase_id, dish_name, restaurant_id, netid
    )
    conn.execute(insert_purchase)

    # find the purchase id if exists (it SHOULD since it was just inserted)
    # purchase_id = get_purchase_id_HELPER(restaurant_id, netid, dish_name)
    # if (restaurant_name is None):
    #     return "Could not find correct Purchase ({}, {}, {})".format(restaurant_id, netid, dish_name)

    # insert review with correct purchaseID
    new_review_id = get_new_review_id_HELPER()
    insert_review = 'INSERT INTO Reviews (ReviewID, PurchaseID, NetID, Rating, Title, Description) VALUES ("{}", "{}", "{}","{}", "{}", "{}");'.format(
        new_review_id, new_purchase_id, netid, rating, title, description
    )
    conn.execute(insert_review)

    conn.close()

    return ''


def get_new_review_id_HELPER() -> int:
    conn = db.connect()
    query = 'SELECT MAX(ReviewID) FROM Reviews;'
    results = conn.execute(query).fetchall()
    conn.close()

    if (len(results) > 0):
        return int(results[0][0]) + 1
    else:
        return None

def get_new_purchase_id_HELPER() -> int:
    conn = db.connect()
    query = 'SELECT MAX(PurchaseID) FROM Purchases;'
    results = conn.execute(query).fetchall()
    conn.close()

    if (len(results) > 0):
        return int(results[0][0]) + 1
    else:
        return None

def get_credibility_helper(netid: str) -> str:
    conn = db.connect()

    query = 'SELECT Credibility FROM Customers WHERE NetID = "{}" LIMIT 1;'.format(netid)
    results = conn.execute(query).fetchall()

    conn.close()

    if (len(results) > 0):
        return results[0][0]
    else:
        return None

def get_credibility(netid: str) -> str:
    cred = get_credibility_helper(netid)

    if (cred is None):
        return "NetID {} has no credibility level".format(netid)
    else:
        return "Customer {} has credibility status {}!".format(netid,cred)

def create_table(columns, query_results):
    print(len(columns))
    print(len(query_results[0]))
    if (len(columns) != len(query_results[0])):
        return "Column name and query result mismatch"
    
    header_row = build_table_row(columns)
    print(header_row)
    rows = ""
    for result in query_results:
        rows += build_table_row(result)

    to_return = '<table class="table">{}</table>'.format(header_row + rows)
    print(to_return)
    return to_return

def build_table_row(result):
    print (result)
    vals = ""
    for val in result:
        vals += ('<td>{}</td>'.format(val))
        print(val, vals)

    out = "<tr>{}</tr>".format(vals)
    print(out)
    return out