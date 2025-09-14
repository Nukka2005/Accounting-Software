from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QFont, QKeySequence
import sys
from pprint import pprint
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QWidget,
    QAction,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QGridLayout,
    QMessageBox,
    QAbstractItemView,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
)
import databaseHandler

MAIN_WINDOW_WIDTH_RATIO = 0.8
MAIN_WINDOW_HEIGHT_RATIO = MAIN_WINDOW_WIDTH_RATIO
WINDOW_WIDTH_RATIO = 0.8
WINDOW_HEIGHT_RATIO = WINDOW_WIDTH_RATIO
ICON_FILE = "Images/icon.ico"
FONT = "Arial"
COLOR_PRIMARY = "#0e131f"
COLOR_SECONDARY = "#f5f7ff"
COLOR_SECONDARY_DARK = "#dce3ff"
COLOR_SELECTION = "transparent"
# COLOR_SELECTION = "#a6c5f7"
FONT_SIZE_HEADING = 30

class windowLedger(QWidget):
    def __init__(self, app, type):
        super().__init__()
        self.setWindowTitle(f"EU ACCOUNTS LEDGERS")
        self.setWindowIcon(QIcon(ICON_FILE))
        self.setStyleSheet(f"background: {COLOR_PRIMARY}")
        calculatedSize = getWindowSize(app, WINDOW_WIDTH_RATIO, WINDOW_HEIGHT_RATIO)
        self.setGeometry(calculatedSize)
        self.setMinimumSize(calculatedSize.width(), calculatedSize.height())
        
        self.heading = createHeading(self, self, "LEDGER")
        self.heading.setFixedHeight(FONT_SIZE_HEADING * 3)

        dropdown = QComboBox(self)
        partyList = databaseHandler.getParties(type="Customer") + databaseHandler.getParties(type="Supplier")
        dropdown.addItems(map(lambda party: str(party["id"]) + " : " + party["name"] + " : " + party["type"], partyList))
        dropdown.setFont(QFont(FONT, 15))
        dropdown.setStyleSheet(f'''
                            background: {COLOR_SECONDARY};
                            ''')
        self.ledgerLayout = QGridLayout(self)
        self.ledgerLayout.addWidget(self.heading, 0, 0, 1, 5)
        self.ledgerLayout.addWidget(dropdown, 1, 2, 1, 1)
        self.ledgerLayout.setAlignment(Qt.AlignCenter)
        dropdown.currentIndexChanged.connect(lambda: self.createLedger(partyList[dropdown.currentIndex()]))
    
    def createLedger(window, party):
        type = party["type"]
        if type == "Customer":
            tradeCol = "Credit"
            paymentCol = "Debit"
            tradeType = "Sale"
            paymentType = "Receipt"
        elif type == "Supplier":
            tradeCol = "Debit"
            paymentCol = "Credit"
            tradeType = "Purchase"
            paymentType = "Payment"
        all = databaseHandler.getPayments(type=paymentType) + databaseHandler.getTrades(type=tradeType)
        data = []
        for transaction in all:
            if party["id"] == transaction["party"]["id"]:
                data.append(transaction)
        data = sorted(data, key = lambda row: str(row["_date"]))
        balance = 0
        for row in data:
            if row.get("item"): # if row is of trade
                if type == "Customer":
                    row["debit"]  = "-"
                    row["credit"] = row["rate"] * row["quantity"]
                    balance -= row["credit"]
                elif type == "Supplier":
                    row["debit"] = row["rate"] * row["quantity"]
                    row["credit"]  = "-"
                    balance += row["debit"]
                del row["item"]
                del row["quantity"]
                del row["rate"]
            else:
                if type == "Customer":
                    row["debit"] = row["amount"]
                    row["credit"]  = "-"
                    balance += row["debit"]
                elif type == "Supplier":
                    row["debit"]  = "-"
                    row["credit"] = row["amount"]
                    balance -= row["credit"]
                del row["amount"]
            del row["party"]
            del row["type"]
            # del row["id"]
            row["Balance"] = balance
            
        window.table = QTableWidget(window)
        if data:
            setupTable(window.table, data)
        else:
            displayError("No Transactions of Party", f"No record found of {party["name"]} in database.\nSelect another party or add new transactions.")
        window.ledgerLayout.addWidget(window.table, 2, 0, 1, 5)

