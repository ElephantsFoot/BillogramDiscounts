# Billogram Discounts Project
`pip3 install -r requirements.txt` - to install all the requirements\
`python3 setup_db.py` - to set up the SQLite database\
`pytest tests/` - to run the tests\
`python3 main.py` - to run the server locally

Requests:

1. Create a discount_code:
        
        curl --location --request POST 'http://127.0.0.1:5000/discount_code' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "company_id": 1,
            "user_id": 1
        }'
        
1. Use a discount_code:
        
        curl --location --request POST 'http://127.0.0.1:5000/use_discount_code' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "discount_code": "16dd1180ffce4d69a46351e8b858e53e",
            "company_id": 1,
            "user_id": 1
        }'

1. Get user ids for the users that shared their data with certain company:

        curl --location --request GET 'http://127.0.0.1:5000/users_shared_data?company_id=1'