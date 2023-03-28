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
            pass_check = db_session.query(User).where(User.username == username).all()
            if (password_check == password and pass_check == None):
                break
            else:
                print("Error. Passwords don't match. Please try again.")
        new_user = username(username, password)
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
            account = db_session.query(User).where(User.password == password and User.username == username).first()
            if(account.username == username and account.password == password):
                break
            else:
                print("Incorrect login information, please try again.")
        print("Login succesful. Welcome.")
        self.logged_in = True
        self.current_user = account

    
    def logout(self):
        self.logged_in = False

    """
    Allows the user to login,  
    register, or exit.
    """
    
    def startup(self):
        pass

    def follow(self):
        following_id = input("Who would you like to follow?")
        following_user = db_session.query()

    def unfollow(self):
        

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

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
