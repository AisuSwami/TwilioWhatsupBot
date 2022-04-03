# Call an external API 
# Get the response
# Print the response

from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
import random
        
app = Flask(__name__)
        
        
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg+'..')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
        
    if incoming_msg in ['hello','hi','hey','start','hii']:
        response = """
            *Hello!! Welcome to 'of-the-day' Bot. Daily dose of fun and learning in equal parts!*
        Here are some options to start with:
            > *'quote':* Get quote of the day!
            > *'word':* Get word of the day!
            > *'joke':* Get joke of the day!
            > *'meme'*: Get meme of the day."""
        msg.body(response)
        responded = True
            
    elif 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Sorry! We could not retrieve a quote at this time.'
        msg.body(quote)
        responded = True
            
    elif 'meme' in incoming_msg:
        #return a meme
        r = requests.get('https://www.reddit.com/r/memes/top.json?limit=20?t=day', headers = {'User-agent': 'whatsbot 0.1'})
                    
        if r.status_code == 200:
            data = r.json()
            memes = data['data']['children']
            random_meme = random.choice(memes)
            meme_data = random_meme['data']
            title = meme_data['title']
            image = meme_data['url']
        
            msg.body(title)
            msg.media(image)
                    
        else:
            msg.body('Sorry, We cannot find memes at this time.')
        responded = True
    
    elif 'joke' in incoming_msg:
        # return a joke
        headers = {}
        payload = {}
        r = requests.get('https://backend-omega-seven.vercel.app/api/getjoke', headers = headers, data = payload)                                                                                                                                                                                                                                                                                                      
        if r.status_code == 200:
            jokes = json.loads(r.text)  
            for joke in jokes:
                print_joke = f'{joke["question"]}\n{joke["punchline"]}'
                break
            joke["question"] = data["question"]
            joke["punchline"] = data["punchline"]
            joke = f'{data["question"]} ({data["punchline"]})'
        else:
            print_joke = 'Sorry! We could not retrieve a joke at this time.'
        msg.body(print_joke)
        responded = True
    
    elif 'word' in incoming_msg:
        # return a word
        headers = {}
        payload = {}
        r = requests.get('https://san-random-words.vercel.app/', headers = headers, data = payload)                                                                                                                                                                                                                                                                                                      
        if r.status_code == 200:
            word_data = json.loads(r.text)  
            for word_single in word_data:
                print_word = f'{word_single["word"]}\n{word_single["definition"]}'
                break
        else:
            print_word = 'Sorry! We could not retrieve a word at this time.'
        msg.body(print_word)
        responded = True
        
    if not responded:
        msg.body('We can only help you with Word, Jokes, Quotes and Memes')
    return str(resp)
        
        
if __name__ == '__main__':
    app.run()