class windowTrade(QWidget):
    def __init__(self, app, type):
        super().__init__()
        self.setWindowTitle(f"EU ACCOUNTS - {type.upper()}")
        self.setWindowIcon(QIcon(ICON_FILE))
        self.setStyleSheet(f"background: {COLOR_PRIMARY}")
        calculatedSize = getWindowSize(app, WINDOW_WIDTH_RATIO, WINDOW_HEIGHT_RATIO)
        self.setGeometry(calculatedSize)
        self.setMinimumSize(calculatedSize.width(), calculatedSize.height())
        self.Trade = removeType(databaseHandler.getTrades(type=type))
        self.TradeTable = QTableWidget(self)
        setupTable(self.TradeTable, self.Trade)
        
        self.heading = createHeading(self, self, f"CURRENT {type.upper()}")
        self.heading.setFixedHeight(FONT_SIZE_HEADING * 3)

        self.btnAdd = QPushButton("Add")
        self.btnEdit = QPushButton("Edit")
        self.btnDelete = QPushButton("Delete")
        styleButton(self.btnAdd)
        styleButton(self.btnEdit)
        styleButton(self.btnDelete)
        inputDetails = [
            {"_date": QLineEdit(self.parent()), "party_id": QLineEdit(self.parent()), "item_id": QLineEdit(self.parent()), "quantity": QLineEdit(self.parent()), "rate": QLineEdit(self.parent())},
            {"id": QLineEdit(self.parent()), "party_id": QLineEdit(self.parent()), "item_id": QLineEdit(self.parent()), "_date": QLineEdit(self.parent()), "quantity": QLineEdit(self.parent()), "rate": QLineEdit(self.parent())},
            {"id": QLineEdit(self.parent())},
        ]
        # Create the main layout
        self.TradeLayout = QGridLayout(self)
        self.btnAdd.clicked.connect(lambda: setEvents(self, self.btnAdd, inputDetails[0],  self.TradeLayout, type))
        self.btnEdit.clicked.connect(lambda: setEvents(self, self.btnEdit, inputDetails[1],  self.TradeLayout, type, self.Trade))
        self.btnDelete.clicked.connect(lambda: setEvents(self, self.btnDelete, inputDetails[2],  self.TradeLayout, type))
        self.TradeLayout.addWidget(self.heading, 0, 0, 1, 5)
        self.TradeLayout.addWidget(self.TradeTable, 1, 0, 1, 5)
        self.TradeLayout.addWidget(self.btnAdd, 2, 1)
        self.TradeLayout.addWidget(self.btnEdit, 2, 2)
        self.TradeLayout.addWidget(self.btnDelete, 2, 3)
        self.TradeLayout.setAlignment(Qt.AlignCenter)
            
    def submitAdd(self, inputs, type):
        if type == "Purchase":
            partyType = "Supplier"
        elif type == "Sale":
            partyType = "Customer"
        errors = []
        _date = inputs["_date"].text()
        party_id = inputs["party_id"].text()
        item_id = inputs["item_id"].text()
        quantity = inputs["quantity"].text()
        rate = inputs["rate"].text()
        errors.extend(checkError_Text(_date, "Date"))
        errors.extend(checkError_Id(party_id, "Party ID", databaseHandler.getParties(type=partyType)))
        errors.extend(checkError_Id(item_id, "Item ID", databaseHandler.getStock()))
        errors.extend(checkError_Float(quantity, "Quantity"))
        errors.extend(checkError_Float(rate, "Rate"))
        amount = float(quantity) * float(rate)
        if errors == []:
            party = getDictById(party_id, databaseHandler.getParties(type=partyType))
            item = getDictById(item_id, databaseHandler.getStock())
            if getConfirmation("Confirmation:", f"Do you want to add:\n{item["name"]}, {quantity} {item["unit"]} at {rate} in account of {party["name"]} at {_date}, Total: {amount}"):
                databaseHandler.addTrade({
                    "_date" : _date,
                    "party_id" : party_id,
                    "item_id" : item_id,
                    "quantity" : quantity,
                    "rate" : rate,
                    "type" : type,
                })
                self.Trade = removeType(databaseHandler.getTrades(type=type))
                setupTable(self.TradeTable, self.Trade)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

    def submitEdit(self, inputs, type):
        if type == "Purchase":
            partyType = "Supplier"
        elif type == "Sale":
            partyType = "Customer"
        errors = []
        if self.Trade != removeType(databaseHandler.getTrades(type=type)):
            displayError("Data Sync Error!", f"{type} Table data has changed by another process.\n Table has been updated.\nPlease review your changes first.")
            return
        _id = inputs["id"].text()
        _date = inputs["_date"].text()
        party_id = inputs["party_id"].text()
        item_id = inputs["item_id"].text()
        quantity = inputs["quantity"].text()
        rate = inputs["rate"].text()
        pprint(_id)
        pprint(self.Trade)
        errors.extend(checkError_Id(_id, "Trade ID", self.Trade))
        errors.extend(checkError_Id(party_id, "Party ID", databaseHandler.getParties(type=partyType)))
        errors.extend(checkError_Id(item_id, "Item ID", databaseHandler.getStock()))
        errors.extend(checkError_Text(_date, "Date"))
        errors.extend(checkError_Text(quantity, "Quantity"))
        errors.extend(checkError_Text(rate, "Rate"))
        if errors == []:
            editedItem = getDictById(_id, self.Trade)
            editedItem["amount"] = float(editedItem["quantity"]) * float(editedItem["rate"])
            amount = float(quantity) * float(rate)
            party = getDictById(party_id, databaseHandler.getParties(type=partyType))
            item = getDictById(item_id, databaseHandler.getStock())
            if getConfirmation("Confirmation:", f'''Do you want to edit:\n{item["name"]}, {editedItem["quantity"]} {item["unit"]} at {editedItem["rate"]} in account of {party["name"]} at {editedItem["_date"]}, Total: {editedItem["amount"]}\nto\n({item["name"]}, {quantity} {item["unit"]} at {rate} in account of {party["name"]} at {_date}, Total: {amount}'''):
                databaseHandler.updateTrade(_id, {
                    "_date" : _date,
                    "party_id" : party_id,
                    "item_id" : item_id,
                    "quantity" : quantity,
                    "rate" : rate,
                })
                self.Trade = removeType(databaseHandler.getTrades(type=type))
                setupTable(self.TradeTable, self.Trade)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

    def submitDelete(self, inputs, type):
        if type == "Purchase":
            partyType = "Supplier"
        elif type == "Sale":
            partyType = "Customer"
        errors = []
        if self.Trade != removeType(databaseHandler.getTrades(type=type)):
            displayError("Data Sync Error!", f"{type} Table data has changed by another process.\n Table has been updated.\nPlease review your changes first.")
            return
        _id = inputs["id"].text()
        errors.extend(checkError_Id(_id, "Trade ID", self.Trade))
        if errors == []:
            editedItem = getDictById(_id, self.Trade)
            editedItem["amount"] = float(editedItem["quantity"]) * float(editedItem["rate"])
            party = databaseHandler.getParties(id = editedItem["party"]["id"])[0]
            item = databaseHandler.getStock(id = editedItem["item"]["id"])[0]
            if getConfirmation("Confirmation:", f'''Do you want to delete:\n({item["name"]}, {editedItem["quantity"]} {item["unit"]} at {editedItem["rate"]} in account of {party["name"]} at {editedItem["_date"]}, Total: {editedItem["amount"]}'''):
                databaseHandler.deleteTrade(_id)
                self.Trade = removeType(databaseHandler.getTrades(type=type))
                setupTable(self.TradeTable, self.Trade)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

            
