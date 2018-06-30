import random
import pickle
import os
from time import sleep
#------------------------- BlackJack -------------------------------


# Every card has a rank and a face value
#
# The following Rank maps a rank into the value:
#   Ace is 11 
#   J, Q, K are 10
#   the rest of the cards 2 - 10 are face value

Ranks = {
    # Rank => Value
    '2'     :  2,
    '3'     :  3,
    '4'     :  4,
    '5'     :  5,
    '6'     :  6,
    '7'     :  7,
    '8'     :  8,
    '9'     :  9,
    '10'    : 10,
    'Jack'  : 10,
    'Queen' : 10,
    'King'  : 10,
    'Ace'   : 11
}


# Function to create the deck of cards, and randomly shuffle it.

def deck_of_cards():
    l=[]
    for k in range(4):
        for i in ['Hearts','Clubs','Diamonds','Spades']:
            for j in Ranks.keys():
                l.append(j+' of '+i)
    random.shuffle(l)
    return l

deck=deck_of_cards()
#-----------------------------------------------------------------------------------------------
# Function to deal a card
# This function is used by both the player and the dealer

def deal_a_card():
    global deck
    position=random.randint(0, len(deck)-1)
    card=deck[position]
    deck.pop(position)
    return card
#-----------------------------------------------------------------------------------------------
# Takes a card from the deck if the player decides to hit.
# return None if player stands.

def hit_or_stand(player,dealer):
    cards(player,dealer)# displays cards with player
    ch=input("Do you want to hit or stand: ").lower()
    if 'h' in ch:
        print("You have decided to hit")
        k=deal_a_card()
        print("You have recieved",k)
        return k #card taken
    elif 's' not in ch:
        print("Invalid choice")
        hit_or_stand(player,dealer)#calls function again
    print("You have decided to stand.")
    return None
#-----------------------------------------------------------------------------------------------
# This function prints the details of all the cards with both the dealer and the player.
def cards(player,dealer,k=None): 
    s=''# string for dealer's cards
    if k:
        for i in range(len(dealer)):
            if i==len(dealer)-1:
                s+=dealer[i]
                break
            s+=dealer[i]+' and '
        print("Dealer has",s)
    else:
        print("Dealer has",dealer[0],"and <hidden card>")
    s=''# string for player's cards
    for i in range(len(player)):
        if i==len(player)-1:
            s+=player[i]
            break
        s+=player[i]+' and '
    print("Your total is",check_total(player))#also prints player total
    print("You have",s)
#-----------------------------------------------------------------------------------------------
# Takes the cards with the player/dealer, and return their total

def check_total(l):
    total=0
    for i in l:
        if ('Jack' in i) or ('King' in i) or ('Queen' in i) or ('10' in i):
            total+=10
        elif 'Ace' in i:
            total+=11
        elif '2' in i:
            total+=2
        elif '3' in i:
            total+=3
        elif '4' in i:
            total+=4
        elif '5' in i:
            total+=5
        elif '6' in i:
            total+=6
        elif '7' in i:
            total+=7
        elif '8' in i:
            total+=8
        elif '9' in i:
            total+=9
        else:
            continue
    return total

#-----------------------------------------------------------------------------------------------
# Main method for blackjack

