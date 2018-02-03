CREATE TABLE movie
(
    movieID INTEGER NOT NULL,
    title VARCHAR(20) NOT NULL,
    popularity INTEGER,
    genre CHAR(20),
    revenue INTEGER,
    PRIMARY KEY(movieID),
);

CREATE TABLE user
(
    userID INTEGER NOT NULL,
    password VARCHAR(20) NOT NULL,
    nickname CHAR(20),
    age INTEGER,
    gender CHAR(20),
    imageURL VARCHAR(100),
    email VARCHAR(20),
    description TEXT,
    PRIMARY KEY(userID),
    CONSTRAINT valid_age CHECK (age > 0 AND Age < 100),
    CONSTRAINT valid_gender CHECK (gender = 'male' OR gender = 'female')
);

CREATE TABLE actor
(
    actID INTEGER NOT NULL,
    gender CHAR(20),
    name CHAR(20) NOT NULL,
    age INTEGER,
    PRIMARY KEY(actID),
    CONSTRAINT valid_age CHECK (age > 0 AND Age < 100),
    CONSTRAINT valid_gender CHECK (gender = 'male' OR gender = 'female')
);

CREATE TABLE director
(
    directorID INTEGER NOT NULL,
    gender CHAR(20),
    name CHAR(20) NOT NULL,
    age INTEGER,
    recognition CHAR(20)
    PRIMARY KEY(directorID),
    CONSTRAINT valid_age CHECK (age > 0 AND Age < 100),
    CONSTRAINT valid_gender CHECK (gender = 'male' OR gender = 'female')
);

CREATE TABLE region
(
    regionID INTEGER NOT NULL,
    country CHAR(20),
    language CHAR(20) NOT NULL,
    PRIMARY KEY(regionID),
);

CREATE TABLE Keyword
(
    keywordID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    movieID INTEGER NOT NULL,
    content CHAR(20) NOT NULL,
    modifiedTime DATE,
    PRIMARY KEY(keywordID),
    FOREIGN KEY(userID)REFERENCES User ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES Movie ON DELETE CASCADE
);

CREATE TABLE Wishlist
(
    wishlistID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    movieID INTEGER NOT NULL,
    comment CHAR(20) NOT NULL,
    modifiedTime DATE,
    PRIMARY KEY(keywordID),
    FOREIGN KEY(userID)REFERENCES User ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES Movie ON DELETE CASCADE
);

CREATE TABLE Review
(
    reviewID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    movieID INTEGER NOT NULL,
    comment CHAR(20) NOT NULL,
    rating INTEGER NOT NULL,
    vote INTEGER,
    modifiedTime DATE,
    PRIMARY KEY(keywordID),
    FOREIGN KEY(userID)REFERENCES User ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES Movie ON DELETE CASCADE,
    CONSTRAINT valid_rate CHECK (Rate > 0 AND Rate < 6)
);

CREATE TABLE Perform
(
    actID INTEGER NOT NULL,
    movieID INTEGER NOT NULL,
    modifiedTime DATE,
    PRIMARY KEY(actID,movieID),
    FOREIGN KEY(actID)REFERENCES actor ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES movie ON DELETE CASCADE,
);

CREATE TABLE Direct
(
    directorID INTEGER NOT NULL,
    movieID INTEGER NOT NULL,
    modifiedTime DATE,
    PRIMARY KEY(actID,movieID),
    FOREIGN KEY(actID)REFERENCES actor ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES movie ON DELETE CASCADE,    
);

CREATE TABLE Show
(
    regionID INTEGER NOT NULL,
    movieID INTEGER NOT NULL,
    modifiedTime DATE,
    PRIMARY KEY(actID,movieID),
    FOREIGN KEY(actID)REFERENCES actor ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES movie ON DELETE CASCADE,
);