class windowPayment(QWidget):
    def __init__(self, app, type):
        super().__init__()
        self.setWindowTitle(f"EU ACCOUNTS - {type.upper()}")
        self.setWindowIcon(QIcon(ICON_FILE))
        self.setStyleSheet(f"background: {COLOR_PRIMARY}")
        calculatedSize = getWindowSize(app, WINDOW_WIDTH_RATIO, WINDOW_HEIGHT_RATIO)
        self.setGeometry(calculatedSize)
        self.setMinimumSize(calculatedSize.width(), calculatedSize.height())
        self.Payment = removeType(databaseHandler.getPayments(type=type))
        self.PaymentTable = QTableWidget(self)
        setupTable(self.PaymentTable, self.Payment)
        
        self.heading = createHeading(self, self, f"CURRENT {type.upper()}")
        self.heading.setFixedHeight(FONT_SIZE_HEADING * 3)

        self.btnAdd = QPushButton("Add")
        self.btnEdit = QPushButton("Edit")
        self.btnDelete = QPushButton("Delete")
        styleButton(self.btnAdd)
        styleButton(self.btnEdit)
        styleButton(self.btnDelete)
        inputDetails = [
            {"_date": QLineEdit(self.parent()), "party_id": QLineEdit(self.parent()), "amount": QLineEdit(self.parent())},
            {"id": QLineEdit(self.parent()), "_date": QLineEdit(self.parent()), "party_id": QLineEdit(self.parent()), "amount": QLineEdit(self.parent())},
            {"id": QLineEdit(self.parent())},
        ]
        # Create the main layout
        self.PaymentLayout = QGridLayout(self)
        self.btnAdd.clicked.connect(lambda: setEvents(self, self.btnAdd, inputDetails[0],  self.PaymentLayout, type))
        self.btnEdit.clicked.connect(lambda: setEvents(self, self.btnEdit, inputDetails[1],  self.PaymentLayout, type, self.Payment))
        self.btnDelete.clicked.connect(lambda: setEvents(self, self.btnDelete, inputDetails[2],  self.PaymentLayout, type))
        self.PaymentLayout.addWidget(self.heading, 0, 0, 1, 5)
        self.PaymentLayout.addWidget(self.PaymentTable, 1, 0, 1, 5)
        self.PaymentLayout.addWidget(self.btnAdd, 2, 1)
        self.PaymentLayout.addWidget(self.btnEdit, 2, 2)
        self.PaymentLayout.addWidget(self.btnDelete, 2, 3)
        self.PaymentLayout.setAlignment(Qt.AlignCenter)
        
    def submitAdd(self, inputs, type):
        if type == "Payment":
            partyType = "Supplier"
        elif type == "Receipt":
            partyType = "Customer"
        errors = []
        _date = inputs["_date"].text()
        party_id = inputs["party_id"].text()
        amount = inputs["amount"].text()
        errors.extend(checkError_Text(_date, "Date"))
        errors.extend(checkError_Id(party_id, "Party ID", databaseHandler.getParties(type=partyType)))
        errors.extend(checkError_Text(amount, "Amount"))
        if errors == []:
            party = getDictById(party_id, databaseHandler.getParties(type=partyType))
            if getConfirmation("Confirmation:", f"Do you want to add:\n{amount} in account of {party["name"]} at {_date}"):
                databaseHandler.addPayments({
                    "_date" : _date,
                    "party_id" : party_id,
                    "amount" : amount,
                    "type" : type,
                })
                self.Payment = removeType(databaseHandler.getPayments(type=type))
                setupTable(self.PaymentTable, self.Payment)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

    def submitEdit(self, inputs, type):
        if type == "Payment":
            partyType = "Supplier"
        elif type == "Receipt":
            partyType = "Customer"
        errors = []
        if self.Payment != removeType(databaseHandler.getPayments(type=type)):
            displayError("Data Sync Error!", f"{type} Table data has changed by another process.\n Table has been updated.\nPlease review your changes first.")
            return
        _id = inputs["id"].text()
        _date = inputs["_date"].text()
        party_id = inputs["party_id"].text()
        amount = inputs["amount"].text()
        errors.extend(checkError_Id(_id, "Payment ID", self.Payment))
        errors.extend(checkError_Id(party_id, "Party ID", databaseHandler.getParties(type=partyType)))
        errors.extend(checkError_Text(_date, "Date"))
        errors.extend(checkError_Text(amount, "Amount"))
        if errors == []:
            editedItem = getDictById(_id, self.Payment)
            party = getDictById(party_id, databaseHandler.getParties(type=partyType))
            if getConfirmation("Confirmation:", f'''Do you want to edit:\n({editedItem["id"]}) {editedItem["party"]["name"]} : {editedItem["_date"]} : {editedItem["amount"]}\nto\n({_id}) {party["name"]} : {_date} : {amount}'''):
                databaseHandler.updatePayments(_id, {
                    "_date" : _date,
                    "party_id" : party_id,
                    "amount" : amount,
                })
                self.Payment = removeType(databaseHandler.getPayments(type=type))
                setupTable(self.PaymentTable, self.Payment)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

    def submitDelete(self, inputs, type):
        errors = []
        if self.Payment != removeType(databaseHandler.getPayments(type=type)):
            displayError("Data Sync Error!", f"{type} Table data has changed by another process.\n Table has been updated.\nPlease review your changes first.")
            return
        _id = inputs["id"].text()
        errors.extend(checkError_Id(_id, "Payment ID", self.Payment))
        if errors == []:
            editedItem = getDictById(_id, self.Payment)
            if getConfirmation("Confirmation:", f'''Do you want to delete:\n({editedItem["id"]}) {editedItem["party"]["name"]} : {editedItem["_date"]}'''):
                databaseHandler.deleteParties(_id)
                self.Payment = removeType(databaseHandler.getPayments(type=type))
                setupTable(self.PaymentTable, self.Payment)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

