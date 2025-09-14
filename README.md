# Inventory & Accounting Management System
# A comprehensive desktop application for managing inventory, sales, purchases, customer/supplier records, and financial transactions built with Python and PyQt5.
Features
Core Modules

Stock Management - Track inventory items with quantities and units
Customer Management - Maintain customer records with contact details
Supplier Management - Manage supplier information and relationships
Sales Tracking - Record sales transactions with automatic stock updates
Purchase Management - Log purchases with inventory adjustments
Payment Processing - Track receipts from customers
Payment Records - Monitor payments to suppliers
Ledger System - Generate party-wise ledger reports with balance calculations

Key Capabilities

Real-time Stock Updates - Automatic inventory adjustments on sales/purchases
Data Validation - Comprehensive input validation and error handling
Transaction Integrity - Automatic stock quantity updates when adding/editing/deleting trades
Ledger Generation - Party-wise transaction history with running balances
User-friendly Interface - Clean, intuitive GUI with consistent styling
Data Synchronization - Real-time data refresh to prevent conflicts

Technology Stack

Language: Python 3.x
GUI Framework: PyQt5
Database: SQLite3
Architecture: Desktop application with modular design

Database Schema
The application expects a SQLite database with the following tables:
Stock Table

id - Primary key
name - Item name
quantity - Current quantity (float)
unit - Unit of measurement

Parties Table

id - Primary key
name - Party name
type - "Customer" or "Supplier"
number - Contact number
email - Email address
address - Physical address

Trades Table

id - Primary key
_date - Transaction date
type - "Sale" or "Purchase"
party_id - Foreign key to parties table
item_id - Foreign key to stock table
quantity - Quantity traded
rate - Price per unit

Payments Table

id - Primary key
_date - Payment date
type - "Receipt" or "Payment"
party_id - Foreign key to parties table
amount - Payment amount

Usage
Main Dashboard
The main window provides access to all modules through clearly labeled buttons:

Sales, Purchases, Stock, Customers, Suppliers, Receipts, Payments, Ledgers

Adding Records

Click the respective module button
Click "Add" in the module window
Fill in the required fields
Confirm the transaction

Editing Records

Navigate to the relevant module
Click "Edit"
Enter the ID of the record to edit
Modify the fields as needed
Confirm changes

Generating Ledgers

Click "Ledgers" from the main menu
Select a customer or supplier from the dropdown
View the complete transaction history with running balance

Key Features Explained
Automatic Stock Management

Sales automatically reduce stock quantities
Purchases automatically increase stock quantities
Editing/deleting trades adjusts stock accordingly

Data Integrity

Input validation prevents invalid data entry
Transaction rollback on errors
Real-time sync checking to prevent concurrent modification issues

Ledger System

Combines trade and payment data
Calculates running balances
Separates debit/credit based on party type (Customer vs Supplier)