def blackjack(balance):
    print ('-'*75)
    #Multiline string
    print('''
             Welcome to the BlackJack Simulator
             You'll be asked if you want to play. Each round costs a certain amount.
             To win, you must have a total either equal to 21 or higher than that of the dealer.
             Every card has a rank and a face value
             The following Rank maps a rank into the value:
                    Ace 11 
                    J, Q, K are 10
             the rest of the cards 2 - 10 are face value
             Your total is the sum of the Face values of your cards.
             If you win, you get the bet amount from the dealer.
             If your total is greater than 21, then you are busted. i.e., you have lost.
             If both you and the dealer bust, you lose only the entry fee.
          ''')
    print()
    #player's cards, initially
    player=[deal_a_card(),deal_a_card()]
    #dealer's cards, initially
    dealer=[deal_a_card(),deal_a_card()]
    
    while True:
        try:# Try block to prevent invalid inputs
            print("Enter a minimum bet of 1000")
            bet=float(input("Enter the bet amount: "))
            if bet<1000:
                print("Sorry, minimum bet must be 1000")
                continue
            if balance-bet>0 :
                break
            print("Sorry, you do not have enough money to place this bet.\n Place a smaller bet.")
        except ValueError:
            print("Invalid input")
            
    
    # Player's loop
    p_total=check_total(player)
    while True:
        #if player has 21
        if p_total==21:
            cards(player,dealer,1) # Displays cards of both 
            print("You Win!")
            balance+=bet
            break
        if p_total>21:
            cards(player,dealer)# Displays cards of player
            print("You are BUSTED!")
            balance-=bet
            break
        ch=hit_or_stand(player,dealer) #either gives the player a card or exits loop
        if ch:
            player.append(ch)
            p_total=check_total(player) 
        else:
            break
    print ('-'*75)
    
    #Dealer's loop
    while True:
        if p_total>=21:#player either won or is busted
            break
        d_total=check_total(dealer)
        if d_total>21:
            print("Dealer has busted!")
            cards(player,dealer,1)
            break
        if d_total<=p_total and d_total<19:#dealer has to hit until total is 18 or above
            card=deal_a_card()#card drawn
            print("The dealer hits.")
            print("The dealer gets",card)
            dealer.append(card)
            sleep(0.5)
            continue
        if d_total>p_total:#dealer wins
            print("Dealer wins")
            print("The dealer's total is",d_total)
            cards(player,dealer,1)
            balance-=bet #player loses bet
            break
        if d_total==p_total:
            print("Draw")#player loses no money
            break
        if d_total>18:
            print("You win!")
            balance+=bet #player wins bet amount
            break
    print ('-'*75)
    print("Your balance is",balance)
    return balance
#-----------------------------------------------------------------------------------------------
#-------------------------------- 3 slot machine -----------------------------------------------
# main function for 3 slot machine
def play_3slot(stake,table):
    print ('-'*75)
    #Multiline string
    print('''
             Welcome to the Slot Machine Simulator
             You'll be asked if you want to play. Each round costs as much as the table.
             Answer with yes/no.
             To win you must get one of the following combinations:
             BAR\tBAR\tBAR\t\tpays\t25000
             BELL\tBELL\tBELL/BAR\tpays\t2000
             PLUM\tPLUM\tPLUM/BAR\tpays\t1400
             ORANGE\tORANGE\tORANGE/BAR\tpays\t1000
             CHERRY\tCHERRY\tCHERRY\t\tpays\t700
             CHERRY\tCHERRY\t  -\t\tpays\t500
             CHERRY\t  -\t  -\t\tpays\t200
          ''')
    print ('-'*75)
    firstWheel=None #initializing the wheels of the machine
    secondWheel=None
    thirdWheel=None
    playQuestion=askPlayer(stake,table)# asks player if they want to play
    while(stake>table and playQuestion==True):
        firstWheel=spinWheel()#gets random values for each wheel
        secondWheel=spinWheel()
        thirdWheel=spinWheel()
        stake=printScore(stake,firstWheel,secondWheel,thirdWheel,table)
        playQuestion=askPlayer(stake,table)
    
    return stake
#-----------------------------------------------------------------------------------------------
def askPlayer(stake,table):
    
    '''
    Asks the player if he wants to play again.
    expecting from the user to answer with yes, y, no or n
    No case sensitivity in the answer.
    '''
    if stake<table:
        print("Sorry, you do not have enough money to play anymore ...")
        return False
    while True:     #To retake input if it is invalid
        answer=input("You have " + str(stake) + ". Would you like to play? ").lower()
        if(answer=="yes" or answer=="y"):
            return True
        elif(answer=="no" or answer=="n"):
            print("You ended the game with " + str(stake) + " in your hand.")
            print ('-'*75)
            return False
        else:
            print("wrong input!")
            