class windowParty(QWidget):
    def __init__(self, app, type):
        super().__init__()
        self.setWindowTitle(f"EU ACCOUNTS - {type.upper()}")
        self.setWindowIcon(QIcon(ICON_FILE))
        self.setStyleSheet(f"background: {COLOR_PRIMARY}")
        calculatedSize = getWindowSize(app, WINDOW_WIDTH_RATIO, WINDOW_HEIGHT_RATIO)
        self.setGeometry(calculatedSize)
        self.setMinimumSize(calculatedSize.width(), calculatedSize.height())
        self.partyTable = QTableWidget(self)
        self.parties = removeType(databaseHandler.getParties(type=type))
        setupTable(self.partyTable, self.parties)
        
        self.heading = createHeading(self, self, type.upper())
        self.heading.setFixedHeight(FONT_SIZE_HEADING * 3)

        self.btnAdd = QPushButton("Add")
        self.btnEdit = QPushButton("Edit")
        self.btnDelete = QPushButton("Delete")
        styleButton(self.btnAdd)
        styleButton(self.btnEdit)
        styleButton(self.btnDelete)
        inputDetails = [
            {"name": QLineEdit(self.parent()), "number": QLineEdit(self.parent()), "email": QLineEdit(self.parent()), "address": QLineEdit(self.parent())},
            {"id": QLineEdit(self.parent()), "name": QLineEdit(self.parent()), "number": QLineEdit(self.parent()), "email": QLineEdit(self.parent()), "address": QLineEdit(self.parent())},
            {"id": QLineEdit(self.parent())},
        ]
        # Create the main layout
        self.partyLayout = QGridLayout(self)
        self.btnAdd.clicked.connect(lambda: setEvents(self, self.btnAdd, inputDetails[0], self.partyLayout, type))
        self.btnEdit.clicked.connect(lambda: setEvents(self, self.btnEdit, inputDetails[1], self.partyLayout, type, self.parties))
        self.btnDelete.clicked.connect(lambda: setEvents(self, self.btnDelete, inputDetails[2], self.partyLayout, type))
        self.partyLayout.addWidget(self.heading, 0, 0, 1, 5)
        self.partyLayout.addWidget(self.partyTable, 1, 0, 1, 5)
        self.partyLayout.addWidget(self.btnAdd, 2, 1)
        self.partyLayout.addWidget(self.btnEdit, 2, 2)
        self.partyLayout.addWidget(self.btnDelete, 2, 3)
        self.partyLayout.setAlignment(Qt.AlignCenter)

    def submitAdd(self, inputs, type):
        errors = []
        name = inputs["name"].text()
        number = inputs["number"].text()
        email = inputs["email"].text()
        address = inputs["address"].text()
        errors.extend(checkError_Text(name, "Name"))
        errors.extend(checkError_Text(number, "Number"))
        errors.extend(checkError_Text(email, "Email"))
        errors.extend(checkError_Text(address, "Address"))
        if errors == []:
            if getConfirmation("Confirmation:", f"Do you want to add:\n{name} : {number} : {email} : {address}"):
                databaseHandler.addParties({
                    "name" : name,
                    "number" : number,
                    "email" : email,
                    "address" : address,
                    "type" : type,
                })
                self.parties = removeType(databaseHandler.getParties(type=type))
                setupTable(self.partyTable, self.parties)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

    def submitEdit(self, inputs, type):
        errors = []
        if self.parties != removeType(databaseHandler.getParties(type=type)):
            displayError("Data Sync Error!", f"{type} Table data has changed by another process.\n Table has been updated.\nPlease review your changes first.")
            return
        _id = inputs["id"].text()
        name = inputs["name"].text()
        number = inputs["number"].text()
        email = inputs["email"].text()
        address = inputs["address"].text()
        errors.extend(checkError_Id(_id, "Party ID", self.parties))
        errors.extend(checkError_Text(name, "Name"))
        errors.extend(checkError_Text(number, "Number"))
        errors.extend(checkError_Text(email, "Email"))
        errors.extend(checkError_Text(address, "Address"))

        if errors == []:
            editedItem = getDictById(_id, self.parties)
            if getConfirmation("Confirmation:", f'''Do you want to edit:\n({editedItem["id"]}) {editedItem["name"]} : {editedItem["number"]} : {editedItem["email"]} : {editedItem["address"]}\nto\n({_id}) {name} : {number} : {email} : {address}'''):
                result = databaseHandler.updateParties(_id, {
                    "name" : name,
                    "number" : number,
                    "email" : email,
                    "address" : address,
                    "type" : type,
                })
                self.parties = removeType(databaseHandler.getParties(type=type))
                setupTable(self.partyTable, self.parties)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

    def submitDelete(self, inputs, type):
        errors = []
        if self.parties != removeType(databaseHandler.getParties(type=type)):
            displayError("Data Sync Error!", f"{type} Table data has changed by another process.\n Table has been updated.\nPlease review your changes first.")
            return
        _id = inputs["id"].text()
        
        errors.extend(checkError_Id(_id, "Party ID", self.parties))

        if errors == []:
            editedItem = getDictById(_id, self.parties)
            if getConfirmation("Confirmation:", f'''Do you want to delete:\n({editedItem["id"]}) {editedItem["name"]} : {editedItem["number"]} : {editedItem["email"]} : {editedItem["address"]}'''):
                result = databaseHandler.deleteParties(_id)
                self.parties = removeType(databaseHandler.getParties(type=type))
                setupTable(self.partyTable, self.parties)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

