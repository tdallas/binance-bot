CREATE DATABASE alt_bot_service;

USE alt_bot_service;
CREATE TABLE pairs
(
    pair varchar(255),
    date datetime,
    traded bool,
    buy_price double,
    PRIMARY KEY (pair)
)