#-----------------------------------------------------------------------------------------------
def spinWheel():
    
    '''
    returns a random item from the wheel
    '''

    randomNumber=random.randint(0, 5)
    ITEMS=["CHERRY", "LEMON", "ORANGE", "PLUM", "BELL", "BAR"]
    return ITEMS[randomNumber]
#-----------------------------------------------------------------------------------------------
def printScore(stake,firstWheel,secondWheel,thirdWheel,table):

    '''
    prints the current score
    '''
    
    stake-=table
    if((firstWheel=="CHERRY") and (secondWheel != "CHERRY")):
        win=200
    elif((firstWheel=="CHERRY") and (secondWheel=="CHERRY") and (thirdWheel != "CHERRY")):
        win=500
    elif((firstWheel=="CHERRY") and (secondWheel=="CHERRY") and (thirdWheel=="CHERRY")):
        win=700
    elif((firstWheel=="ORANGE") and (secondWheel=="ORANGE") and ((thirdWheel=="ORANGE") or (thirdWheel=="BAR"))):
        win=1000
    elif((firstWheel=="PLUM") and (secondWheel=="PLUM") and ((thirdWheel=="PLUM") or (thirdWheel=="BAR"))):
        win=1400
    elif((firstWheel=="BELL") and (secondWheel=="BELL") and ((thirdWheel=="BELL") or (thirdWheel=="BAR"))):
        win=2000
    elif((firstWheel=="BAR") and (secondWheel=="BAR") and (thirdWheel=="BAR")):
        win=25000
    else:
        win=0
    stake+= win #adds winnings to balance
    if(win > 0):
        print(firstWheel + '\t' + secondWheel + '\t' + thirdWheel + ' -- You win ' + str(win))
    else:
        print(firstWheel + '\t' + secondWheel + '\t' + thirdWheel + ' -- You lose')
    return stake
#-----------------------------------------------------------------------------------------------
#--------------------------------- High/Lo -----------------------------------------------------
# Main method for high/lo
def play_hilo(stake):
    print ('-'*75)
    print('''
            Welcome to the High/Lo Simulator
            You'll be asked if you want to play. Each round costs 250.
            Answer with yes/no.
            To win you must guess the computer's number correctly.
         ''')
    playQuestion=askPlayer_hilo(stake)
    while(stake>250 and playQuestion==True):
        stake-=250
        result=hilo()
        if result==True:
            stake+=500
        playQuestion=askPlayer_hilo(stake)
    print ('-'*75)
    return stake
#-----------------------------------------------------------------------------------------------
def askPlayer_hilo(stake):
        
    '''
        Asks the player if he wants to play again.
        expecting from the user to answer with yes, y, no or n
    '''
    if stake<5:
        print("Sorry, you do not have enough money to play anymore ...")
        return False
    while True:     #To retake input if it is invalid
        answer=input("You have " + str(stake) + ". Would you like to play? ").lower()
        if 'y' in answer:
            return True
        elif(answer=="no" or answer=="n"):
            print("You ended the game with " + str(stake) + " in your hand.")
            print ('-'*75)
            return False
        else:
            print("wrong input!")
#-----------------------------------------------------------------------------------------------
def hilo():

    '''
        Function to let the player guess the number.
        Expects an input in the range of 1 to 1024
    '''
    
    no=random.randint(1,1024)
    li=[]# list of guesses
    print("You have to guess my number.\n My number lies between 1 and 1024\n You have 10 guesses.")
    i=0# no. of guesses made
    while i<10:
        i+=1#i incremented
        try:# makes sure that input is valid
            guess=int(input("Enter your guess: "))
        except ValueError:
            print("Invalid choice!")
            i-=1#removes guess
            continue
        if guess in li:#removes guess
            print("You have already guessed this!")
            i-=1
            continue
        if guess not in range(1,1024):#removes guess
            print("Invalid guess!")
            i-=1
            continue
        li.append(guess)# adds guess to list of guesses
        if guess<no:
            print("Your guess is too low. You have",10-i,"guesses.")
        elif guess>no:
            print("Your guess is too high. You have",10-i,"guesses.")
        else:
            print("You Win!")
            return True
    print("My number was",no)
    return False
