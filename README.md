# Inventory & Accounting Management System

![Python](https://img.shields.io/badge/Python-3.x-blue) ![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green) ![SQLite](https://img.shields.io/badge/Database-SQLite-orange) ![License](https://img.shields.io/badge/License-Open%20Source-brightgreen)

**Tags:** 

A comprehensive desktop application for managing inventory, sales, purchases, customer/supplier records, and financial transactions built with Python and PyQt5.

## Features

### Core Modules

- **Stock Management** - Track inventory items with quantities and units  

- **Customer Management** - Maintain customer records with contact details  

- **Supplier Management** - Manage supplier information and relationships  

- **Sales Tracking** - Record sales transactions with automatic stock updates  

- **Purchase Management** - Log purchases with inventory adjustments  

- **Payment Processing** - Track receipts from customers  

- **Payment Records** - Monitor payments to suppliers  

- **Ledger System** - Generate party-wise ledger reports with balance calculations  

### Key Capabilities

- **Real-time Stock Updates** - Automatic inventory adjustments on sales/purchases  

- **Data Validation** - Comprehensive input validation and error handling  
  `#DataValidation` `#ErrorHandling`

- **Transaction Integrity** - Automatic stock quantity updates when adding/editing/deleting trades  

- **Ledger Generation** - Party-wise transaction history with running balances  

- **User-friendly Interface** - Clean, intuitive GUI with consistent styling  

- **Data Synchronization** - Real-time data refresh to prevent conflicts  
  
## Technology Stack

| Component | Technology | Tags |
|-----------|------------|------|
| **Language** | Python 3.x | `#Python3` |
| **GUI Framework** | PyQt5 | `#PyQt5` `#DesktopGUI` |
| **Database** | SQLite3 | `#SQLite` `#Database` |
| **Architecture** | Desktop application with modular design | `#ModularDesign` `#SoftwareArchitecture` |

## Database Schema

The application expects a SQLite database with the following tables:

### Stock Table
| Field | Type | Description |
|-------|------|-------------|
| `id` | Primary key | Unique identifier |
| `name` | Text | Item name |
| `quantity` | Float | Current quantity |
| `unit` | Text | Unit of measurement |

### Parties Table
| Field | Type | Description |
|-------|------|-------------|
| `id` | Primary key | Unique identifier |
| `name` | Text | Party name |
| `type` | Text | "Customer" or "Supplier" |
| `number` | Text | Contact number |
| `email` | Text | Email address |
| `address` | Text | Physical address |

### Trades Table
| Field | Type | Description |
|-------|------|-------------|
| `id` | Primary key | Unique identifier |
| `_date` | Text | Transaction date |
| `type` | Text | "Sale" or "Purchase" |
| `party_id` | Foreign key | References parties table |
| `item_id` | Foreign key | References stock table |
| `quantity` | Float | Quantity traded |
| `rate` | Float | Price per unit |

### Payments Table
| Field | Type | Description |
|-------|------|-------------|
| `id` | Primary key | Unique identifier |
| `_date` | Text | Payment date |
| `type` | Text | "Receipt" or "Payment" |
| `party_id` | Foreign key | References parties table |
| `amount` | Float | Payment amount |

## Usage

### Main Dashboard
The main window provides access to all modules through clearly labeled buttons:
- **Sales, Purchases, Stock, Customers, Suppliers, Receipts, Payments, Ledgers**

### Adding Records
1. Click the respective module button
2. Click **"Add"** in the module window
3. Fill in the required fields
4. Confirm the transaction

### Editing Records
1. Navigate to the relevant module
2. Click **"Edit"**
3. Enter the ID of the record to edit
4. Modify the fields as needed
5. Confirm changes

### Generating Ledgers
1. Click **"Ledgers"** from the main menu
2. Select a customer or supplier from the dropdown
3. View the complete transaction history with running balance

## File Structure

```
eu-accounts/
├── main.py              # Main application entry point and GUI
├── databaseHandler.py   # Database operations and business logic
├── sqlite.db           # SQLite database file
├── Images/
│   └── icon.ico        # Application icon
└── README.md           # This file
```

## Key Features Explained

### Automatic Stock Management
- ✅ Sales automatically reduce stock quantities
- ✅ Purchases automatically increase stock quantities
- ✅ Editing/deleting trades adjusts stock accordingly

### Data Integrity
- ✅ Input validation prevents invalid data entry
- ✅ Transaction rollback on errors
- ✅ Real-time sync checking to prevent concurrent modification issues

### Ledger System
- ✅ Combines trade and payment data
- ✅ Calculates running balances
- ✅ Separates debit/credit based on party type (Customer vs Supplier)



