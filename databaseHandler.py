import sqlite3
import sys
from pprint import pprint

con = None
try:
    con = sqlite3.connect('sqlite.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

except sqlite3.Error as e:
    print(f"Error {e.args[0]}")
    sys.exit(1)

def convertToDict(result):
    for rowId in range(len(result)):
        result[rowId] = dict(result[rowId])
    return result

def getStock(id: int = None):
    query = "SELECT * FROM stock;"
    if id:
        query = f"SELECT * FROM stock WHERE id='{id}';"
    cur.execute(query)
    return convertToDict(cur.fetchall())

def updateStock(id: int, item: dict):
    if not (item.get("name") and item.get("quantity") and item.get("unit")): # checking if dictionary is invalid
        raise Exception("Invalid Item Dictionary in argument")
    query = f"UPDATE stock SET (name, quantity, unit) = ('{item['name']}', '{item['quantity']}', '{item['unit']}') WHERE id={id};"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

def addStock(item: dict):
    if not (item.get("name") and item.get("quantity") and item.get("unit")): # checking if dictionary is invalid
        raise Exception("Invalid Item Dictionary in argument")
    query = f"INSERT INTO stock (name, quantity, unit) VALUES ('{item['name']}', '{item['quantity']}', '{item['unit']}')"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

def deleteStock(id: int):
    query = f"DELETE FROM stock WHERE id='{id}';"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false


# pprint(updateStock(1, {"name":"Product A", "quantity": 100.0, "unit":"ft"}))
# pprint(addStock({"name":"Product C", "quantity": 1000, "unit":"kg"}))
# pprint(deleteStock(6))
# pprint(getStock(1))
# pprint(getStock())


def getParties(type: str = None, id: int = None):
    if not (type or id): # checking if either one argument is given
        raise Exception("Atleast one argument is required. type or id")
    if type and type != "Customer" and type != "Supplier": # checking if type is invalid
        raise Exception("Invalid party type provided in argument")
    
    if id and type:
        query = f"SELECT * FROM parties WHERE type='{type}' AND id='{id}';"
    elif type:
        query = f"SELECT * FROM parties WHERE type='{type}';"
    elif id:
        query = f"SELECT * FROM parties WHERE id='{id}';"
    cur.execute(query)
    return convertToDict(cur.fetchall())

def updateParties(id: int, item: dict):
    if not (item.get("name") and item.get("number") and item.get("email") and item.get("address")): # checking if dictionary is invalid
        raise Exception("Invalid Party Dictionary in argument")
    query = f"UPDATE parties SET (name, number, email, address) = ('{item['name']}', '{item['number']}', '{item['email']}', '{item['address']}') WHERE id={id};"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

def addParties(item: dict):
    if not (item.get("name") and item.get("number") and item.get("type") and item.get("email") and item.get("address")): # checking if dictionary is invalid
        raise Exception("Invalid Party Dictionary in argument")
    query = f"INSERT INTO parties (name, type, number, email, address) VALUES ('{item['name']}', '{item['type']}', '{item['number']}', '{item['email']}', '{item['address']}')"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

def deleteParties(id: int):
    query = f"DELETE FROM parties WHERE id='{id}';"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

# pprint(updateParties(1, {'address': 'Address A', 'email': 'partyedited@example.com', 'name': 'Party A', 'number': '1234567890'}))
# pprint(getParties(type="Customer"))
# pprint(addParties({'name':'Party C', 'type':'Customer', 'number':'000000000','email':'abd@gmail.coj','address':'wowowowo'}))
# pprint(getParties(id=1))


def getPayments(type: str = None, id: int = None):
    if not (type or id): # checking if either one argument is given
        raise Exception("Atleast one argument is required. type or id")
    if  type and type != "Receipt" and type != "Payment": # checking if type is invalid
        raise Exception("Invalid payment type provided in argument")

    if id and type:
        query = f"SELECT * FROM payments WHERE type='{type}' AND id='{id}';"
    elif type:
        query = f"SELECT * FROM payments WHERE type='{type}';"
    elif id:
        query = f"SELECT * FROM payments WHERE id='{id}';"
    cur.execute(query)

    result = convertToDict(cur.fetchall())
    for i in range(len(result)):
        # result[i] = list(result[i])
        result[i]["party"] = getParties(id=result[i]["party_id"])[0]
        del result[i]["party_id"]
    return result

def updatePayments(id: int, item: dict):
    if not (item.get("_date") and item.get("amount") and item.get("party_id")): # checking if dictionary is invalid
        raise Exception("Invalid Payment Dictionary in argument")
    query = f"UPDATE payments SET (_date, amount, party_id) = ('{item['_date']}','{item['amount']}','{item['party_id']}') WHERE id={id};"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

def addPayments(item: dict):
    if not (item.get("_date") and item.get("amount") and item.get("type") and item.get("party_id")): # checking if dictionary is invalid
        raise Exception("Invalid Payment Dictionary in argument")
    query = f"INSERT INTO payments (_date, party_id, type, amount) VALUES ('{item['_date']}', '{item['party_id']}', '{item['type']}', '{item['amount']}')"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

def deletePayments(id: int):
    query = f"DELETE FROM payments WHERE id='{id}';"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

# pprint(updatePayments(1, ({'_date' : '11/23/24', 'amount' : '1270'}))
# pprint(getPayments(type="Receipt"))
# pprint(addPayments({'_date' : '11/23/24','party_id':'3' ,'type':'Payment', 'amount' : '1900'}))
# pprint(getPayments(Payment=1))

def getTrades(type: str = None, id: int = None):
    if not (type or id): # checking if either one argument is given
        raise Exception("Atleast one argument is required. type or id")
    if  type and type != "Sale" and type != "Purchase": # checking if type is invalid
        raise Exception("Invalid trade type provided in argument")

    if id and type:
        query = f"SELECT * FROM trades WHERE type='{type}' AND id='{id}';"
    elif type:
        query = f"SELECT * FROM trades WHERE type='{type}';"
    elif id:
        query = f"SELECT * FROM trades WHERE id='{id}';"
    cur.execute(query)

    result = convertToDict(cur.fetchall())
    for i in range(len(result)):
        # result[i] = list(result[i])
        result[i]["party"] = getParties(id=result[i]["party_id"])[0]
        result[i]["item"] = getStock(id=result[i]["item_id"])[0]
        del result[i]["party_id"]
        del result[i]["item_id"]
    return result

def updateTrade(id: int, item: dict):
    if not (item.get("_date") and item.get("quantity") and item.get("rate") and item.get("item_id") and item.get("party_id")): # checking if dictionary is invalid
        raise Exception("Invalid trade Dictionary in argument")
    oldTrade = getTrades(id=id)[0]
    oldQuantity = oldTrade["quantity"]
    query = f"UPDATE trades SET (_date, quantity, rate, item_id, party_id) = ('{item['_date']}', '{item['quantity']}', '{item['rate']}', '{item['item_id']}', '{item['party_id']}') WHERE id={id};"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        con.commit() # saving changes
        tradeType = oldTrade["type"]
        updatedStock = getStock(item["item_id"])[0]
        if tradeType == "Sale":
            updatedStock["quantity"] -= (float(item["quantity"]) - oldQuantity)
        else:
            updatedStock["quantity"] += (float(item["quantity"]) - oldQuantity)
        updateStock(item["item_id"], updatedStock)
    return bool(cur.rowcount) # returning true or false

def addTrade(item: dict):
    if not (item.get("_date") and item.get("type") and item.get("party_id") and item.get("item_id") and item.get("quantity") and item.get("rate")): # checking if dictionary is invalid
        raise Exception("Invalid trade Dictionary in argument")
    query = f"INSERT INTO trades (_date, type, party_id, item_id, quantity, rate) VALUES ('{item['_date']}', '{item['type']}', '{item['party_id']}', '{item['item_id']}', '{item['quantity']}', '{item['rate']}')"
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        tradeType = item["type"]
        updatedStock = getStock(item["item_id"])[0]
        if tradeType == "Sale":
            updatedStock["quantity"] -= float(item["quantity"])
        else:
            updatedStock["quantity"] += float(item["quantity"])
        updateStock(item["item_id"], updatedStock)
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false

def deleteTrade(id: int):
    query = f"DELETE FROM trades WHERE id='{id}';"
    oldTrade = getTrades(id=id)[0]
    cur.execute(query)
    if cur.rowcount: #checking if query ran successfully
        tradeType = oldTrade["type"]
        updatedStock = getStock(oldTrade["item"]["id"])[0]
        if tradeType == "Sale":
            updatedStock["quantity"] += float(oldTrade["quantity"])
        else:
            updatedStock["quantity"] -= float(oldTrade["quantity"])
        updateStock(oldTrade["item"]["id"], updatedStock)
        con.commit() # saving changes
    return bool(cur.rowcount) # returning true or false


# pprint(getPayments(type="Payment"))
# print(getPayments(id=1))

# queries = [
#     "SELECT * FROM parties;",
#     "SELECT * FROM payments;",
#     "SELECT * FROM stock;",
#     "SELECT * FROM trades;",
# ]
# for query in queries:
#     cur.execute(query)
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)

# SELECT * FROM parties;
# SELECT * FROM payments;
# SELECT * FROM stock;
# SELECT * FROM trades;
