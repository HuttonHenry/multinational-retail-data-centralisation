Milestone 3.1 I wrote a convoluted SQL query to automatically collect data and then alter the table.

But I hit issues.  At the bototm I added a straight forward alter 

DO $$
DECLARE 
    card_number_max_length INTEGER;
    store_code_max_length INTEGER;
    product_code_max_length INTEGER;
    alter_query VARCHAR(1000);
BEGIN
    -- Get max lengths of fields
    SELECT 
        MAX(CHAR_LENGTH(card_number)) AS card_number_max_length,
        MAX(CHAR_LENGTH(store_code)) AS store_code_max_length,
        MAX(CHAR_LENGTH(product_code)) AS product_code_max_length
    INTO 
        card_number_max_length, store_code_max_length, product_code_max_length
    FROM 
        orders_table;
        
    -- Construct the alter query string
    alter_query := 'ALTER TABLE orders_table 
                        ALTER COLUMN date_uuid SET DATA TYPE UUID USING date_uuid::UUID,
                        ALTER COLUMN user_uuid SET DATA TYPE UUID USING user_uuid::UUID,
                        ALTER COLUMN card_number SET DATA TYPE VARCHAR(' || card_number_max_length || '),
                        ALTER COLUMN store_code SET DATA TYPE VARCHAR(' || store_code_max_length || '),
                        ALTER COLUMN product_code SET DATA TYPE VARCHAR(' || product_code_max_length || '),
                        ALTER COLUMN product_quantity SET DATA TYPE SMALLINT;';
                        
    -- Execute the alter query
    EXECUTE alter_query;
END $$;
In this modified code, the LENGTH function is replaced with the CHAR_LENGTH function, which returns the number of characters in a string in Postgres. The rest of the code is similar to the previous version, with the ALTER TABLE statement constructed as a string and executed using EXECUTE.




hutton@beyond-ma.com
same issue by the looks of it:

ERROR:  function char_length(bigint) does not exist
LINE 2:         MAX(CHAR_LENGTH(card_number)) AS card_number_max_len...
                    ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
QUERY:  SELECT 
        MAX(CHAR_LENGTH(card_number)) AS card_number_max_length,
        MAX(CHAR_LENGTH(store_code)) AS store_code_max_length,
        MAX(CHAR_LENGTH(product_code)) AS product_code_max_length
                                                                                             FROM 
        orders_table
CONTEXT:  PL/pgSQL function inline_code_block line 9 at SQL statement
SQL state: 42883
In PostgreSQL, the function for getting the length of a string is LENGTH(). Please try using LENGTH() instead of CHAR_LENGTH(). Heres the corrected query:

sql
Copy code
SELECT 
  MAX(LENGTH(card_number)) AS card_number_max_length,
  MAX(LENGTH(store_code)) AS store_code_max_length,
  MAX(LENGTH(product_code)) AS product_code_max_length
FROM 
  orders_table;



STRAIGHT FORWARD:

alter table orders_table
	alter column date_uuid set data type UUID USING date_uuid::uuid,
	alter column user_uuid set data type UUID USING user_uuid::uuid,
	alter column card_number set data type VARCHAR(30),
	alter column store_code set data type VARCHAR(20),
	alter column product_code set data type VARCHAR(20),
	alter column product_quantity set data type SMALLINT;
	


Milestone 3.2

The column required to be changed in the users table are as follows:

+----------------+--------------------+--------------------+
| dim_user_table | current data type  | required data type |
+----------------+--------------------+--------------------+
| first_name     | TEXT               | VARCHAR(255)       |
| last_name      | TEXT               | VARCHAR(255)       |
| date_of_birth  | TEXT               | DATE               |
| country_code   | TEXT               | VARCHAR(?)         |
| user_uuid      | TEXT               | UUID               |
| join_date      | TEXT               | DATE               |
+----------------+--------------------+--------------------+

Both the date columns had invalid data in them, so I ran SQL queries to delete those records

SELECT *
FROM dim_users
WHERE join_date ~ '[a-zA-Z]';

DELETE FROM dim_users
WHERE join_date ~ '[a-zA-Z]';

DELETE FROM dim_users
WHERE date_of_birth ~ '[a-zA-Z]';

And then we ran the alter statements

alter table dim_users
	alter column first_name set data type VARCHAR(255),
	alter column last_name set data type VARCHAR(255),
	alter column date_of_birth set data type DATE using to_date(date_of_birth,'yyyy-mm-dd'),
	alter column country_code set data type VARCHAR(10),
	alter column user_uuid set data type UUID using user_uuid::uuid,
	alter column join_date set data type DATE using to_date(join_date,'yyyy-mm-dd');

    







