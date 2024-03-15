CREATE DATABASE banking_data ;
USE banking_data;

CREATE TABLE users (
	user_id INT PRIMARY KEY auto_increment UNIQUE,
    username VARCHAR(200) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
	account_id INT PRIMARY KEY auto_increment UNIQUE, 
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    account_type ENUM('savings', 'trading', 'platinum') NOT NULL,
    account_number VARCHAR(255) NOT NULL UNIQUE,
    balance DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
	transaction_id INT PRIMARY KEY auto_increment UNIQUE,
    from_account_id INT,
    to_account_id INT,
	FOREIGN KEY (from_account_id) REFERENCES Accounts (account_id),
	FOREIGN KEY (to_account_id) REFERENCES Accounts (account_id),
    type_transaction ENUM('deposit', 'withdrawal', 'transfer') NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- EXAMPLE QUERY 
SELECT *
FROM transactions
WHERE from_account_id = 1 OR to_account_id = 1;

SELECT *
FROM accounts
WHERE user_id = 2;

SELECT *
FROM accounts
WHERE balance > 10.00;

-- SHOW TABLE 
SELECT * FROM users;
SELECT * FROM accounts;
SELECT * FROM transactions;

-- DELETING TABLE
DROP TABLE transactions;
DROP TABLE users; 
DROP TABLE accounts;