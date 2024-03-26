import json
import os

from flask import Flask, request, jsonify, abort
import google.generativeai as genai

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/gen')
def gen():

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content("The opposite of hot is")

    return response.text


@app.route('/translate', methods=["GET", "POST"])
def trans():
    """

    request data:
    {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text":"My user id is s4dkvkmtKl. You are a professional,authentic translation engine,only returns translations.\\nFor example:\\n<Start>\\nHello <Keep This Symbol>\\nWorld <Keep This Symbol>\\n<End>\\nThe translation is:\\n<Start>\\n\xe4\xbd\xa0\xe5\xa5\xbd<Keep This Symbol>\\n\xe4\xb8\x96\xe7\x95\x8c<Keep This Symbol>\\n<End>\\n\\nTranslate the content to zh-CN Language:\\n\\n<Start>Authors: core dbt maintainers<End>"
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 2048,
            "stopSequences": [],
            "temperature": 0.1,
            "topK": 1,
            "topP": 1
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
    }

    Original url: https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}
    :return:
    """
    # all_get_params = request.args.to_dict()
    #
    # print('--- get params: %d' % len(all_get_params))
    # for key, value in all_get_params.items():
    #     print(f"GET parameter: {key} - {value}")
    #
    # all_post_params = request.form.to_dict()
    #
    # print('--- post params: %d' % len(all_post_params))
    # for key, value in all_post_params.items():
    #     print(f"POST parameter: {key} - {value}")
    #
    # if request.data:
    #     print('--- request data:')
    #     print(request.data)

    access_key = request.args.get('key', '')

    print('--- access key: %s' % access_key)

    if access_key == '' or access_key != os.environ["ACCESS_API_KEY"]:
        abort(401)

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel('gemini-pro')

    response_text = 'This is great!'
    ai_response = ''

    request_data = request.data

    if request_data:
        request_data = request_data.decode('utf-8')
        json_data = json.loads(request_data)

        print('--- contents: %s' % json_data['contents'])

        contents = json_data['contents']
        for content in contents:
            parts = content.get('parts')
            for part in parts:
                print('--- prompt: %s' % part.get('text'))
                ai_response = model.generate_content(part.get('text'))

    if ai_response:
        response_text = ai_response.text

    result = {
        "errcode": "ok",
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": response_text
                        }
                    ]
                }
            }
        ]
    }

    json_response = jsonify(result)
    json_response.headers['Content-Type'] = 'application/json'
    return json_response


@app.route('/about')
def about():
    return 'About'
