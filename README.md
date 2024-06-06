# Vendor-Navigator
Vendor-Navigator is a Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

Setup Instructions

  -> Create a directory, open cmd in directory path  and clone Vendor-Navigator project
  
      git clone https://github.com/abynxv/Vendor-Navigator.git

  -> Install Virtual environment
  
      pip install virtualenv

  -> Create virtual environment within the directory. 
  
      python -m venv venv_name  # On Windows
      python3 -m venv venv_name  # On macOS/Linux

  -> Activate virtual environmant    
  
      venv_name\Scripts\activate       # On Windows           
      source venv_name/bin/activate     # On macOS/Linux

  -> Install requirements.txt
  
      pip install -r requirements.txt

  -> Open VendorNexus in VScode
 
      code .

  -> Open terminal in vscode, navigate to project directory, Run the server and follow link

      cd Vendor_Management
      py manage.py runserver

API Endpoints

1)Registration

    Endpoint : /api/register/ 
    Method   : POST    - Create a new user account.
    Data     : JSON    - {"username": "string","password": "string","email": "user@example.com"}

2)Login & Token Generation

    Endpoint : /api/login/
    Method   : POST    - Logging in & Create a token for registered user account.
    Data     : JSON    - {"username": "string","password": "string"}

3)Logout & Token Deletion

    Endpoint : /api/logout/
    Method   : POST    - Logging out & Delete the token for registered user account.
    Data     : JSON    - {"username": "string","password": "string"}
                         Headers - Key   : Authorization
                                   Value : Token "user_token"

4)Vendor Management

a) 

    Endpoint  : /api/vendors/
    Method    : POST   - (Create a vendor)
    Data      : JSON   - {"name": "string", "contact": "string", "address": "string"}         
b)  

    Endpoint  : /api/vendors/
    Method    : GET    - (List details of all vendors)
c)  

    Endpoint  : /api/vendors/{id}/
    Method    : GET    - (Retrieve details of a specific vendor)
d)  

    Endpoint  : /api/vendors/{id}/
    Method    : PUT    - (Update details of a specific vendor)
    Data      : JSON   - {"name": "string", "contact": "string", "address": "string"}
e)  

    Endpoint  : /api/vendors/{id}/
    Method    : DELETE - (Delete details of a specific vendor)
f)  

    Endpoint  : /api/vendors/{id}/performance/
    Method    : GET    - (Retrieve calculated performance metrics for a specific vendor)
g)  

    Endpoint  : /api/vendors/historical_performance/
    Method    : GET    - (Retrieve historical performance metrics of all vendors)
f)  

    Endpoint  : /api/vendors/{id}/historical_performance/
    Method    : GET    - (Retrieve historical performance metrics for a specific vendor)
       
5)Purchase Order Management

a)  

    Endpoint  : /api/purchase_orders/
    Method    : POST   - (Create a Purchase order)
    Data      : JSON   - {"vendor": "id", {"items": "string"}}
b)  

    Endpoint  : /api/purchase_orders/
    Method    : GET    - (List all purchase orders)
c) 

    Endpoint  : /api/purchase_orders/?vendor_id={id}/
    Method    : GET    - (List all purchase orders with an option to filter by vendor)
d)  

    Endpoint  : /api/purchase_orders/{id}/
    Method    : GET    - Retrieve details of a specific purchase order)
e)  

    Endpoint  : /api/purchase_orders/{id}/
    Method    : PUT    - (Update details of a specific purchase order)
    Data      : JSON   - {"vendor": "id", {"items": "string"}}
f)  

    Endpoint: /api/purchase_orders/{id}/
    Method: DELETE (Delete details of a specific purchase order)
g)  

    Endpoint: /api/purchase_orders/{id}/acknowledge/
    Method: POST (Acknowledge a purchase order and update acknowledgment date)
    