#-----------------------------------------------------------------------------------------------

# Creates the folder player_data if it does not exist.
newpath = r'player_data'
# Creates the player data file if it does not exist.
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Path for rest of players
path1='player_data\\' # Two '', because escape sequence

#------------------------------ class to create a player -------------------------------------
class Player(object):
    # Constructor 
    def __init__(self):
        self.username=''
        self.password=''
        self.balance=0.0
        self.played={ 'BlackJack:': 0,
                      '3_Slot_Machine:': 0,
                      'High_Low:': 0
                    }
        self.won={    'BlackJack:' : 0,
                      '3_Slot_Machine:': 0,
                      'High_Low:': 0
                 }
        self.earned={ 'BlackJack:': 0,
                      '3_Slot_Machine:': 0,
                      'High_Low:': 0
                    }
    # Function to create a new account
    def create_user(self):
        global path1
        print ('-'*75)
        username=input("Enter your username: ").lower()
        while len(username)<6:
            print("Sorry, username must be atleast 6 characters long!")
            username=input("Enter your username: ").lower()
        try:
            file=open(path1+username+'.dat','r+b')
            print("Username taken!")
            self.create_user() #calls create_user again, since username is taken
        except:
            # Username does not exist
            pass #continues
            
        password=input("Enter your password: ").lower()
        while len(password)<8:
            print("Sorry, your password is not long enough!\nYour password must be atleast 8 characters long")
            password=input("Enter your password: ").lower()
        self.username=username
        self.password=password
        print("Your one time membership fee is 2000 credits.")
        balance=0
        while balance<7000:
            print("You must deposit atleast 5000")
            try:
                balance=float(input("Enter the amount you want to deposit inclusive of membership fees: "))
            except ValueError:
                print("Enter numeric values only!")
        self.balance=balance-2000
        print ('-'*75)
    # Function to display player statistics 
    def stats(self):
        print ('-'*75)
        print("Player username: ",self.username)
        print("Player balance: ",self.balance)
        print("Games played:")
        for i in self.played.keys():
            print(i,self.played[i])
        print("Games won: ")
        for i in self.won.keys():
            print(i,self.won[i])
        print("Credits earned: ")
        for i in self.earned.keys():
            print(i,self.earned[i])
        print ('-'*75)    
    # Function to add/withdraw money
    def deposit(self):
        print ('-'*75)
        while True:
            try:
                ch=int(input("Enter\n1. Deposit \n2. Withdraw \n3. Exit\nEnter your choice: "))
                if ch==1:
                    amt=float(input("Enter the amount you want to deposit: "))
                    self.balance+=amt
                    break
                elif ch==2:
                    print("Minimum account balance must be 5000")
                    amt=float(input("Enter the amount you want to withdraw: "))
                    if self.balance-amt<5000:
                        print("Sorry, you cannot withdraw that much")
                        continue
                    self.balance-=amt
                    break
                elif ch==3:
                    break
                else:
                    print("Invalid input!")
            except ValueError:
                print("Please enter a number only!")
                continue
#-----------------------------------------------------------------------------------------------                   
# Function to login 
def login():
    global path1,obj
    print ('-'*75)
    username=input("Enter your username: ").lower()
    k=logging_in(username)# function call
    return k
#-----------------------------------------------------------------------------------------------
# Prompts user to create an account
def prompt_create_account():
    ch=None #variable to store user choice
    k=None #variable to store username
    print("Enter \n1 to create an account\n2 to try logging in again\n3 to exit")
    ch=input("Enter your choice: ")
    if ch=='1':
        print("Creating a new account")
        k=create_user()#calls create_user
        return k
    elif ch=='2':
        c=0# trys logging in 
        while c<5:
            c+=1
            k=login()
            if not k:
                break
    elif ch=='3':#exits
        return None
    if k:#returns username
        return k
    print("Invalid choice!")
    prompt_create_account()
