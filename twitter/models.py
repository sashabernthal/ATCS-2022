"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    username = Column("username", TEXT, unique=True, nullable=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.id==Follower.follower_id",
                             secondaryjoin="User.id==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.id==Follower.following_id",
                             secondaryjoin="User.id==Follower.follower_id",
                             overlaps="following")
                             
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "@" + self.username


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id

class Tweet(Base):
    __tablename__ = "tweet"

    id = Column("id", INTEGER, primary_key=True)
    content = Column('content', TEXT)
    timestamp = Column('timestamp', DATETIME)
    username = Column('username', TEXT, ForeignKey('users.username'))
    tags = relationship("Tag", secondary="tweettag", back_populates="tweets")

    def __init__(self, content, timestamp, username):
        self.content = content
        self.timestamp = timestamp
        self.username = username

    def __repr__(self):
        string = ""
        for tag in self.tags:
            string = string + " " + tag.content
        return "@" + self.username + self.content + string + self.timestamp

class Tag(Base):
    __tablename__ = "tag"

    id = Column("id", INTEGER, primary_key=True)
    content = Column('content', TEXT)
    tweets = relationship("Tweet", secondary="tweettag", back_populates="tags")

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return "#" + self.content

class TweetTag(Base):
    __tablename__ = "tweettag"

    id = Column("id", INTEGER, primary_key=True)
    tweet_id = Column("tweet_id", INTEGER, ForeignKey('tweet.id'))
    tag_id = Column("tag_id", INTEGER, ForeignKey('tag.id'))

    def __init__(self, tweet_id, tag_id):
        self.tweet_id = tweet_id
        self.tag_id = tag_id
