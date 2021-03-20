CREATE TABLE webseries
(
	webseries_name		VARCHAR(128) PRIMARY KEY,
	last_issue_read		INTEGER,
	latest_URL			VARCHAR(128) NOT NULL,
	base_URL			VARCHAR(128) NOT NULL,
	latest_index		INTEGER NOT NULL
);

CREATE TABLE webcomics_issue_locations
(
	webseries_name		VARCHAR(128),
	issue				INTEGER				NOT NULL,
	issue_location		VARCHAR(128)		PRIMARY KEY,
    FOREIGN KEY (webseries_name) REFERENCES webseries(webseries_name)

);

CREATE TABLE missed_comics
(
	webseries_name		VARCHAR(128),
	missed_URL			VARCHAR(128)		PRIMARY KEY,
	FOREIGN KEY (webseries_name) REFERENCES webseries(webseries_name)
);