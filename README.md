## install dependencies
pip install -r requirements.txt

## run the programe
python main.py


## API Documentation
=> go to fastapi swagger ui

## Default

1. /user/create/ => This is a POST request. This will perform new user registration. 
    Body should have -> "username", "email", "password"
    

2. /payment-form/create => This is a POST request. This api will create new payment form but need to be logged in.
    Body should have -> "form-name", "description", "amount", "currency"
    

3. /get-all-forms => This is a GET request. This api will show all the form of a perticular logged in user.

4. /payment-form/{user_id}/{name} => This is a GET request. This can be used for getting the form_id of a perticular user with a specific form_name.

5. /transaction/{user_id}/{form_id} => This is a POST request. This will make the transaction for a specific url.
     Body should have -> "user_id", "form_id", "date", "is_succeded", "amount"

6. /transactions => This is a GET request. This will show all the logged transaction of a perticular user.