#-----------------------------------------------------------------------------------------------
# function to try to log in by opening data file storing details
def logging_in(username=None):
    try:# Try to open datafile
        file1=open(path1+username+'.dat','r+b')
        obj=pickle.load(file1)
        password=input("Enter your password: ").lower()
        c=0
        while obj.password!=password and c<5:
            print("Incorrect password! Try again")
            password=input("Enter your password: ").lower()
            c+=1
        file1.close()
        if c==5:
            print("Sorry, you have entered the password incorrectly too many times")
            print("Please try again later")
            return False
        print("Login successful!")
        return obj.username
    except:
        print("Sorry, username does not exist")
        k=prompt_create_account()#asks to create an accoung
        return k #returns username or none
#-----------------------------------------------------------------------------------------------
# Loading screen
def loading():
    print("Loading",end='')
    for i in range(5):
        sleep(0.25)
        print('.',end='')
    print()
#-----------------------------------------------------------------------------------------------
# Function to add new account to data file
def create_user():
    global path1
    obj=Player()
    obj.create_user()
    file=open(path1+obj.username+'.dat','a+b')
    pickle.dump(obj,file)
    file.close()
    # Adds new user to file containing user names
    print("Account created. Redirecting you to login screen.")
    loading()
    k=login()#stores username or None
    if k:
        return obj.username
#-----------------------------------------------------------------------------------------------
# Function to display game dev credits
def credits():
    print('''
    ___                                     __              
   /   |     ____ _____ _____ ___  ___     / /_  __  __   _ 
  / /| |    / __ `/ __ `/ __ `__ \/ _ \   / __ \/ / / /  (_)
 / ___ |   / /_/ / /_/ / / / / / /  __/  / /_/ / /_/ /  _   
/_/  |_|   \__, /\__,_/_/ /_/ /_/\___/  /_.___/\__, /  (_)  
          /____/                              /____/       
''')
    print('''
    _   __      _           _      __  
   / | / /___ _(_)___ ___  (_)____/ /_ 
  /  |/ / __ `/ / __ `__ \/ / ___/ __ \
 / /|  / /_/ / / / / / / / (__  ) / / /
/_/ |_/\__,_/_/_/ /_/ /_/_/____/_/ /_/ 
                                       
''')    
#-----------------------------------------------------------------------------------------------
# Function to play each game
def play(username):
    file=open(path1+username+'.dat','r+b')# try not used, because account exists
    obj=pickle.load(file)
    file.close()
    print('-'*75)
    print('''
Welcome to the Lotus Casino!
We have 3 games for our esteemed customers:
        1. BlackJack
        2. High_Low
        3. 3_Slot_Machine
You can play any of the games as long as your balance permits you to do so.
         ''')
    while True:
        ch=0
        try: #try block to take input
            print('-'*75)
            ch=int(input('''
Enter:
        '1' for BlackJack
        '2' for High_Low
        '3' for 3_Slot_Machine
        '4' to exit
Enter your choice: '''))
        except ValueError:
            print("Invalid input! Please enter a number only!")
            continue
        loading()#loading screen
        old_balance=obj.balance
        while ch==1: # While loop due to try block inside it.
            #play blackjack
            obj.played['BlackJack:']+=1
            print('We have 3 tables available, with an entry fee of :\n1. Green table :  500\n2. Blue table  : 1000\n3. Red table   : 1500')
            try:#try block for invalid inputs
                ch1=int(input("Enter your choice: "))
                while ch1 not in [1,2,3]:#invalid choice
                    print("Invalid choice! Please enter a number between 1 and 3")
                    ch1=int(input("Enter your choice: "))
                loading()
            except ValueError:
                print("Invalid input!")
                continue
            obj.balance-=ch1*500
            new_balance=blackjack(obj.balance)
            if new_balance>obj.balance :
                obj.won['BlackJack:']+=1
                obj.earned['BlackJack:']+=(new_balance-obj.balance)
            obj.balance=new_balance
            break
        if ch==2:# play high/low
            obj.played['High_Low:']+=1
            new_balance=play_hilo(obj.balance)
            if new_balance>obj.balance :
                obj.won['High_Low:']+=1
                obj.earned['High_Low:']+=(new_balance-obj.balance)
            obj.balance=new_balance
        while ch==3:# While loop due to try block inside it
            #play 3 slot machine
            obj.played['3_Slot_Machine:']+=1
            print('We have 3 tables available, with an entry fee of :\n1. Green table :  500\n2. Blue table  : 1000\n3. Red table   : 1500')
            try:#try block for invalid inputs
                ch1=int(input("Enter your choice: "))
                while ch1 not in [1,2,3]:#invalid choice
                    print("Invalid choice! Please enter a number between 1 and 3")
                    ch1=int(input("Enter your choice: "))
                loading()
            except ValueError:
                print("Invalid input! Enter numbers only!")
                continue
            new_balance=play_3slot(obj.balance,ch1*500)
            if new_balance>obj.balance :
                obj.won['3_Slot_Machine:']+=1
                obj.earned['3_Slot_Machine:']+=(new_balance-obj.balance)
            obj.balance=new_balance
            break
        if ch==4:# exit
            break
        if ch not in [1,2,3,4]:#invalid choice
            print("Invalid choice! Try again")
            continue
        if old_balance>obj.balance:
            print("Too bad, you lost",old_balance-obj.balance)
            print("Play more to win that amount back!")
        elif old_balance<obj.balance:
            print("Congratulations! You won",obj.balance-old_balance)
            print("Play more to win more money!")
        else:
            print("You neither won nor lost any money.")
            print("Play more to win more money!")
    #Saves game data after each play
    file=open(path1+username+'.dat','w+b')#rewrite onto file
    pickle.dump(obj,file)
    file.close()
