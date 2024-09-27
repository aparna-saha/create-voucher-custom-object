# Create Voucher Custom Objects

The purpose of this project is to create voucher custom objects in the Commerce Tool. These custom objects will enable the creation of additional pending vouchers, which are often needed for development and testing purposes.

## Technologies

- Python 3.8

## Setup

- Install [Virtualenv](http://www.virtualenv.org/)
- Create a virtual environment
    ``` 
    virtualenv --python=/path/to/python3.8 <virtualenv-name>
    ```
- Activate virtualenv
    ```
    source <virtualenv-name>/bin/activate # Activate environment
    ```
- Install
    ``` 
    pip dotenv
    ```

- copy `.env.example` to `.env` and add correct credentials
- Run the application

## Run the application


Now, run the create custom object command:

```
python create.py path-to-file.json
```

Update the `path-to-file.json` with the correct path to the JSON file containing the voucher data. Please refer the `staffel.json` or `data.json` file for the sample data.

To delete the custom object, run the delete custom object command:

```
python delete.py voucher-code
```

Update the `voucher-code` with the correct voucher code to delete the custom object.

To get the custom object, run the get custom object command:

```
python get.py voucher-id
```

Update the `voucher-id` with the correct voucher id to get the custom object.




