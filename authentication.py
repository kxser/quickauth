import os, random, bcrypt, json, datetime, time


#If you are thinking of using this in an actual project, do not
#leave it unencrypted, unhashed or leave the file unobfuscated
#Use the function start_auth to start authentication in other files.



###################
#######Setup#######
###################
config = {
    "verbose": "false", #Wheter to print debug logs or not (not recommended)
    "language": "en", #only english is available
}

class ByteEncoder(json.JSONEncoder):
    def default(self, x):
        return x.decode('utf-8') if isinstance(x, bytes) else super().default(x)


def verboseprint(text): #An easy way to debug code without having to 
                        # remove print statements afterwards.
    if config.get('verbose') == 'true':
        print(f"Debug: {text}")
###################
#######END#########
###################


def check_credentials():
    username_input = input("Username: ")
    credentials_files = os.listdir("userCredentials")
    verboseprint(credentials_files)
    for elem in credentials_files:
        f = open(f'userCredentials/{elem}',)
        data = json.load(f)
        data = json.loads(data)
        f.close()
        if data.get('user') == username_input:
            password_input = input("Password: ").encode('utf-8')

            if bcrypt.checkpw(password_input, data.get('pw').encode('utf-8')):
                print("Successfully logged in.")
                global signed_in_user
                signed_in_user = {"username": f"{username_input}", "time": f"{datetime.datetime.now()}", "status": "signed_in"}
                verboseprint(signed_in_user)
                return signed_in_user
                #######This is the section that runs in the case of
                ####### a successful login.

        





def set_credentials(): # Function where the user can create an account
    global credentials_list
    random_user_id = random.randint(0, 999) #Gives you a username based on a random number
    login = True                            # and your username on your pc
    if login == True:
        current_user = f"{os.getlogin()}-{random_user_id}"
        print(f"""
        Your assigned username is: {current_user}
        Save it somewhere.
        """)


        def register_prompt(): #Section where we prompt the user
                               # for a password and save the info
                               # to a json file. (hashed)
            password = input("Enter new password: ")

            if len(password) > 6:
                password = password.encode("utf-8")
                current_credentials = {
                    "user": current_user,
                    "pw": bcrypt.hashpw(password, bcrypt.gensalt())

                }


                #section where we sort existing credentials' 
                #in alphabetic order, in order to decide what to
                #name the new users file
                saved_users = [] 
                credentials_db = os.listdir("userCredentials")
                verboseprint(credentials_db)
                for elem in credentials_db:
                    for i in range(len(credentials_db) + 1):                 
                        if str(i) in elem:
                            saved_users.append(str(i))
                            saved_users = sorted (saved_users, key = lambda x: (len (x), x))
                            verboseprint(saved_users)
                

                if saved_users != []: #Checks if there are any previous users saved
                    db_number = [int(i) for i in str(saved_users[-1]).split() if i.isdigit()]
                    db_number = int(r"{}".format(db_number).replace("[", "").replace("]", "")) + 1
                else:
                    db_number = 1

                db_file_name = f"credential_{db_number}.json" #Sets database name

                
                with open(f"userCredentials/{db_file_name}", "w+") as f: #Writes current info to database
                    json_object = json.dumps(current_credentials, indent=4, cls=ByteEncoder)
                    json.dump(json_object, f)
            else:
                print("Your password must be greater than 6 characters.")
                register_prompt()

        register_prompt() #Calls the main password function

def main():
    global start_auth
    def start_auth():
        print("""
        -------------------------
             Authentication     
        -------------------------
        made by      Kaiser    @
        github.com/kaiserwastaken
        -------------------------
        "L" : login
        "R" : Register
        "Control + C" : Cancel
        -------------------------
        """)
        time.sleep(1)
        cont = True
        while cont:
            user_action = input(": ")
            if user_action.lower() == "l":
                check_credentials()
            elif user_action.lower() == "r":
                set_credentials()
            user_action = input("Start another action? (y/n): ")
            if user_action.lower() == "n":
                cont = False
                quit()
    start_auth()

if __name__ == '__main__':
    main()
    


    

