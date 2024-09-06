
import mysql.connector as db
import re
import random 
import datetime

class hospital:
    def __init__(self):
        # admin data 
        self.__AdminId = 'admin'
        self.__AdminPass = 'admin'

        # create database

        mydb = db.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        cur = mydb.cursor()
        query = '''create database if not exists dbuser;'''
        cur.execute(query)
        mydb.close()

        # create table for doctor
        mydb = db.connect(host = 'localhost' , user = 'root' , passwd = 'root' , database = 'dbuser')
        # print("Connected to the server")
        cur = mydb.cursor()
        query = '''create table if not exists doctor_info(id int primary key auto_increment,
        name varchar(100) not null,
        gender varchar(20) not null,
        email varchar(100) unique not null,
        contact bigint unique not null,
        specialization varchar(100) not null,
        Time TIME not null,
        shift varchar(50) not null,
        Fees bigint not null,
        password varchar(150));'''

        cur.execute(query)
        mydb.close()


        # create table for patient
        mydb = db.connect(host = 'localhost' , user = 'root' , passwd = 'root' , database = 'dbuser')
        # print("Connected to the server")
        cur = mydb.cursor()
        query = '''create table if not exists patient_info(id int primary key auto_increment,
        name varchar(100) not null,
        dob date not null,
        gender varchar(20) not null,
        bg varchar(10) not null,
        email varchar(100) unique not null,
        contact bigint unique not null,
        password varchar(150));'''

        cur.execute(query)
        mydb.close()


        # Creating appointments table
        mydb = db.connect(host = 'localhost' , user = 'root' , passwd = 'root' , database = 'dbuser')
        # print("Connected to the server")
        cur = mydb.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS appointments (
            token varchar(255) NOT NULL,
            patient_email VARCHAR(255) NOT NULL,
            doctor_email VARCHAR(255) NOT NULL,
            specialization VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            FOREIGN KEY (patient_email) REFERENCES patient_info(email),
            FOREIGN KEY (doctor_email) REFERENCES doctor_info(email)
        );"""

        cur.execute(query)
        mydb.close()


        # History Table for patient
        mydb = db.connect(host = 'localhost' , user = 'root' , passwd = 'root' , database = 'dbuser')
        # print("Connected to the server")
        cur = mydb.cursor()
        query = '''create table if not exists History_info(id int primary key auto_increment, 
        patient_email varchar(100),
        history text,
        date_time datetime);'''
        cur.execute(query)
        mydb.close()


    # admin login section
    def AdminLogin(self , adminid , adminpass):
        if self.__AdminId == adminid:
            if self.__AdminPass == adminpass:
                return True
            else:
                return " INVALID ADMIN PASSWORD ... "

        else:
            return 'INVALID ADMIN ID ...'

    #database connection
    def connection(self):
        self.mydb = db.connect(host = 'localhost' , user = 'root' , passwd = 'root' , database = 'dbuser')
        self.cur = self.mydb.cursor()


    
    #Register table for doctor
    def RegisterUser_d(self, name ,gender, email , contact , specialization , Time , shift , Fees):

        self.connection()
        try:
            data = (name ,gender, email ,  contact ,specialization , Time , shift , Fees)
            query = '''insert into doctor_info(name, gender,  email, contact , specialization , Time , shift , Fees , password) values (%s,%s, %s , %s ,%s , %s, %s, %s, null);'''

            self.cur.execute(query , data )

            self.cur.execute("commit;")
            self.mydb.close()
        except:
            self.mydb.close()
            return "EMAIL OR CONTACT ALREADY EXISTS ..."

        else:        
            return True
    

    #Register table for patient
    def RegisterUser(self, name , dob ,gender , bg , email , contact ):

        self.connection()
        try:
            data = (name , dob ,gender,bg, email ,  contact)
            query = '''insert into patient_info(name, dob,gender,bg, email, contact , password) values (%s, %s ,%s, %s , %s, %s , null);'''

            self.cur.execute(query , data )

            self.cur.execute("commit;")
            self.mydb.close()
        except:
            self.mydb.close()
            return "EMAIL OR CONTACT ALREADY EXISTS ..."

        else:        
            return True
        

        
    # Reading all or filtered doctors
    def read_doctors(self , specialization=None):

        # Getting all or filtered doctors from database
        self.connection()
        if specialization:
            self.cur.execute("SELECT name, gender,  email, contact , specialization , Time , shift , Fees FROM doctor_info WHERE specialization = %s", (specialization,))
        else:
            self.cur.execute("SELECT name, gender,  email, contact , specialization , Time , shift , Fees FROM doctor_info")

        # Fetching all or filtered doctors from database
        results = self.cur.fetchall()

        if results:
            # Printing all or filtered doctors
            print("NAME \tGENDER \tEMAIL \tCONTACT \tSPECIALIZATION \tTIME  \tSHIFT  \tFEES")
            print("")
            for result in results:
                print(result[0] + "\t" + result[1] + "\t" + result[2] + "\t" + str(result[3]) + "\t" + result[4] + "\t" + str(result[5]) + "\t" + result[6] + "\t" + str(result[7]))
            return True
        else:
            print("""................................................................................
                                    NO DOCTOR FOUND WITH THAT SPECILIZATION   
                    ................................................................................
                """)
            
        return False


    # generate password for doctor

    def generatepassword_d(self,pass1,email):
        self.connection()
        data=(email,)
        query='''select password from doctor_info where email=%s;'''
        
        self.cur.execute(query,data)
        d=self.cur.fetchone()
        # print(d)

        self.mydb.close()
        
        if d[0]==None:
            self.connection()
            try:
                
                data=(pass1,email)
                query='''update doctor_info set password=%s where email=%s;'''
                self.cur.execute(query,data)
                self.cur.execute("commit;")
                self.mydb.close()
            except:
                self.mydb.close()
                return "PASSWORD FAILED TO GENERATE"
            else:
                return True

        else:
            return "PASSWORD ALREADY GENERATED"
        
    # generate password for patient

    def generatepassword(self,pass1,email):
        self.connection()
        data=(email,)
        query='''select password from patient_info where email=%s;'''
        
        self.cur.execute(query,data)
        d=self.cur.fetchone()
        # print(d)

        self.mydb.close()
        
        if d[0]==None:
            self.connection()
            try:
                
                data=(pass1,email)
                query='''update patient_info set password=%s where email=%s;'''
                self.cur.execute(query,data)
                self.cur.execute("commit;")
                self.mydb.close()
            except:
                self.mydb.close()
                return "PASSWORD FAILED TO GENERATE"
            else:
                return True

        else:
            return "PASSWORD ALREADY GENERATED"
        

    
    # delete account for doctor

    def DeleteAccount_d(self ,email,pass1):
        self.connection()
        data = (email,pass1)
        query = '''select email from doctor_info where email = %s && password = %s;'''
        self.cur.execute(query , data)
        d = self.cur.fetchone()
        print(d)
        self.mydb.close()

        if d == None:
            return "ACCOUNT DOES NOT EXISTS"

        elif d[0] == None:
            return "ACCOUNT DOES NOT EXISTS"

        else :
            self.connection()
            data = (email ,pass1)
            query = '''delete from doctor_info where email = %s && password = %s;'''
            self.cur.execute(query , data)
            self.cur.execute("commit;")
            self.mydb.close()
            return True
    
    # delete account for patient

    def DeleteAccount(self ,email,pass1):
        self.connection()
        data = (email,pass1)
        query = '''select email from patient_info where email = %s && password = %s;'''
        self.cur.execute(query , data)
        d = self.cur.fetchone()
        print(d)
        self.mydb.close()

        if d == None:
            return "ACCOUNT DOES NOT EXISTS"

        elif d[0] == None:
            return "ACCOUNT DOES NOT EXISTS"

        else :
            self.connection()
            data = (email ,pass1)
            query = '''delete from patient_info where email = %s && password = %s;'''
            self.cur.execute(query , data)
            self.cur.execute("commit;")
            self.mydb.close()
            return True
        

    #update info for doctor

    def UpdateInfo_d(self , query , new_data , email):
        self.connection()
        try :
            data = (new_data , email)
            self.cur.execute(query , data)
            self.cur.execute("commit;")
            self.mydb.close()

        except :
            return "SOMETHING WENT WRONG "
        
        else :
            return True
    
    #update info for patient

    def UpdateInfo(self , query , new_data , email):
        self.connection()
        try :
            data = (new_data , email)
            self.cur.execute(query , data)
            self.cur.execute("commit;")
            self.mydb.close()

        except :
            return "SOMETHING WENT WRONG "
        
        else :
            return True

    #userlogin for doctor

    def UserLogin_d(self , email , pass1):
        self.connection()
        data = (email , pass1)
        query = '''select email,password from doctor_info where email = %s && password = %s;'''
        self.cur.execute(query , data)
        value = self.cur.fetchone()
        # print(value)
        self.mydb.close()
        try :
            if value[0] == email:
                if value[1] == pass1 :
                    return True
        
        except :
            return "INVALID EMAIL-ID OR PASSWORD"


    #userlogin for patient

    def UserLogin(self , email , pass1):
        self.connection()
        data = (email , pass1)
        query = '''select email,password from patient_info where email = %s && password = %s;'''
        self.cur.execute(query , data)
        value = self.cur.fetchone()
        # print(value)
        self.mydb.close()
        try :
            if value[0] == email:
                if value[1] == pass1 :
                    return True
        
        except :
            return "INVALID EMAIL-ID OR PASSWORD"
        
        
    # Booking an appointment with a specialized doctor
    def book_appointment(self ,email, specialization):

        # Getting all doctors with that specialization from database

        self.connection()
        self.cur.execute("SELECT name, email FROM doctor_info WHERE specialization = %s", (specialization,))
        results = self.cur.fetchall()
        if results:

            # Choosing a random doctor from the results

            doctor = random.choice(results)
            doctor_name = doctor[0]
            doctor_email = doctor[1]

            # Generating a token number 
            now = datetime.datetime.now()
            # token = int(now.strftime("%Y%m%d%H%M%S"))
            token = str(random.randint(1000 , 9999))

            # Inserting appointment details into database
            self.cur.execute("INSERT INTO appointments VALUES (%s, %s, %s, %s, %s, %s)", (token, email, doctor_email, specialization, now.date(), now.time()))
            self.cur.execute("commit;")

            print("""
                =============================================================================
                                      APPOINTMENT BOOKED SUCCESSFULLY
                =============================================================================
            
            """)

            print()
        
            print("|| YOUR TOKEN NUMBER IS     || :-", token)
            print("|| YOUR DOCTOR'S NAME IS    || :-", doctor_name)
            print("|| YOUR DOCTOR'S EMAIL IS   || :-", doctor_email)
            print("|| YOUR APPOINTMENT DATE IS || :-", now.date())
            print("|| YOUR APPOINTMENT TIME IS || :-", now.time())
        else:
            print("""
                    ____________________________________________________________________________________
                        NO DOCTORS FOUND WITH THAT SPECIALIZATION. PLEASE TRY ANOTHER ONE.  
                    ____________________________________________________________________________________
                                    
                                    """)
            

    # Viewing all or upcoming appointments for a patient or a doctor
    def view_appointments(self,email, mode):

        # Getting all or filtered appointments from database based on email address or date range
        self.connection()

        if mode == "history":
            self.cur.execute("SELECT * FROM appointments WHERE patient_email = %s OR doctor_email = %s ORDER BY date DESC, time DESC", (email, email))

        elif mode == "upcoming":
            today = datetime.date.today()
            self.cur.execute("SELECT * FROM appointments WHERE (patient_email = %s OR doctor_email = %s) AND date >= %s ORDER BY date ASC, time ASC", (email, email, today))

        else:
            print("Invalid mode. Please try again.")
            return False
        
        # Fetching all or filtered appointments from database
        results = self.cur.fetchall()
        if results:
            print("--------------------------------------------------------------------")
            print("TOKEN \tPATIENT \tDOCTOR \tSPECIALIZATION \tDATE \tTIME")
            print("--------------------------------------------------------------------")
            print("")
            for result in results:

                # Getting patient's and doctor's names from database
                self.cur.execute("SELECT name FROM patient_info WHERE email = %s", (result[1],))
                patient_name = self.cur.fetchone()[0]
                self.cur.execute("SELECT name FROM doctor_info WHERE email = %s", (result[2],))
                doctor_name = self.cur.fetchone()[0]

                # Printing appointment details
                print(str(result[0]) + "\t" + patient_name + "\t" + doctor_name + "\t" + result[3] + "\t" + str(result[4]) + "\t" + str(result[5]))
                print("--------------------------------------------------------------------")
            return True
        else:
            print("""
                    ____________________________________________________________________________________
                                   N O      A P P O I N T M E N T     F O U N D 
                    ____________________________________________________________________________________
                                    
                                    """)
            
            
        
            return False

    # Sending reminders for upcoming appointments for both patients and doctors

    def send_reminders(self):

        # Getting all upcoming appointments from database

        self.connection()
        today = datetime.date.today()
        self.cur.execute("SELECT * FROM appointments WHERE date >= %s ORDER BY date ASC, time ASC", (today,))
        results = self.cur.fetchall()
        if results:

            # Comparing current time with appointment time
            now = datetime.datetime.now()
            for result in results:

                # Getting appointment details
                token = result[0]
                patient_email = result[1]
                doctor_email = result[2]
                specialization = result[3]
                date = result[4]
                time = result[5]

                # Calculating time difference in hours
                appointment_time = datetime.datetime.combine(date, time)
                time_diff = (appointment_time - now).total_seconds() / 3600

                # Sending reminder message if appointment is within 24 hours
                if 0 < time_diff < 24:

                    # Getting patient's and doctor's names from database
                    self.cur.execute("SELECT name FROM patient_info WHERE email = %s", (patient_email,))
                    patient_name = self.cur.fetchone()[0]
                    self.cur.execute("SELECT name FROM doctor_info WHERE email = %s", (doctor_email,))
                    doctor_name = self.cur.fetchone()[0]

                    
                    print(f"REMINDER : YOU HAVE AN APPOINTMENT WITH {doctor_name} ({specialization}) AT {time} ON {date}. YOUR TOKEN NUMBER IS {token}.")
                    print("")
                    print(f"REMINDER : YOU HAVE AN APPOINTMENT WITH {patient_name} AT {time} ON {date}. YOUR TOKEN NUMBER IS {token}.")






# application start prom here 

app = hospital()


tht1='''
                   BEAUTIFUL THINGS HAPPEN WHEN YOU DISTANCE YOURSELF FROM 
                  ---------------------------------------------------------
                                       NEGATIVITY
                                      ------------
                    '''
tht2='''
                          DREAMS ARE NOT WHAT YOU SEE WHEN YOU SLEEP,
                          ------------------------------------------
                          DREAMS ARE THOSE WHICH DON'T LET YOU SLEEP 
                          ------------------------------------------
       '''
tht3='''
                     YOU ONLY LIVE ONCE. BUT IF YOU DO IT RIGHT,
                     ------------------------------------------
                                   ONCE IS ENOUGH
                                  ----------------
       '''
tht4=''' 
                      THE EXPERT IN ANYTHING WAS ONCE A BEGINNER
                     --------------------------------------------

'''
tht5='''
                      NOT ALL STORMS COME TO DISRUPT YOUR LIFE
                      ----------------------------------------
                           SOME COME TO CLEAR YOUR PATH
                           ----------------------------
        '''
tht6='''
                   LISTEN TO EVERYONE AND LEARN FROM EVERYONE, BEACAUSE NOBODY KNOWS EVERYTHING  
                  ------------------------------------------------------------------------------       
                                         BUT EVERYONE KNOWS SOMETHING
                                         ----------------------------
                  '''

tht7='''
                     ONE KIND WORD CAN CHANGE SOMEONE'S 
                     ----------------------------------
                               ENTIRE DAY
                               ----------
                               '''
tht8='''
                     GOOD MANNERS AND KINDNESS ARE ALWAYS 
                     ------------------------------------
                                 IN FASHION
                                 ----------
                                 '''
                                 
th=(tht1,tht2,tht3,tht4,tht5,tht6,tht7,tht8)
print("""  
  
               ___       ___   ___            ___     _____ ___       ___  _____ _____
     |      | |    |    |   | |   | |\    /| |          |  |   |     |   |   |     |   |   |
     |  /\  | |__  |    |     |   | | \  / | |__        |  |   |     |       |     |   |___|
     | /  \ | |    |    |     |   | |  \/  | |          |  |   |     |       |     |       |
     |/    \| |___ |___ |___| |___| |      | |___       |  |___|     |___| __|__   |    ___|
   _________________________________________________  __________    _________________________
                         
                            ___   ___   ___  _____  _____  ____    
                     |   | |   | |     |   |   |      |   |    |  |
                     |___| |   | |___  |___|   |      |   |____|  |
                     |   | |   |     | |       |      |   |    |  |
                     |   | |___|  ___| |     __|__    |   |    |  |____
                    ____________________________________________________                
          """)

d=datetime.date.today()
t=datetime.datetime.now()
print(" ")
print(" ")
print("        DATE:-",d.strftime("%A, %d %B %Y"))
print(" ")
print("        TIME:-",t.strftime("%H:%M:%S"))
print("")
print('')
choice=random.choice(th)
print(choice)



while True:
    print("""

    ********************************************************************************************************************
            S E L E C T             F R O M               G I V E N              O P T I O N
    ********************************************************************************************************************    
           _________________
          |                 |
          | 1 - ADMIN LOGIN | 
          |_________________|

           __________________________
          |                          |
          | 2 - USER LOGIN AS DOCTOR | 
          |__________________________|

           ___________________________
          |                           |
          | 3 - USER LOGIN AS PATIENT | 
          |___________________________|

           __________________________________
          |                                  |
          | 4 - GENERATE PASSWORD FOR DOCTOR | 
          |__________________________________|

           ______________________
          |                      |
          | 5 - EXIT APPLICATION | 
          |______________________|                                   
          

          """
          
          )
    
    print("******************************************************************************************************")
    ch = input("ENTER YOUR APPLICATION CHOICE :")
    print("******************************************************************************************************")

    if ch == '1':
        print(""" --------------------------------------------------------------
                        A D M I N    L O G I N    S E C T I O N 
                  --------------------------------------------------------------
             """)

        adminid = input(" ||  ENTER ADMIN ID  || :-")
        print("")
        adminpass = input(" ||  ENTER ADMIN PASSWORD  || :-")

        # cleaning data 
        adminid = adminid.strip()
        adminpass = adminpass.strip()

        x = app.AdminLogin(adminid , adminpass)
        if x != True:
            print(f"\n*********** {x} ************\n")
        else:
            print("""
                =============================================================================
                                    SUCCESSFULLY ADMIN LOGED IN
                =============================================================================
            
            """)
            while True:


                print(""" 
      
    
        
         _____________                     __________
        |             |                   |          |
        | 1. DOCTOR   |                   | 2. EXIT  |
        |_____________|                   |__________|
        
         
        
        """)
                e=input("||  SELECT || :-")

                if e == '1':
                    while True:

                        print("""
                        
                        _____________________________________
                       | 1 - CREATE ACCOUNT FOR DOCTOR       |
                       |_____________________________________| 
                              
                        _____________________________________
                       | 2 - READ DOCTOR RECORDS             |
                       |_____________________________________|

                        _____________________________________
                       | 3 - DELETE DOCTOR ACCOUNT           |
                       |_____________________________________| 
                       
                        _____________________________________
                       | 4 - UPDATE DOCTOR ACCOUNT           |
                       |_____________________________________| 
                       
                        _____________________________________
                       | 5 - EXIT                            |
                       |_____________________________________| 
                       
                        
                        """)
                        print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                        p_ch = input("|| SELECT OPTION || :-")
                        print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                        print("")

                        if p_ch == '1':
                            print("""------------------------------------------------------------------------------------
                                        C R E A T E      A C C O U N T      F O R       D O C T O R
                                     ------------------------------------------------------------------------------------    
                            """)

                            
                            while True:
                                name = input("||  ENTER DOCTOR NAME  || :-")
                                
                                name_ptr = r'[a-zA-Z]+$'
                                if re.match(name_ptr , name):
                                    print("")
                                    break
                                else:
                                    print("""
                                        ____________________________________________________________________________________
                                            P L E A S E           F I L L          N A M E            C O R R E C T L Y   
                                        ____________________________________________________________________________________
                                    
                                    """)

                            while True:
                                gender = input("||  ENTER YOUR GENDER  || :-")
                                
                                name_ptr = r'[a-zA-Z]+$'
                                if re.match(name_ptr , gender):
                                    print("")
                                    break
                                else:
                                    print("""
                                        ____________________________________________________________________________________
                                                    P L E A S E           F I L L          C O R R E C T L Y   
                                        ____________________________________________________________________________________
                                    
                                    """)

                            while True:

                                email = input("||  ENTER DOCTOR EMAIL-ID  || :-" )
                                email_ptr = r'[a-z0-9\_\.]+@+[a-z]+\.[a-z]+'
                                if re.match(email_ptr , email):
                                    print("")
                                    break
                                else:
                                    print("""
                                        ____________________________________________________________________________________
                                            P L E A S E         E N T E R       C O R R E C T        E M A I L   
                                        ____________________________________________________________________________________
                                    
                                    """) 
                            
                            
                            while True:
                                contact = input("||  ENTER DOCTOR CONTACT  || :-" )
                                contact_ptr = r'^[6-9]+[0-9]{9}$'
                                if re.match(contact_ptr , contact):
                                    print("")
                                    break
                                else:
                                    print("""
                                        ____________________________________________________________________________________
                                            I N C O R R E C T       C O N T A C T        N U M B E R  
                                        ____________________________________________________________________________________
                                    
                                    """)


                            while True:
                                specialization = input("||  ENTER YOUR SPECIALIZATION  || :-")
                                name_ptr = r'[a-zA-Z]+$'
                                if re.match(name_ptr , specialization):
                                    print("")
                                    break
                                else:
                                    print("""
                                        ____________________________________________________________________________________
                                            P L E A S E     F I L L    S P E C I A L I Z A T I O N     C O R R E C T L Y   
                                        ____________________________________________________________________________________
                                    
                                    """)
                                    
                            

                            while True:
                                Timing = input("||  ENTER YOUR TIMING (HH:MM:SS)  || :-")
                                name_ptr = r'\d{2}:\d{2}:\d{2}'
                                if re.match(name_ptr , Timing):
                                    print("")
                                    break
                                else:
                                    print("""
                                        ____________________________________________________________________________________
                                                    PLEASE    FILL    TIMING   AS    PER    THE     FORMAT   
                                        ____________________________________________________________________________________
                                    
                                    """)

                            while True:
                                shift = input("||  ENTER YOUR SHIFT  || :-")
                                name_ptr = r'[a-zA-Z]+$'
                                if re.match(name_ptr , shift):
                                    print("")
                                    break
                                else:
                                    print("""
                                        ____________________________________________________________________________________
                                            P L E A S E           F I L L          S H I F T            C O R R E C T L Y   
                                        ____________________________________________________________________________________
                                    
                                    """)

                            while True:
                                fees = input("|| ENTER YOUR VISITING CHARGES || : -")
                                print("")
                                break




                            x = app.RegisterUser_d(name ,gender, email , contact , specialization , Timing , shift , fees)
                            if x != True:
                                print(f"\n*************** {x} ***************\n")
                            else:
                                print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                 SUCCESSFULLY ACCOUNT CREATED PLEASE GENERATE PASSWORD
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                    
                                    """)
                        elif p_ch == '2':
                            
                            # Reading all or filtered doctors
                            specialization = input("||  ENTER SPECIALIZATION TO FILTER BY (LEAVE BLANK TO SHOW ALL)  || :- ")
                            print("")
                            a = app.read_doctors(specialization)  
                        

                        elif p_ch == '3':
                            print("""------------------------------------------------------------------------------------
                                        D E L E T E          D O C T O R            A C C O U N T
                                     ------------------------------------------------------------------------------------    
                            """)

                            email = input("||  ENTER DOCTOR EMAIL-ID WHICH YOU WANT TO DELETE  || :- ")
                            print("")
                            pass1 = input("||  ENTER YOUR PASSWORD  || :- ")
                            
                            print("""
                                ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                                ARE YOU SURE YOU WANT TO DELETE THIS ACCOUNT PRESS "Y" TO DELETE AND ANY KEY FOR THE EXIT :
                                ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

                                """)
                            
                            ch1 = input("(Y/N) :")
                            if ch1 == "Y" or ch1 == "y":
                                y = app.DeleteAccount_d(email,pass1)
                                if y != True:
                                    print(f"\n************ {y} ***************\n")
                                else :
                                    print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                          ACCOUNT      SUCCESSFULLY      CLOSED
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                    
                                    """)
                            else :
                                print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                         DELETE       PROCESS       CANCELLED
                                    < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <
                                    
                                    """)

                        
                        elif p_ch == '4':
                            print("""------------------------------------------------------------------------------------
                                        U P D A T E          D O C T O R            A C C O U N T
                                     ------------------------------------------------------------------------------------    
                            """)


                            print("""
                                 ___________________________________
                                |                                   |
                                |    1 - UPDATE NAME    
                                ....................................|
                                |    2 - UPDATE GENDER  
                                ....................................|
                                |    3 - UPDATE CONTACT   
                                ....................................|
                                |    4 - UPDATE SPECIALIZATION  
                                ....................................|
                                |    5 - UPDATE TIMING     
                                ....................................|
                                |    6 - UPDATE SHIFT 
                                ....................................|
                                |    7 - UPDATE VISITING CHARGES 
                                ....................................|
                                |    8 - EXIT UPDATE                |       
                                |___________________________________|
                                
                                    """)
                            
                            updateflag = False
                            while True :
                                print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                                ch2 = input("|| SELECT OPTION || :-")
                                print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")

                            
                                
                                if ch2 == "1":
                                    email = input("||   CONFIRMED EMAIL-ID   || :- ")
                                    print("")
                                    new_data = input("||   ENTER DOCTOR NAME   || :- ")
                                    query = '''update doctor_info set name = %s where email = %s;'''
                                    break

                                elif ch2 == "2":
                                    email = input("||   CONFIRMED EMAIL-ID   || :- ")
                                    print("")
                                    new_data = input("||   ENTER YOUR GENDER   || :- ")
                                    query = '''update doctor_info set gender = %s where email = %s;'''
                                    break

                                elif ch2 == "3":
                                    email = input("||   CONFIRMED EMAIL-ID   || :- ")
                                    print("")
                                    new_data = input("||   ENTER DOCTOR NEW CONTACT   || :- ")
                                    query = '''update doctor_info set contact = %s where email = %s;'''
                                    break

                                elif ch2 == "4":
                                    email = input("||   CONFIRMED EMAIL-ID   || :- ")
                                    print("")
                                    new_data = input("||   ENTER NEW SPECIALIZATION   || :- ")
                                    query = '''update doctor_info set specialization = %s where email = %s;'''
                                    break

                                elif ch2 == "5":
                                    email = input("||   CONFIRMED EMAIL-ID   || :- ")
                                    print("")
                                    new_data = input("||   ENTER NEW TIMING (HH:MM:SS)   || :- ")
                                    query = '''update doctor_info set Time = %s where email = %s;'''
                                    break

                                elif ch2 == "6":
                                    email = input("||   CONFIRMED EMAIL-ID   || :- ")
                                    print("")
                                    new_data = input("||   ENTER NEW SHIFT   || :- ")
                                    query = '''update doctor_info set shift = %s where email = %s;'''
                                    break

                                elif ch2 == "7":
                                    email = input("||   CONFIRMED EMAIL-ID   || :- ")
                                    print("")
                                    new_data = input("||   ENTER NEW VISITING CHARGES   || :- ")
                                    query = '''update doctor_info set fees = %s where email = %s;'''
                                    break

                                elif ch2 == "8":
                                    
                                    print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                         UPDATE       PROCESS       CANCELLED
                                    < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <
                                    
                                    """)
                                    updateflag = True
                                    break

                                else:
                                    print("""
                                    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                          I N V A L I D     C H O I C E
                                    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                    
                                    """)

                            if updateflag == True :
                                pass

                            else :
                                z = app.UpdateInfo_d(query , new_data , email)
                                if z != True :
                                    print(f"\n*************** {z} *****************\n")

                                else :
                                    print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                    SUCCESSFULLY   INFORMATION   UPDATED
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                    
                                    """)

                        elif p_ch == '5':
                            print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                      B A C K     T O      T H E       H O M E
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                    
                                    """)
                            break

                        else:
                            print("""
                                    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                          I N V A L I D     C H O I C E
                                    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                    
                                    """)

                        
                        
                elif e == "2":
                    print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                              SUCCESSFULLY   ADMIN LOGED OUT
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                    
                                    """)
                    break

                else:
                    print("""
                                    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                  I N V A L I D         A D M I N         C H O I C E
                                    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                    
                                    """)



    elif ch == '2':
        print("""-                     --------------------------------------------------------------
                                                   D O C T O R    L O G I N    S E C T I O N 
                                       --------------------------------------------------------------
                            """)
        email = input("||  ENTER YOUR EMAIL-ID  || :-")
        print("")
        pass1 = input("||  ENTER YOUR PASSWORD  || :-")

        x = app.UserLogin_d(email , pass1)

        if x != True:
            print(f"\n*************** {x} ******************\n")
        else :
            print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                              SUCCESSFULLY  USER  LOGED  IN
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                    
                                    """)
            
            while True :

                print("""
                                    WELCOME TO THE DOCTOR MENU PLEASE CHOOSE AN OPTION :-
                        ---------------------------------------------------------------------------------------
                    """)

                print("""
                            
                        _____________________________________
                        | 1 - VIEW YOUR APPOINTMENTS HISTORY  |
                        |_____________________________________| 
                                
                         _____________________________________
                        | 2 - VIEW YOUR UPCOMING APPOINTMENTS |
                        |_____________________________________|

                        _____________________________________
                        | 3 - EXIT THE PROGRAM                |
                        |_____________________________________| 
                        
                            
                            """)


                print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                choice = input("Enter your choice: ")
                print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                
                if choice == "1":

                    # Viewing appointments history
                    print("-----------------------------------------------------------------------------")
                    x =app.view_appointments(email, "history")

                elif choice == "2":
                    
                    t=datetime.datetime.now()
                    l=t.strftime("%p")
                    if l=="PM":
                        
                        print("|||   GOOD EVENING    |||")
                        
                    else:
                        print("|||   GOOD MORNING    |||")
                    print(" ")
                    print(""" YOU HAVE APPOINTMENT WITH FOLLOWING PATIENTS:-""")
                    print("")

                # Viewing upcoming appointments
                    print("--------------------------------------------------------------------------")
                    x = app.view_appointments(email, "upcoming")
    
                elif choice == "3":
                    email = None
                    pass1 = None
                    print("""
                                > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                            SUCCESSFULLY   USER  LOGED  OUT
                                > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                
                                """)
                    
                    break

                else :
                    print("""
                                * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                        I N V A L I D     C H O I C E
                                * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                
                            """)
    
    
    elif ch == '3':
        while True:

            print("""
            
            ______________________________________
            | 1 - CREATE NEW ACCOUNT FOR PATIENT  |
            |_____________________________________| 
                  
             ______________________________________
            | 2 - GENERATE PASSWORD FOR PATIENT   |
            |_____________________________________|

             _____________________________________
            | 3 - LOGIN PATIENT                   | 
            |_____________________________________|
                  
            ______________________________________      
            | 4 - DELETE PATIENT ACCOUNT          |
            |_____________________________________| 
            
            ______________________________________
            | 5 - UPDATE PATIENT ACCOUNT          |
            |_____________________________________| 
            
            ______________________________________
            | 6 - EXIT                            |
            |_____________________________________| 
            
            
            """)

            print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
            p_ch = input("|| SELECT OPTION || :-")
            print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")

            
            if p_ch == '1':
                print("")
                print("""==========================================================================================
                            C R E A T E      A C C O U N T      F O R       P A T I E N T
                        ===========================================================================================   
                """)
                
                while True:
                    name = input("||   ENTER PATIENT NAME   || :- ")
                    
                    name_ptr = r'[a-zA-Z]+$'
                    if re.match(name_ptr , name):
                        print("")
                        break
                    else:
                        print("""
                            ____________________________________________________________________________________
                                P L E A S E           F I L L          N A M E            C O R R E C T L Y   
                            ____________________________________________________________________________________
                        
                        """)


                while True:
                    dob = input('||   ENTER PATIENT DATE OF BIRTH (YYYY-MM-DD)   || :- ')
                    dob_ptr = r'\d{4}-\d{2}-\d{2}'
                    if re.match(dob_ptr , dob):
                        print("")
                        break
                    else:
                        print("""
                            ____________________________________________________________________________________
                                        PLEASE     FILL      DATE     AS     PER     THE     FORMAT 
                            ____________________________________________________________________________________
                        
                        """)

                while True:
                    gender = input("||   ENTER YOUR GENDER   || :- ")
                    name_ptr = r'[a-zA-Z]+$'
                    if re.match(name_ptr , gender):
                        print("")
                        break
                    else:
                        print("""
                            ____________________________________________________________________________________
                                        P L E A S E           F I L L          C O R R E C T L Y   
                            ____________________________________________________________________________________
                        
                        """)

                while True:
                    bg=input("||  ENTER YOUR BlOOD GROUP (A+,B+,O+,AB+,A-,B-,O-,AB-)  || :-")
                    if bg==("A+") or bg==("B+") or bg==("o+") or bg==("AB+") or bg==("A-") or bg==("B-") or bg==("O-") or bg==("AB-"):
                        print("")
                        break
                    else:
                        print("""
                            ____________________________________________________________________________________
                                            E N T E R            V A L I D             V A L U E   
                            ____________________________________________________________________________________
                        
                        """)
                

                while True:

                    email = input("||   ENTER PATIENT EMAIL-ID   || :- ")
                    email_ptr = r'[a-z0-9\_\.]+@+[a-z]+\.[a-z]+'
                    if re.match(email_ptr , email):
                        print("")
                        break
                    else:
                        print("""
                            ____________________________________________________________________________________
                                P L E A S E        E N T E R          E M A I L          C O R R E C T L Y   
                            ____________________________________________________________________________________
                        
                        """) 
                
                
                while True:
                    contact = input("||   ENTER PATIENT CONTACT   || :- ")
                    contact_ptr = r'^[6-9]+[0-9]{9}$'
                    if re.match(contact_ptr , contact):
                        print("")
                        break

                    else:
                        print("""
                            ____________________________________________________________________________________
                                I N V A L I D          C O N T A C T           N U M B E R   
                            ____________________________________________________________________________________
                        
                        """)



                x = app.RegisterUser(name , dob ,gender ,bg , email , contact )
                if x != True:
                    print(f"\n*************** {x} ***************\n")
                else:
                    print("""
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                        SUCCESSFULLY ACCOUNT CREATED PLEASE GENERATE PASSWORD
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                        
                        """)
                    
            elif p_ch == '2':
                print("""
                    ---------------------------------------------------------------------------------------------
                                                GENERATE PASSWORD FOR PATIENT
                    ---------------------------------------------------------------------------------------------
                
                """)
                email=input("||  ENTER YOUR EMAIL-ID  || : -")
                print("")
                pass1=input("||  ENTER YOUR PASSWORD  || : -")
                print("")
                pass2=input("||  CONFIRM YOUR PASSWORD  || : -")
                print("")
                if pass1!=pass2:
                    print("""
                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                    P A S S W O R D     D I D     N O T      M A T C H E D
                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    
                    """)

                else:
                    x=app.generatepassword(pass1,email)

                    if x!=True:
                        print(f"\n*********** {x}************\n")
                    else:
                        print("""
                                            > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                                        SUCCESSFULLY   PASSWORD GENERATED
                                            > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                            
                                            """)
                        

            elif p_ch == '3':
                    print("""   ____________________________________________________________________
                                            P A T I E N T    L O G I N    S E C T I O N 
                                _____________________________________________________________________
                        """)
                    email = input("||  ENTER YOUR EMAIL-ID  || :-")
                    print("")
                    pass1 = input("||  ENTER YOUR PASSWORD  || :-")

                    x = app.UserLogin(email , pass1)

                    if x != True:
                        print(f"\n*************** {x} ******************\n")
                    else :
                        print("""
                                                > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                                        SUCCESSFULLY   USER   LOGED   IN
                                                > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                
                                                """)
                        print("")

                        while True :

                            print("""
                                                    WELCOME TO THE PATIENT MENU PLEASE CHOOSE AN OPTION :-
                                    ---------------------------------------------------------------------------------------
                            """)

                            print("""
                                         ____________________________________________________
                                        | 1 - BOOK AN APPOINTMENT WITH A SPECIALIZED DOCTOR  |
                                        |____________________________________________________|
                                                    
                                         _____________________________________
                                        | 2 - VIEW YOUR APPOINTMENTS HISTORY  |
                                        |_____________________________________| 
                                                
                                         _____________________________________
                                        | 3 - VIEW YOUR UPCOMING APPOINTMENTS |
                                        |_____________________________________|
                        
                                         _____________________________________
                                        | 4 - EXIT THE PROGRAM                |
                                        |_____________________________________| 
                       
                        
                        """)
                            

                            print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                            U_ch = input("Enter Your Choice :")
                            print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                            print("")
                            if U_ch == "1":
                                specialization = input("Enter the specialization you need: ")
                                x = app.book_appointment(email, specialization)

                            elif U_ch == "2":
                                x = app.view_appointments(email, "history")

                            elif U_ch == "3":
                                x = app.view_appointments(email, "upcoming")

                            elif U_ch == "4":
                                email = None
                                pass1 = None
                                print("""
                                                > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                                        SUCCESSFULLY   USER LOGED OUT
                                                > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                
                                                """)
                                break

                            else :
                                print("""
                                                * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                                    I N V A L I D     C H O I C E
                                                * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                
                                                """)


            elif p_ch == '4':
                print("""------------------------------------------------------------------------------------
                            D E L E T E          P A T I E N T            A C C O U N T
                            ------------------------------------------------------------------------------------    
                """)

                email = input("||   ENTER PATIENT EMAIL WHICH YOU WANT TO DELETE   || :- ")
                print("")
                pass1 = input("||   ENTER YOUR PASSWORD   || :- ")

                print("""
                    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                    ARE YOU SURE YOU WANT TO DELETE THIS ACCOUNT PRESS "Y" TO DELETE AND ANY KEY FOR THE EXIT :
                    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

                    """)
                ch1 = input("(Y/N) :")
                if ch1 == "Y" or ch1 == "y":
                    y = app.DeleteAccount(email,pass1)
                    if y != True:
                        print(f"\n************ {y} ***************\n")
                    else :
                        print("""
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                ACCOUNT      SUCCESSFULLY      CLOSED
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                        
                        """)
                else :
                    print("""
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                DELETE       PROCESS       CANCELLED
                        < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <
                        
                        """)

            
            elif p_ch == '5':
                print("""------------------------------------------------------------------------------------
                            U P D A T E          P A T I E N T            A C C O U N T
                        ------------------------------------------------------------------------------------    
                    """)
            
        
                print("""
                    ___________________________________
                    |                                   |
                    |    1 - UPDATE NAME    
                    ....................................|
                    |    2 - UPDATE DOB   
                    ....................................|
                    |    3 - UPDATE GENDER   
                    ....................................|
                    |    4 - UPDATE BLOOD GROUP   
                    ....................................|
                    |    5 - UPDATE CONTACT  
                    ....................................|
                    |    6 - EXIT UPDATE                |       
                    |___________________________________|
                    
                        """)
                print("")
                updateflag = False
                while True :
                    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                    ch2 = input("|| SELECT OPTION || :-")
                    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")

                    print("")
                    
                    if ch2 == "1":
                        email = input("||   CONFIRMED EMAIL-ID   || :- ")
                        print("")
                        new_data = input("||   ENTER PATIENT NEW NAME   || :- ")
                        query = '''update patient_info set name = %s where email = %s;'''
                        break

                    
                    elif ch2 == "2":
                        email = input("||   CONFIRMED EMAIL-ID   || :- ")
                        print("")
                        new_data = input("||   ENTER PATIENT NEW DOB (YYYY:MM:DD)   || :- :")
                        query = '''update patient_info set dob = %s where email = %s;'''
                        break

                    elif ch2 == "3":
                        email = input("||   CONFIRMED EMAIL-ID   || :- ")
                        print("")
                        new_data = input("||   ENTER YOUR GENDER   || :- :")
                        query = '''update patient_info set gender = %s where email = %s;'''
                        break

                    elif ch2 == "4":
                        email = input("||   CONFIRMED EMAIL-ID   || :- ")
                        print("")
                        new_data = input("||   ENTER YOUR BLOOD GROUP TYPE (A+,B+,O+,AB+,A-,B-,O-,AB-)   || :- ")
                        query = '''update patient_info set bg = %s where email = %s;'''
                        break

                    elif ch2 == "5":
                        email = input("||   CONFIRMED EMAIL-ID   || :- ")
                        print("")
                        new_data = input("||   ENTER PATIENT NEW CONTACT   || :- ")
                        query = '''update patient_info set contact = %s where email = %s;'''
                        break

                    elif ch2 == "6":
                        print("""
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                UPDATE       PROCESS       CANCELLED
                        < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <
                        
                        """)

                        updateflag = True
                        break

                    else:
                        print("""
                        * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                I N V A L I D     C H O I C E
                        * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                        
                        """)

                if updateflag == True :
                    pass

                else :
                    z = app.UpdateInfo(query , new_data , email)
                    if z != True :
                        print(f"\n*************** {z} *****************\n")

                    else :        
                        print("""
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                        SUCCESSFULLY   INFORMATION   UPDATED
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                        
                        """)

            elif p_ch == '6':

                print("""
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                B A C K      T O       T H E       H O M E
                        > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                        
                        """)
                break

            else:
                print("""
                        * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                I N V A L I D     C H O I C E
                        * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                        
                        """)



    elif ch == '4':
        print("""
            ---------------------------------------------------------------------------------------------
                                        GENERATE PASSWORD FOR DOCTOR
            ---------------------------------------------------------------------------------------------
        
        """)
        email=input("||  ENTER YOUR EMAIL-ID  || : -")
        pass1=input("||  ENTER YOUR PASSWORD  || : -")
        pass2=input("||  CONFIRM YOUR PASSWORD  || : -")
        if pass1!=pass2:
            print("""
                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                           P A S S W O R D     D I D     N O T      M A T C H E D
                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
            
            """)

        else:
            x=app.generatepassword_d(pass1,email)

            if x!=True:
                print(f"\n*********** {x}************\n")
            else:
                print("""
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                                              SUCCESSFULLY   PASSWORD GENERATED
                                    > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
                                    
                                    """)
        


    elif ch == '5':
        print("""
            =================================================================================================
                        T H A N K         Y O U         V I S I T          A G A I N
            =================================================================================================
        
        """)
        break

    else:
        print("""
                                    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                                          I N V A L I D     C H O I C E
                                    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                                    
                                    """)

