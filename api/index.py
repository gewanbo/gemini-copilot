import json
import os
import logging
from flask import Flask, request, jsonify, abort
import google.generativeai as genai

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure genai once
api_key = os.getenv("GEMINI_API_KEY", "default_api_key")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return 'Hello, World! -- Version: 0.1.1'

@app.route('/gen')
def gen():
    try:
        response = model.generate_content("The opposite of hot is")
        return response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

    try:
        access_key = request.args.get('key', '')

        logger.info('--- access key: %s' % access_key)

        if access_key == '' or access_key != os.environ["ACCESS_API_KEY"]:
            abort(401)

        request_data = request.data

        if request_data:
            request_data = request_data.decode('utf-8')
            json_data = json.loads(request_data)
            logger.info(f"Request data: {json_data}")

            contents = json_data.get('contents', [])
            response_text = 'This is great!'
            ai_response = ''

            for content in contents:
                parts = content.get('parts', [])
                for part in parts:
                    prompt_text = part.get('text', '')
                    logger.info(f"Generating content for prompt: {prompt_text}")
                    ai_response = model.generate_content(prompt_text)

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
            logger.info("Translation successful")
            return json_response
        else:
            logger.warning("No request data provided")
            return jsonify({"error": "No request data provided"}), 400
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/about')
def about():
    return 'About'
