from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:

    def __init__(self, current_user=None, logged_in=False):
        self.current_user = current_user
        self.logged_in = logged_in

    """
    The menu to print once a user has logged in
    """

    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """

    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """

    def register_user(self):
        users = db_session.query(User).all()
        while True:
            username = input("What username would you like?")
            password = input("What do you want your password to be?")
            password_check = input("Please enter your password again.")
            pass_check = db_session.query(User).filter(User.username == username).all()
            if (password_check == password and len(pass_check) == 0):
                break
            else:
                print("Error. Passwords don't match. Please try again.")
        new_user = User(username=username, password=password)
        self.logged_in = True
        self.current_user = new_user
        db_session.add(new_user)
        db_session.commit()
        print("Welcome to Twitter," + username)


    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """


    def login(self):
        while(True):
            username = input("Input username:")
            password = input("Input password:")
            account = db_session.query(User).filter(User.password == password and User.username == username).first()
            if account is not None and account.username == username and account.password == password:
                break
            else:
                print("Incorrect login information, please try again.")
        print("Login succesful. Welcome.")
        self.logged_in = True
        self.current_user = account

    
    def logout(self):
        self.logged_in = False
        self.current_user = None
        print("Logout succesful.")

    """
    Allows the user to login,  
    register, or exit.
    """
    
    def startup(self):
        print("Welcome to Twitter!")
        while True:
            option = input("Enter login to login, register to register, or exit to exit.")
            if option == "login":
                self.login()
                break
            elif option == "register":
                self.register_user()
                break
            elif option == "exit":
                print("Exiting.")
                self.end()
            else:
                print("Please try again.")
                

    def follow(self):
        while True:
            username = input("Enter the user's name who you would like to follow. ")
            follow_user = db_session.query(User).where(User.username==username).first()
            if follow_user:
                break
            else:
                print("Cannot find user.")
        
        self.current_user.following.append(follow_user)
        db_session.commit()
        print("You followed @" + username)


    def unfollow(self, current_user_id, unfollowing_id):
        current_user = db_session.query(User).filter_by(id=current_user_id).first()
        unfollowing = db_session.query(User).filter_by(id=unfollowing_id).first()
        current_user.following.remove(unfollowing)
        db_session.commit()
        print("You unfollowed @" + unfollowing)

    def tweet(self):
        tweet = input("Please write what you wanna tweet.")
        tags = input("What tags would you like to add to your tweet?")
        if tweet and tags:
            tag_list = tags.split()
            create_tweet = Tweet(tweet, datetime.now(), self.current_user.username)
            for tag in tag_list:
                create_tag = Tag(tag)
                create_tweet.tags.append(create_tag)
        db_session.add(create_tweet)
        db_session.commit()
        print(create_tweet)

    
    def view_my_tweets(self):
        result = db_session.query(Tweet).filter(self.current_user.username == Tweet.username).all()
        for tweet in result:
            print(tweet)
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        tweets = db_session.query(Tweet).join(Follower, Tweet.username == Follower.following_id).where(self.current_user.username == Follower.follower_id).order_by(Tweet.timestamp.desc()).limit(5).all()
        for tweet in tweets:
            print(tweet)

    def search_by_user(self):
        username = input("Enter the username of the user who's tweets you want to see: ")
        tweets = db_session.query(Tweet).filter_by(username=username).all()
        print("Tweets by " + username)
        for tweet in tweets:
            print(tweet)

    def search_by_tag(self):
        tag_search = input("Enter the tag you'd like to search for: ")
        tags = db_session.query(Tag).filter_by(tag_search = Tag.content).all()
        # for tag in tags:
        #     tweet = tag_search
        #     print(tweet)

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        self.print_menu()
        option = int(input(""))

        if option == 1:
            self.view_feed()
        elif option == 2:
            self.view_my_tweets()
        elif option == 3:
            self.search_by_tag()
        elif option == 4:
            self.search_by_user()
        elif option == 5:
            self.tweet()
        elif option == 6:
            self.follow()
        elif option == 7:
            self.unfollow()
        else:
            self.logout()
        
        self.end()
