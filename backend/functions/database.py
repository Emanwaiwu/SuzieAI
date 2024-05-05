import json
import random

#get recent messages
def get_recent_messages():
    #define the file name and learn instructions
    file_name = "stored_data.json"
    learn_instructions = {
        "role":"system",
        "content": "You are an assistant and friend to the user! Your name is Suzie, interact with the user.",
    }
    
        #Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instructions["content"] = learn_instructions["content"] + "Your response should include some humor."
    else:
        learn_instructions["content"] = learn_instructions["content"] + "Your response should also include you talking about yourself, your day, the weather, school etc."

    #initialize messages 
    messages = []

    #Append instructions to messages
    messages.append(learn_instructions)

    #get last messages 
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            #Append last 5 items of data
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)

    except Exception as e:
        print(e)
        pass
    return messages

#store messages
def store_messages(request_message, response_message):
    #def file name
    file_name="stored_data.json"

    #get recent messages
    messages = get_recent_messages()[1:]

    #add messages to data 
    user_message = {"role": "user", "content":request_message}
    assistant_message = {"role": "assistant", "content":response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    #save the updated file
    with open (file_name, "w") as f:
        json.dump(messages, f)

#reset messages 
def reset_messages():

    #overwrite current file with nothing.
    open("stored_data.json", "w")