#-----------------------------------------------------------------------------------------------
        
# Main body
print('''
  _           _                _____          _             
 | |         | |              / ____|        (_)            
 | |     ___ | |_ _   _ ___  | |     __ _ ___ _ _ __   ___  
 | |    / _ \| __| | | / __| | |    / _` / __| | '_ \ / _ \ 
 | |___| (_) | |_| |_| \__ \ | |___| (_| \__ \ | | | | (_) |
 |______\___/ \__|\__,_|___/  \_____\__,_|___/_|_| |_|\___/ 
''')


# Loop to log in or sign up
obj=Player()
username=''
while True:
    try:
        ch=int(input("Enter 1 to log in, 2 to sign up, or 3 to exit: "))
    except ValueError:# While loop due to try block
        print("Sorry, please enter a number")
        continue #New iteration starts
    if ch==1:
        print("Logging in")
        username=login()
        break
    elif ch==2:
        print("Creating an account")
        username=create_user()
        break
    elif ch==3:
        break
    else:
        print("Invalid input. Try again.")
        continue
# Loop to choose between playing, depositing, viewing stats and quitting
while True:
    if not username:
        break
    print ('-'*75)
    try:
        print("Enter:\n1. To play \n2. To view your game statistics \n3. To deposit/withdraw credits \n4. Exit \n5. Game Development Credits")
        ch=int(input("Enter your choice: "))
    except ValueError:
        print("Sorry, please enter a number")
        continue
    if ch==1:# play
        play(username)
    try: #checks if account exists, else quits game
        fh=open(path1+username+'.dat','r+b')
        obj=pickle.load(fh)
        fh.close()
    except:
        break
    if ch==2:# view stats
        obj.stats()
    elif ch==3:# deposit credits
        obj.deposit()
    elif ch==4:# Updates the player's game data when exiting
        fh=open(path1+username+'.dat','w+b')#rewrite onto file
        pickle.dump(obj,fh)
        fh.close()
        break
    elif ch==5:# displays game dev credits
        credits()
    else:
        print("Invalid choice!")
    
print("Thank you for visiting Lotus Casino! See you soon!")
sleep(5)
