import json
import datetime

#Returns the user's Username (the Username that appears in ever conversation)
def find_main_username(jfile):     
    participants = []
    if len(jfile) < 2:    return None               #in case we have only one conversation
    for conversation in range(len(jfile)-1):
        participants.extend(jfile[conversation]["participants"])  
    all_usernames=sorted(participants,key=participants.count,reverse=True)
    if all_usernames[0] != all_usernames[1]:
        return None                                 # we are unable to identify the username, a userB appers in every conversation also
    else:
        return all_usernames[0]

#Saves the messages of the conversation
def save_messages(name,texts_list):    
    with open(f"{name}.txt", "w",encoding="utf8") as f:
        for line in texts_list:
            f.write(line+"\n")

#Returns partener's Username
#I'm using a list because it might be a group chat
def find_participants(main_username,participants_list):
    temp_list= sorted(participants_list)  
    if main_username:
        temp_list.remove(main_username)
        return ", ".join(temp_list)
    else:
        return ", ".join(temp_list)

#Loads the messages.json file
with open('messages.json', encoding="utf8") as f:
    jfile = json.load(f)


def main():
    my_name = find_main_username(jfile)
    pre_user = ""
    texts_list = []

    for session in reversed(range(len(jfile))):
        #it is reversed because we need the oldest messages first
        indx = len(jfile[session]["conversation"])-1
        pre_date = ""
        cur_user = find_participants(my_name,jfile[session]["participants"])

        #if the user we chatting change, we save and empty the messages container
        #this happens cause a conversation might be included in more than one session, depending on the length 
        if pre_user and pre_user != cur_user:
            save_messages(pre_user,texts_list)
            texts_list = []

        pre_user = cur_user

        while indx>=0:
            #only storing the text messages, ignoring reactions etc
            if "text" in jfile[session]["conversation"][indx]:

                #the time gets trimmed and converted to a datetime object
                dtime = datetime.datetime.strptime(jfile[session]["conversation"][indx]["created_at"][:19], '%Y-%m-%dT%H:%M:%S')
                cur_date = dtime.date()

                #adding a visual indicator for each new date
                if cur_date != pre_date:
                    texts_list.append("\n///////////////")
                    texts_list.append("///"+dtime.strftime('%d/%m/%y')+"///")
                    texts_list.append("//////////////\n")
                    pre_date=dtime.date() 

                #the format of how the messages will be represented in the final TXT file
                text=f'{dtime.time()} {jfile[session]["conversation"][indx]["sender"]}: {jfile[session]["conversation"][indx]["text"]}'
                texts_list.append(text)
            indx-=1

    #Save the last conversation    
    if texts_list:
        save_messages(cur_user,texts_list)

if __name__ == '__main__':
    main()