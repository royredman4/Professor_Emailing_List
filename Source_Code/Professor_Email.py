
import smtplib
import getpass
import os.path
import sys
import string
import time





def senderemail(class_, to_address, message, server, login):
    subject_header = class_ + " Course Information"
    from_addr = YOUR_EMAIL_ADDRESS_GOES_HERE

    message = string.join((
                "From: %s" % from_addr,
                "To: %s" % to_address,
                "Subject: %s" % subject_header,
                "",
                message
                ), "\r\n")

    server.sendmail(login, to_address, message)

    
def Get_Professor_Info():
    first = ""
    second = ""
    temp = ""
    #input where you want to store your text file that holds your professors names and emails
    fileLocation = FILE_LOCATION_GOES_HERE
    if (os.path.exists(fileLocation)):
        temp_Storage = []
        t = 0
        with open(fileLocation) as f:
            while True:
                if t == 0:
                    f.readline()
                    f.readline()
                    t = 4

                temp = f.read(1)
                if not temp:
                    # print("End of the file")
                    break
                while t == 4:
                    if temp == " ":
                        break
                    first += temp
                    temp = f.read(1)
                # print ("first is " + first)
                temp = f.read(2)
                
                while t == 4:
                    temp = f.read(1)
                    if temp == ".":
                        second += temp
                        second += f.read(3)
                        f.read(1)
                        break
                    second += temp
                
                # print ("Second is " + second)
                temp_Storage.append((first, second))
                first = ""
                second = ""
            f.close()
        return temp_Storage
    else:
        os.mkdirs(fileLocation)
        return "NULL"

    
def Professor_Search(name, Prof_history):
    for i in range(0, len(Prof_history)):
        if name == Prof_history[i][0]:
            return Prof_history[i][1]
    return "NULL"
        
        
def Create_Index(Last_name, Course_name, Course_number, email):
    message = "Hello Professor "
    message += Last_name
    message += ". I'm planning on taking "
    message += Course_number
    message += " ("
    message += course_Name
    message += ") next semester and I have heard nothing but good things about your class. "
    message += "I was wondering if there was any way I would be able to get information on when you were teaching your "
    message += Course_number
    message += " class next semester, so I will be able to take your awesome class?\n\n"
    message += "I apologize if I sound a tad assertive, I just would really love to attend your class next semester since it seems that you have a great understanding of the course and I could learn alot of wonderful things from your class.\n\n"

    message += "thanks for your time!!"
    return (Last_name, Course_name, Course_number, email, message)


def Display_Professors(Prof):
    print("Professors Are:")
    for i in range(0, len(Prof)):
        print(Prof[i][0] + " - " + Prof[i][1])
    print("\n")

    
def Display_Index(Last_name, Course_name, Course_number, email):
    print("Professors Last Name: " + str(Last_name) + "\n")
    print("Course Name: " + str(Course_name) + "\n")
    print("Course Number: " + str(Course_number) + "\n")
    print("Email Address: " + str(email) + "\n")


def in_put(output):
    if (sys.version_info > (3, 0)):
        return input(output)
    else:
        return raw_input(output)

    
Profesor_History = Get_Professor_Info()
New_Professors = []
if (Profesor_History == "NULL"):
    Nothing_Stored = True
else:
    Nothing_Stored = False


login = EMAIL_ADDRESS_HERE 

#input where you want to store your text file that holds your professors names and emails
fileLocation = FILE_LOCATION_GOES_HERE
Sending_List = []
different_course = True
                   
Display_Professors(Profesor_History)

x = "1"
while x != "-1":
    Professor_Last_Name = in_put('What is the Last Name of the professor you\'re emailing? ')
    if (different_course):
        course_Name = in_put("What is the name of the course? (Ex: Computer Architecture) ")
        subject = in_put("What is the Course number? Ex: (CPSC 440) ")

    searchResult = Professor_Search(Professor_Last_Name, Profesor_History)
    if (searchResult == "NULL"):
        sending_to = in_put("What is their email address? ")
        New_Professors.append((Professor_Last_Name, sending_to))
        Profesor_History.append(New_Professors[len(New_Professors)-1])
    else:
        sending_to = searchResult

    Sending_List.append(Create_Index(Professor_Last_Name, course_Name, subject, sending_to))
    
    print("\n\nThe Email has been successfully added into the queue\n\n")

    temp = in_put("Do you still have other professors \nto email with for " + course_Name + "? (y/n): ")
    if (temp == "y" or temp == "Y"):
        different_course = False

    else:
        different_course = True
        x = in_put("\nType in \"-1 + enter\" to stop adding emails, \notherwise, press anything else to continue: ")


file = open(fileLocation, "a")
for i in range(0, len(New_Professors)):
    file.write(New_Professors[i][0] + " - " + New_Professors[i][1] + "\n")

for i in range(0, len(Sending_List)):
    print ("Email # " + str(i+1) + " is : \n")
    Display_Index(Sending_List[i][0], Sending_List[i][1], Sending_List[i][2], Sending_List[i][3])


#FOR WHEN YOU ACTUALLY WANT TO EMAIL THE PROFESSORS



condition = True
while condition:
    password = getpass.getpass()
    
    #configure The server and the host. ex: smtplib.SMTP("smtp.live.com", 587) 
    server = smtplib.SMTP(PORT_NAME, PORT)
    server.ehlo()
    server.starttls()

    condition = False
    try:
        server.login(login, password)
    except:
        print("Error!! Wrong password for " + login + "please try again")
        password = ""
        condition = True


for i in range(0, len(Sending_List)):
    senderemail(Sending_List[i][2], Sending_List[i][3], Sending_List[i][4], server, login)
    
server.quit()

print("Finished the loop and waiting here")

    