class windowStock(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("EU ACCOUNTS - STOCK")
        self.setWindowIcon(QIcon(ICON_FILE))
        self.setStyleSheet(f"background: {COLOR_PRIMARY}")
        calculatedSize = getWindowSize(app, WINDOW_WIDTH_RATIO, WINDOW_HEIGHT_RATIO)
        self.setGeometry(calculatedSize)
        self.setMinimumSize(calculatedSize.width(), calculatedSize.height())
        self.stockTable = QTableWidget(self)
        self.stock = databaseHandler.getStock()
        setupTable(self.stockTable, self.stock)
        
        self.heading = createHeading(self, self, "CURRENT STOCK")
        self.heading.setFixedHeight(FONT_SIZE_HEADING * 3)

        self.btnAdd = QPushButton("Add")
        self.btnEdit = QPushButton("Edit")
        self.btnDelete = QPushButton("Delete")
        styleButton(self.btnAdd)
        styleButton(self.btnEdit)
        styleButton(self.btnDelete)
        inputDetails = [
            {"name": QLineEdit(self.parent()), "quantity": QLineEdit(self.parent()), "unit": QLineEdit(self.parent())},
            {"id": QLineEdit(self.parent()), "name": QLineEdit(self.parent()), "quantity": QLineEdit(self.parent()), "unit": QLineEdit(self.parent())},
            {"id": QLineEdit(self.parent())},
        ]
        # Create the main layout
        self.stockLayout = QGridLayout(self)
        self.btnAdd.clicked.connect(lambda: setEvents(self, self.btnAdd, inputDetails[0],  self.stockLayout))
        self.btnEdit.clicked.connect(lambda: setEvents(self, self.btnEdit, inputDetails[1],  self.stockLayout, None, self.stock))
        self.btnDelete.clicked.connect(lambda: setEvents(self, self.btnDelete, inputDetails[2],  self.stockLayout))
        self.stockLayout.addWidget(self.heading, 0, 0, 1, 5)
        self.stockLayout.addWidget(self.stockTable, 1, 0, 1, 5)
        self.stockLayout.addWidget(self.btnAdd, 2, 1)
        self.stockLayout.addWidget(self.btnEdit, 2, 2)
        self.stockLayout.addWidget(self.btnDelete, 2, 3)
        self.stockLayout.setAlignment(Qt.AlignCenter)

    def submitAdd(self, inputs):
        errors = []
        name = inputs["name"].text()
        quantity = inputs["quantity"].text()
        unit = inputs["unit"].text()
        errors.extend(checkError_Text(name, "Name"))
        errors.extend(checkError_Float(quantity, "Quantity"))
        errors.extend(checkError_Text(unit, "Unit"))
        if errors == []:
            if getConfirmation("Confirmation:", f"Do you want to add:\n{name}: {quantity} {unit}"):
                databaseHandler.addStock({
                    "name": name,
                    "quantity": quantity,
                    "unit": unit,
                })
                self.stock = databaseHandler.getStock()
                setupTable(self.stockTable, self.stock)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))
            
    def submitEdit(self, inputs):
        errors = []
        if self.stock != databaseHandler.getStock():
            displayError("Data Sync Error!", "Stock Table data has changed by another process.\n Table has been updated.\nPlease review your changes first.")
            return
        _id = inputs["id"].text()
        name = inputs["name"].text()
        quantity = inputs["quantity"].text()
        unit = inputs["unit"].text()
        
        errors.extend(checkError_Id(_id, "Stock ID", self.stock))
        errors.extend(checkError_Text(name, "Name"))
        errors.extend(checkError_Float(quantity, "Quantity"))
        errors.extend(checkError_Text(unit, "Unit"))

        if errors == []:
            editedItem = getDictById(_id, self.stock)
            if getConfirmation("Confirmation:", f'''Do you want to edit:\n({editedItem["id"]}) {editedItem["name"]}: {editedItem["quantity"]} {editedItem["unit"]}\nto\n({_id}) {name}: {quantity} {unit}'''):
                result = databaseHandler.updateStock(_id, {
                    "name": name,
                    "quantity": quantity,
                    "unit": unit,
                })
                self.stock = databaseHandler.getStock()
                setupTable(self.stockTable, self.stock)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

    def submitDelete(self, inputs):
        errors = []
        if self.stock != databaseHandler.getStock():
            displayError("Data Sync Error!", "Stock Table data has changed by another process.\n Table has been updated.\nPlease review your changes first.")
            return
        _id = inputs["id"].text()
        
        errors.extend(checkError_Id(_id, "Stock ID", self.stock))

        if errors == []:
            editedItem = getDictById(_id, self.stock)
            if getConfirmation("Confirmation:", f'''Do you want to delete:\n({editedItem["id"]}) {editedItem["name"]}: {editedItem["quantity"]} {editedItem["unit"]}'''):
                result = databaseHandler.deleteStock(_id)
                self.stock = databaseHandler.getStock()
                setupTable(self.stockTable, self.stock)
                clearInputs(inputs)
                resetInputs(self, list(inputs.values()))
        else:
            displayError("Error Occured!", formatErrorInStr(errors))

