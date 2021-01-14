CREATE TABLE webseries
(
	webseries_id		uniqueidentifier DEFAULT NEWID()		 PRIMARY KEY,
	webseries_name		VARCHAR(128) UNIQUE NOT NULL,
	last_issue_read		INTEGER,
	latest_URL			VARCHAR(128) NOT NULL,
	base_URL			VARCHAR(128) NOT NULL,
	latest_index		INTEGER NOT NULL
);

CREATE TABLE webcomics_issue_locations
(
	webseries_issue_id	uniqueidentifier DEFAULT NEWID()		PRIMARY KEY,
	webseries_id		uniqueidentifier	FOREIGN KEY REFERENCES webseries(webseries_id),
	issue				INTEGER				NOT NULL,
	issue_location		VARCHAR(128)		UNIQUE

);

CREATE TABLE missed_comics
(
	missed_comic_id		uniqueidentifier	DEFAULT NEWID()		PRIMARY KEY,
	webseries_id		uniqueidentifier	FOREIGN KEY REFERENCES webseries(webseries_id),
	missed_URL			VARCHAR(128)		UNIQUE
);