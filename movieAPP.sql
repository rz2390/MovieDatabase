DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS Director;
DROP TABLE IF EXISTS Region;
DROP TABLE IF EXISTS Keyword;
DROP TABLE IF EXISTS Wishlist;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Perform;
DROP TABLE IF EXISTS Direct;
DROP TABLE IF EXISTS Show;
DROP TABLE IF EXISTS Vote;

CREATE TABLE movie
(
    movieID SERIAL NOT NULL,
    title TEXT NOT NULL,
    popularity INT,
    genre TEXT,
    revenue INT,
    PRIMARY KEY(movieID),
);

CREATE TABLE user
(
    userID SERIAL NOT NULL,
    password TEXT NOT NULL,
    nickname TEXT,
    age INT,
    gender TEXT,
    imageURL TEXT,
    email TEXT,
    description TEXT,
    PRIMARY KEY(userID),
    CONSTRAINT valid_age CHECK (age > 0 AND Age < 100),
    CONSTRAINT valid_gender CHECK (gender = 'male' OR gender = 'female')
);

CREATE TABLE actor
(
    actID SERIAL NOT NULL,
    gender TEXT,
    name TEXT NOT NULL,
    age INT,
    PRIMARY KEY(actID),
    CONSTRAINT valid_age CHECK (age > 0 AND Age < 100),
    CONSTRAINT valid_gender CHECK (gender = 'male' OR gender = 'female')
);

CREATE TABLE director
(
    directorID SERIAL NOT NULL,
    gender TEXT,
    name TEXT NOT NULL,
    age INT,
    recognition TEXT,
    PRIMARY KEY(directorID),
    CONSTRAINT valid_age CHECK (age > 0 AND Age < 100),
    CONSTRAINT valid_gender CHECK (gender = 'male' OR gender = 'female')
);

CREATE TABLE region
(
    regionID SERIAL NOT NULL,
    country TEXT,
    language TEXT NOT NULL,
    PRIMARY KEY(regionID),
);

CREATE TABLE Keyword
(
    keywordID SERIAL NOT NULL,
    userID SERIAL NOT NULL,
    movieID SERIAL NOT NULL,
    content TEXT NOT NULL,
    modifiedTime TIMESTAMP,
    PRIMARY KEY(keywordID),
    FOREIGN KEY(userID)REFERENCES User ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES Movie ON DELETE CASCADE,
    CONSTRAINT User_Keyword_Movie UNIQUE(keywordID,userID,movieID)
);

CREATE TABLE Wishlist
(
    wishlistID SERIAL NOT NULL,
    userID SERIAL NOT NULL,
    movieID SERIAL NOT NULL,
    comment TEXT NOT NULL,
    modifiedTime TIMESTAMP,
    PRIMARY KEY(keywordID),
    FOREIGN KEY(userID)REFERENCES User ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES Movie ON DELETE CASCADE,
    CONSTRAINT User_Wishlist_Movie UNIQUE(keywordID,userID,movieID)
);

CREATE TABLE Review
(
    reviewID SERIAL NOT NULL,
    userID SERIAL NOT NULL,
    movieID SERIAL NOT NULL,
    comment TEXT NOT NULL,
    rating INT NOT NULL,
    vote INT,
    modifiedTime TIMESTAMP,
    PRIMARY KEY(keywordID),
    FOREIGN KEY(userID)REFERENCES User ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES Movie ON DELETE CASCADE,
    CONSTRAINT valid_rate CHECK (Rate > 0 AND Rate < 6),
    CONSTRAINT User_Review_Movie UNIQUE(keywordID,userID,movieID)
);

CREATE TABLE Perform
(
    actID SERIAL NOT NULL,
    movieID SERIAL NOT NULL,
    modifiedTime TIMESTAMP,
    PRIMARY KEY(actID,movieID),
    FOREIGN KEY(actID)REFERENCES Actor ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES Movie ON DELETE CASCADE,
);

CREATE TABLE Direct
(
    directorID SERIAL NOT NULL,
    movieID SERIAL NOT NULL,
    modifiedTime TIMESTAMP,
    PRIMARY KEY(actID,movieID),
    FOREIGN KEY(actID)REFERENCES Actor ON DELETE CASCADE,
    FOREIGN KEY(movieID)REFERENCES Movie ON DELETE CASCADE,    
);

CREATE TABLE Vote
(
    userID SERIAL NOT NULL,
    reviewID SERIAL NOT NULL,
    modifiedTime TIMESTAMP,
    PRIMARY KEY(userID,reviewID),
    FOREIGN KEY(userID)REFERENCES User ON DELETE CASCADE,
    FOREIGN KEY(reviewID)REFERENCES Review ON DELETE CASCADE,
);