class MainWindow(QMainWindow):
    app = None
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("EU ACCOUNTS")
        self.setWindowIcon(QIcon(ICON_FILE))
        calculatedSize = getWindowSize(app, MAIN_WINDOW_WIDTH_RATIO, MAIN_WINDOW_HEIGHT_RATIO)
        self.setGeometry(calculatedSize)
        self.setMinimumSize(calculatedSize.width(), calculatedSize.height())

        container = QWidget(self)
        self.setCentralWidget(container)
        container.setStyleSheet(f"background: {COLOR_PRIMARY}")
        containerLayout = QGridLayout(container)
        containerLayout.setAlignment(Qt.AlignCenter)
        containerLayout.setSpacing(30)
        self.heading = createHeading(self, container, "EU ACCOUNTING SOFTWARE")
        self.buttons = {
            "saleButton" : QPushButton("Sales"),
            "purchaseButton" : QPushButton("Purchases"),
            "receiptButton" : QPushButton("Receipt"),
            "paymentButton" : QPushButton("Payments"),
            "stockButton" : QPushButton("Stock"),
            "ledgerButton" : QPushButton("Ledgers"),
            "customerButton" : QPushButton("Customers"),
            "supplierButton" : QPushButton("Suppliers"),
        }
        self.buttons["ledgerButton"].clicked.connect(self.showWindowLedger)
        
        self.buttons["stockButton"].clicked.connect(self.showWindowStock)
        self.buttons["customerButton"].clicked.connect(lambda event: self.showWindowParty(event, "Customer"))
        self.buttons["supplierButton"].clicked.connect(lambda event: self.showWindowParty(event, "Supplier"))
        
        self.buttons["paymentButton"].clicked.connect(lambda event: self.showWindowPayment(event, "Payment"))
        self.buttons["receiptButton"].clicked.connect(lambda event: self.showWindowPayment(event, "Receipt"))

        self.buttons["saleButton"].clicked.connect(lambda event: self.showWindowTrade(event, "Sale"))
        self.buttons["purchaseButton"].clicked.connect(lambda event: self.showWindowTrade(event, "Purchase"))

        colCount = 2
        rowLimit = (len(self.buttons) - 1)//colCount
        row = 0
        col = 0
        # containerLayout.addWidget(self.heading, 0, 0, 1, colCount)
        for button in self.buttons.values():
            containerLayout.addWidget(button, row, col)
            if row == rowLimit:
                row = 0
                col += 1
            else:
                row += 1
            styleButton(button)

    def closeEvent(self, event):
        QApplication.closeAllWindows()

    def showWindowLedger(self, event):
        if hasattr(self, "windowLedger"):
            if not self.windowLedger.isVisible():
                self.windowLedger.destroy()
                self.windowLedger = windowLedger(self.app)
                self.windowLedger.show()
        else:
            self.windowLedger = windowLedger(self.app, type)
            self.windowLedger.show()
        
    def showWindowPayment(self, event, type: str):
        if hasattr(self, "windowPayment"):
            if not self.windowPayment.isVisible():
                self.windowPayment.destroy()
                self.windowPayment = windowPayment(self.app, type)
                self.windowPayment.show()
        else:
            self.windowPayment = windowPayment(self.app, type)
            self.windowPayment.show()
    
    def showWindowTrade(self, event, type: str):
        if hasattr(self, "windowTrade"):
            if not self.windowTrade.isVisible():
                self.windowTrade.destroy()
                self.windowTrade = windowTrade(self.app, type)
                self.windowTrade.show()
        else:
            self.windowTrade = windowTrade(self.app, type)
            self.windowTrade.show()

    def showWindowParty(self, event, type: str):
        if hasattr(self, "windowParty"):
            if not self.windowParty.isVisible():
                self.windowParty.destroy()
                self.windowParty = windowParty(self.app, type)
                self.windowParty.show()
        else:
            self.windowStock = windowParty(self.app, type)
            self.windowStock.show()

    def showWindowStock(self, event):
        if hasattr(self, "windowStock"):
            if not self.windowStock.isVisible():
                self.windowStock.destroy()
                self.windowStock = windowStock(self.app)
                self.windowStock.show()
        else:
            self.windowStock = windowStock(self.app)
            self.windowStock.show()

    def resizeEvent(self, event):
        if event.size().width() != event.oldSize().width():
            setFullWidth(self, self.heading, 100)

