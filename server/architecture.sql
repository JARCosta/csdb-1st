

drop table if exists item_prices cascade;
drop table if exists profile_items cascade;
drop table if exists items cascade;
drop table if exists profiles cascade;


CREATE TABLE profiles (
  steamid VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE items (
  name VARCHAR(255) PRIMARY KEY,
  type VARCHAR(255) NOT NULL
);



CREATE TABLE profile_items (
  profile VARCHAR(255) NOT NULL,
  item VARCHAR(255) NOT NULL,
  quantity INT NOT NULL,
  auto BOOL DEFAULT TRUE,
  PRIMARY KEY (profile, item),
  FOREIGN KEY (profile) REFERENCES profiles(steamid),
  FOREIGN KEY (item) REFERENCES items(name)
);

CREATE TABLE item_prices (
  item VARCHAR(255) NOT NULL,
  -- date VARCHAR(255) NOT NULL,
  date TIMESTAMP NOT NULL,
	price DECIMAL(10,2) NOT NULL,
	PRIMARY KEY (item, date),
  FOREIGN KEY (item) REFERENCES items(name)
);