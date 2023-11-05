import re
import random
import os
import sys
import time

def generate_8ball_response():
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    return random.choice(responses)

def send_reply(file_path, message):
    mode = 'a' if os.path.exists(file_path) else 'w'
    with open(file_path, mode) as file:
        #file.write(f"SP {message['TO']} < 8BALL ${random.randint(10000, 99999)}_{my_call}\n")
        file.write(f"SP {message['TO']} < 8BALL\n")        
        file.write(f"{message['Title']}\n")
        file.write(f"{message['Body']}\n/EX\n")

def handle_messages(file_path):
    messages = []
    current_message = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == '/EX':
                    if 'Body' in current_message:
                        current_message['Body'] = '\n'.join(current_message['Body'])
                        messages.append(current_message)
                    current_message = {}
                else:
                    if line.startswith('SP '):
                        match = re.match(r'SP\s+(.*?)\s+<\s+(.*?)\s+(\$.*)', line)
                        if match:
                            current_message['TO'] = match.group(1).replace(" ", "")
                            current_message['FROM'] = match.group(2).strip()
                            current_message['ID'] = match.group(3)
                        else:
                            print(f"Invalid 'SP' line (missing FROM or ID): {line}")
                    elif not current_message.get('Title'):
                        current_message['Title'] = line
                    elif line.startswith('R:'):
                        match = re.match(r'R:.*@(.*) .*', line)
                        if match:
                            current_message['FROM_HA'] = match.group(1)
                    else:
                        if not current_message.get('Body') and line == '':
                            continue
                        current_message.setdefault('Body', []).append(line)

        for message in messages:
            process_message(message)

        # Delete the file once it has been read
        os.remove(file_path)

    except FileNotFoundError:
        pass

def quote_text(text):
    quoted_lines = []
    lines = text.split("\n")
    for line in lines:
        quoted_lines.append("> " + line)
    quoted_text = "\n".join(quoted_lines)
    return quoted_text

def process_message(message):
    print("Processing message:")
    print(message)

    previous_message = f"{quote_text(message['Body'])}\n\n"
    response_8ball = generate_8ball_response()

    body = previous_message + response_8ball

    reply = {"TO": f"{message['FROM']}@{message['FROM_HA']}", "FROM": message['TO'], "Title": f"RE: {message['Title']}", "Body": body}

    send_reply(out_file, reply)

def get_env_var_or_exit(var_name):
    value = os.getenv(var_name)
    if value is None or value == "":
        print(f"Error: Environment variable '{var_name}' is not set or empty.")
        sys.exit(1)
    return value


def main():
    global my_call
    global in_file
    global out_file

    my_call = get_env_var_or_exit("MY_CALL")
    in_file = get_env_var_or_exit("IN_FILE")
    out_file = get_env_var_or_exit("OUT_FILE")

    while True:
        handle_messages(in_file)
        time.sleep(5)

if __name__ == '__main__':
    main()