# Helper Functions

def removeType(dataList: list):
    for dict in dataList:
        del dict["type"]
    return dataList

def setEvents(self, buttonPressed: QPushButton, inputDetails: dict, layout: QGridLayout, type = None, data = None):
        textOfButtonClicked = buttonPressed.text()
        if textOfButtonClicked == "Add":
            inputs = setInputs(self, textOfButtonClicked, inputDetails, layout)
            if type:
                inputs["submit"].clicked.connect(lambda: self.submitAdd(inputs, type))
            else:
                inputs["submit"].clicked.connect(lambda: self.submitAdd(inputs))
        elif textOfButtonClicked == "Edit":
            inputs = setInputs(self, textOfButtonClicked, inputDetails, layout)
            if type:
                inputs["submit"].clicked.connect(lambda: self.submitEdit(inputs, type))
            else:
                inputs["submit"].clicked.connect(lambda: self.submitEdit(inputs))
            inputs["id"].textEdited.connect(lambda: fillInputsById(inputs["id"].text(), inputs, data))
        elif textOfButtonClicked == "Delete":
            inputs = setInputs(self, textOfButtonClicked, inputDetails, layout)
            if type:
                inputs["submit"].clicked.connect(lambda: self.submitDelete(inputs, type))
            else:
                inputs["submit"].clicked.connect(lambda: self.submitDelete(inputs))
        else:
            return
        
def setupTable(table: QTableWidget, listOfDict: list[dict]):
    headers = list(listOfDict[0].keys())
    table.setRowCount(len(listOfDict) + 1)
    table.setColumnCount(len(headers))
    for index, header in enumerate(headers):
        # table.setHorizontalHeaderItem(index, QTableWidgetItem(header.upper()))
        item = QTableWidgetItem(header[0].upper() + header[1:])
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(0, index, item)

    for rowId, row in enumerate(listOfDict): # accessed individual dictionaries
        for colId, cell in enumerate(row.values()):
            if type(cell) == dict:
                cell = cell["name"] + " (ID:" + str(cell["id"])  + ")"
            item = QTableWidgetItem(str(cell))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(rowId + 1, colId, item)
    table.horizontalHeader().setHidden(True)
    table.verticalHeader().setHidden(True)
    table.setFont(QFont(FONT, 10))
    for col in range(table.columnCount()):
        table.setColumnWidth(col, 150)
        table.item(0, col).setFont(QFont(FONT, 12, 600))
    for row in range(1, table.rowCount()):
        table.item(row, 0).setFont(QFont(FONT, 10, 600))
    table.setAlternatingRowColors(True)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionMode(QTableWidget.NoSelection)
    table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
    # table.setStyleSheet(f"QTableWidget::item:selected {{ background-color: {COLOR_SELECTION}; }}")
    table.setStyleSheet(f"""
                            QTableWidget {{
                                border: none;
                            }}
                            QTableWidget::item {{
                                background-color: {COLOR_SECONDARY};
                                border: 1px solid {COLOR_SECONDARY_DARK};
                            }}""")

def createHeading(self, container, text: str):
    heading = QLabel(text, container)
    heading.setFont(QFont(FONT, FONT_SIZE_HEADING))
    setFullWidth(self, heading, 100)
    heading.setStyleSheet(f'''
                                color: {COLOR_SECONDARY};
                                font-weight: bold;
                            ''')
    heading.setAlignment(Qt.AlignCenter)
    return heading

def setInputs(self: QMainWindow, task: str, inputs: dict, layout: QGridLayout):
    rowCount = layout.rowCount()
    inputDict = {}
    inputDict["labels"] = []
    for key, input in inputs.items():
        input.setVisible(True)
        inputDict[key] = input
        labeltext = key[0].upper() + key[1:]
        if input.__class__.__qualname__ == "QLineEdit": # check if is simple text input
            inputDict[key].setPlaceholderText(labeltext)
        inputDict["labels"].append(QLabel(labeltext))
        styleLabel(inputDict["labels"][-1])
        layout.addWidget(inputDict["labels"][-1], rowCount, 1, 1, 3) # adding label
        styleInput(inputDict[key])
        layout.addWidget(inputDict[key], rowCount + 1, 1, 1, 3) # adding input
        rowCount += 2
    inputDict["submit"] = QPushButton(task)
    inputDict["close"] = QPushButton("Close")
    styleButton(inputDict["submit"])
    styleButton(inputDict["close"])
    layout.addWidget(inputDict["close"], (rowCount + 1), 1)
    layout.addWidget(inputDict["submit"], (rowCount + 1), 3)
    inputDict["close"].clicked.connect(lambda: resetInputs(self, list(inputDict.values()))) # nested list passed in
    self.btnAdd.setVisible(False)
    self.btnEdit.setVisible(False)
    self.btnDelete.setVisible(False)
    return inputDict

