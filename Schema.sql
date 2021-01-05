USE urlshortener;

CREATE TABLE urls(
    id INT AUTO_INCREMENT PRIMARY KEY,
    link VARCHAR(100),
    short_url VARCHAR(100) UNIQUE,
    visitors INT DEFAULT 0
);

SHOW TABLES;

INSERT INTO urls (link, short_url) VALUES ("https://google.com", "gl");

SELECT * FROM urls;