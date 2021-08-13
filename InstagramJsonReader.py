import json
import datetime

#Finds the my Username 
def find_myname(jfile):     #Finds the my Username 
    participants = []
    if len(jfile) < 2:    return None 
    for s in range(len(jfile)-1):
        participants.extend(jfile[s]["participants"])  
    myname=sorted(participants,key=participants.count,reverse=True)
    if myname[0] != myname[1]:
        return None
    else:
        return myname[0]

#Saves the messages
def dump_messages(name,texts_list):    
    with open(f"{name}.txt", "w",encoding="utf8") as f:
        for line in texts_list:
            f.write(line+"\n")

#Finds the partener's Username
def find_participants(myname,participants_list):
    temp_list= sorted(participants_list)  
    if myname:
        temp_list.remove(myname)
        return ", ".join(temp_list)
    else:
        return ", ".join(temp_list)


#open JSON file
with open('messages.json', encoding="utf8") as f:
    jfile = json.load(f)


def main():
    my_name = find_myname(jfile)
    pre_user = ""
    texts_list = []

    for session in reversed(range(len(jfile))):
        indx = len(jfile[session]["conversation"])-1
        pre_date = ""
        cur_user = find_participants(my_name,jfile[session]["participants"])

        if pre_user and pre_user != cur_user:
            dump_messages(pre_user,texts_list)
            texts_list = []

        pre_user = cur_user
        while indx>=0:
            if "text" in jfile[session]["conversation"][indx]:
                dtime = datetime.datetime.strptime(jfile[session]["conversation"][indx]["created_at"][:19], '%Y-%m-%dT%H:%M:%S')
                cur_date = dtime.date()

                if cur_date != pre_date:
                    texts_list.append("\n////////////////")
                    texts_list.append("///"+dtime.strftime('%d/%m/%y')+"///")
                    texts_list.append("///////////////\n")
                    pre_date=dtime.date() 

                text=f'{dtime.time()} {jfile[session]["conversation"][indx]["sender"]}: {jfile[session]["conversation"][indx]["text"]}'
                texts_list.append(text)
            indx-=1
        
    if texts_list:
        dump_messages(cur_user,texts_list)

if __name__ == '__main__':
    main()