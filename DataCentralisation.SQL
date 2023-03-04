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
 

Task 3.3
We added a column for the latitude merge

ALTER TABLE dim_store_details ADD COLUMN latitude_new text;

Then we merged the data into the database.
UPDATE dim_store_details SET latitude_new = CONCAT(lat, ' ', latitude);

Then I had to get rid of NULL records
But the NULL wasn't working so I deleted two manually

delete FROM dim_store_details WHERE level_0=405;
delete FROM dim_store_details WHERE latitude='N/A';
delete FROM dim_store_details WHERE longitude='N/A';

Then deleted records where there was alpha chars in the wrong fields
DELETE
FROM dim_store_details
WHERE staff_numbers !~ '^\d+$';


Milestone 3.4:
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')

Milestone 3.5
Now we change the data type for all fields as they have been cleaned.

ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT

ALTER TABLE dim_products
ALTER COLUMN weight TYPE FLOAT USING weight::FLOAT

ALTER COLUMN EAN TYPE VARCHAR(255)

Before changing still_availble to boolean I had to change the underlying data:

UPDATE dim_products
SET still_available = 
  CASE
    WHEN still_available = 'Still_available' THEN '1'
    WHEN still_available = 'Removed' THEN 0
	ELSE '1'
  END;

  And then:

  ALTER TABLE dim_products
ALTER COLUMN still_available TYPE BOOL USING still_available::boolean

I used the GUI to change some fields as this was quicker.  No need to recreate this environent going forwards..6 