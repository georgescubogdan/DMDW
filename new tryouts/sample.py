import websocket
import json
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.test.utils import datapath
from lda import LdaModel
from pathlib import Path
import os
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
# https://github.com/aspnet/SignalR/blob/release/2.2/specs/HubProtocol.md

ws = None
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create English stop words list
en_stop = get_stop_words('en')
tokenizer = RegexpTokenizer(r'\w+')


doc_set = []
for filename in os.listdir('./'):
    if filename.endswith(".txt"):
        path_in_str = os.path.join('./', filename)
        print(path_in_str)
        with open(path_in_str,"r") as f:
            contents = f.read()
            doc_set.append(contents)
            print([contents])

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:

    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)
    print('TOKENS')
    print(tokens)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    print('REMOVE STOP WORDS')
    print(stopped_tokens)

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    print('STEAMED')
    print(stemmed_tokens)

    # add tokens to list
    texts.append(stemmed_tokens)


common_dictionary = Dictionary(texts)
def encode_json(obj):
    # All JSON messages must be terminated by the ASCII character 0x1E (record separator).
    # Reference: https://github.com/aspnet/SignalR/blob/release/2.2/specs/HubProtocol.md#json-encoding
    return json.dumps(obj) + chr(0x1E)

def ws_on_message(ws, message: str):
    ignore_list = ['{"type":6}', '{}']
    # Split using record seperator, as records can be received as one message
    temp_file = datapath("model")
    model = LdaModel.load(temp_file)

    for msg in message.split(chr(0x1E)):
        if msg and msg not in ignore_list:
            # Everything else not on ignore list
            print(f"From server: {msg}")
            raw = msg.lower()
            tokens = tokenizer.tokenize(raw)
            print('TOKENS')
            print(tokens)

            # remove stop words from tokens
            stopped_tokens = [i for i in tokens if not i in en_stop]
            print('REMOVE STOP WORDS')
            print(stopped_tokens)

            # stem tokens
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            print('STEAMED')
            print(stemmed_tokens)

            other_corpus = [common_dictionary.doc2bow(stemmed_tokens)]
            unseen_doc = other_corpus[0]
            print([t for t in unseen_doc if t[0] < 1500 ])
            res = model[[t for t in unseen_doc if t[0] < 1500 ]]  # get topic probability distribution for a document
            print(res)

            # TODO: Perform your own handling here
            # TODO: Procces text
            # TODO: Apply model and save result in r. Comment bellow line
            r = [(0, 0.04605865), (1, 0.06408988), (2, 0.027407577), (3, 0.0882964), (4, 0.02613459), (5, 0.036566347), (6, 0.015112683), (7, 0.045046393), (8, 0.03568833), (9, 0.6155991)]
            print(dict((x + 1, y) for x, y in res))
            # print(r)
            # print(dict((x + 1, y) for x, y in r))
            formated_response = json.dumps(dict((x + 1, str(y)) for x, y in res))
            # formated_response = json.dumps(dict((x, y) for x, y in r))
            print(formated_response)
            ws.send(encode_json({
                "type": 1,
                "target": "SendMessage",
                "arguments": ["Response", formated_response]
            }))

def ws_on_error(ws, error):
    print(error)

def ws_on_close(ws):
    print("### Disconnected from SignalR Server ###")

def ws_on_open(ws):
    print("### Connected to SignalR Server via WebSocket ###")
    # Do a handshake request
    print("### Performing handshake request ###")
    ws.send(encode_json({
        "protocol": "json",
        "version": 1
    }))

    # Handshake completed
    print("### Handshake request completed ###")

    # Call chathub's send message method
    # Reference: https://github.com/aspnet/SignalR/blob/release/2.2/specs/HubProtocol.md#invocation-message-encoding
    ws.send(encode_json({
        "type": 1,
        "target": "SendMessage",
        "arguments": ["Python websocket", "Hello world!"]
    }))

    print("### Hello world message sent to ChatHub ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000/chathub",
                              on_message = ws_on_message,
                              on_error = ws_on_error,
                              on_close = ws_on_close)
    ws.on_open = ws_on_open
    ws.run_forever()