def resetInputs(self, toRemove: list):
    self.btnAdd.setVisible(True)
    self.btnEdit.setVisible(True)
    self.btnDelete.setVisible(True)
    for element in toRemove:
        if type(element) == list:
            resetInputs(self, element)
        elif element.__class__.__qualname__ == "QLabel":
            element.deleteLater()
        else:
            element.setVisible(False)
    
def formatErrorInStr(errors: list):
    result = "The following errors have occured:\n"
    for error in errors:
        result += "  - " + error + "\n"
    return result

def getConfirmation(title: str, message: str):
    dialogue = QMessageBox()
    dialogue.setWindowTitle(title)
    dialogue.setText(message)
    dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    dialogue.setStyleSheet(f'''
                           QMessageBox {{
                                background-color: {COLOR_PRIMARY};
                            }}
                            QMessageBox QLabel {{
                                color: {COLOR_SECONDARY};
                            }}
                                ''')
    dialogue.setIcon(QMessageBox.Question)
    button = dialogue.exec()
    if button == QMessageBox.Yes:
        return True
    return False

def displayError(title: str, message: str):
    dialogue = QMessageBox()
    dialogue.setWindowTitle(title)
    dialogue.setText(message)
    dialogue.setIcon(QMessageBox.Critical)
    dialogue.setFont(QFont(FONT, 10))
    dialogue.setStyleSheet(f'''
                           QMessageBox {{
                                background-color: {COLOR_PRIMARY};
                            }}
                            QMessageBox QLabel {{
                                color: {COLOR_SECONDARY};
                            }}
                                ''')
    dialogue.exec()

def checkError_Float(inp: str, type: str):
    errors = []
    if inp == "":
        errors.append(f"{type} input is empty.")
    elif len(inp) > 255:
        errors.append(f"{type} is too high.")
    elif not is_number(inp):
        errors.append(f"{type} is invalid.")
    return errors

def checkError_Id(inp: str, type: str, listOfDict: list):
    errors = []
    if inp == "":
        errors.append(f"{type} input is empty.")
    elif len(inp) > 255:
        errors.append(f"{type} is too long.")
    elif not inp.isdigit():
        errors.append(f"{type} is invalid.")
    elif not getDictById(str(inp), listOfDict):
        errors.append(f"{type} match not found.")
    return errors

def checkError_Text(inp: str, type: str):
    errors = []
    if inp == "":
        errors.append(f"{type} input is empty.")
    elif len(inp) > 255:
        errors.append(f"{type} is too long.")
    return errors

def is_number(string):
    if string.isnumeric():
        return True
    if string.count('.') == 1:
        if string.replace('.', '').isnumeric():
            return True
    return False

def styleInput(inp: QLineEdit):
    inp.setStyleSheet(f'''
                      color: {COLOR_SECONDARY};
                    ''')
    inp.setAlignment(Qt.AlignVCenter)
    inp.setFont(QFont(FONT, 15))
    inp.setFixedHeight(30)

def styleLabel(inp: QLabel):
    inp.setStyleSheet(f'''
                      color: {COLOR_SECONDARY};
                    ''')
    inp.setAlignment(Qt.AlignVCenter)
    inp.setFont(QFont(FONT, 15))
    inp.setFixedHeight(20)

def getDictById(id: str, listOfDict: list[dict]):
    result = {}
    for dict in listOfDict:
        if id == str(dict.get("id")):
            result = dict
    return result

def fillInputsById(id: str, inputs: dict, listOfDict: list[dict]):
    dictionary = getDictById(id, listOfDict)
    if dictionary:
        for key, value in dictionary.items():
            if type(value) == dict:
                key += "_id"
                value = value["id"]
            if key != "id" and inputs.get(key):
                inputs[key].setText(str(value))
    else:
        clearInputs(inputs)

def clearInputs(inputs: dict):
    for key, input in inputs.items():
        if key not in ["id", "submit", "labels", "close"]:
            input.setText("")

def setFullWidth(self, widget, height):
    window_width = self.width()
    widget.setGeometry(0, 0, window_width, height)

def styleButton(button: QPushButton):
    button.setMinimumHeight(40)
    button.setMinimumWidth(150)
    button.setFont(QFont(FONT, 16))
    button.setStyleSheet(f'''
                        QPushButton {{
                            color: {COLOR_PRIMARY};
                            background-color: {COLOR_SECONDARY};
                            border: none;
                            border-radius: 5px;
                        }}
                        QPushButton::hover {{
                            background-color: {COLOR_SECONDARY_DARK};
                        }}
                        QPushButton::pressed{{
                            background-color: {COLOR_SECONDARY};
                        }}
                        ''')

def getWindowSize(app: QApplication, widthRatio, heightRatio):
        # get screen size
    screen = app.primaryScreen().size()
        # calculate window size according to ratio
    width = int (screen.width() * widthRatio)
    height = int (screen.height() * heightRatio)
        # calculate window position by dividing remaining space by 2 to keep on top and left
    pos_x = (screen.width() - width) // 2
    pos_y = (screen.height() - height) // 2
    return QRect(pos_x, pos_y, width, height)

def main():
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

if databaseHandler.con:
    databaseHandler.con.close()