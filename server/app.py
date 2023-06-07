import openai
from flask import Flask, jsonify, request, send_file
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from enum import Enum
import backoff
import time
import ast
from flask_sse import sse
from babel.numbers import format_currency
import pdfkit
import io


class Role(Enum):
    system = 1
    user = 2
    assistant = 3


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
openai.api_key = "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"


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def chat_completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def get_embedding_with_backoff(**kwargs):
    return get_embedding(**kwargs)


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def create_embedding_with_backoff(**kwargs):
    return openai.Embedding.create(**kwargs)


attribute_keys = [
    "snap_product_id",
    "title",
    "description",
    "link",
    "image_link",
    "google_product_category",
    "product_type",
    "brand",
    "gender",
    "sale_price_micro_amount",
    "sale_price_currency"
]

# Lucy Catalog
# SELECT * FROM `snapchat-pcs-prod.v1.products_20230427`
# where catalog_id='6aada195-bba1-4ad5-8e1e-d88dc9ad7cec'

# Uncomment if you use a new catalog
get_embedding_start_time = time.time()
product_data_df = pd.read_csv('lucy_catalog.csv')
product_data_df['combined'] = product_data_df.apply(
    lambda row: f"{row['title']}, {row['description']}, {row['google_product_category']}, {row['product_type']}, {row['brand']}, {row['gender']}", axis=1)
product_data_df['text_embedding'] = product_data_df.combined.apply(
    lambda x: get_embedding_with_backoff(text=x, engine='text-embedding-ada-002'))
product_data_df.to_csv('example.csv', index=False)
print("get_embedding: " + str(time.time() - get_embedding_start_time))

# comment if you use a new catalog
#product_data_df = pd.read_csv('example.csv')
product_data_df['text_embedding'] = product_data_df['text_embedding'].apply(
    ast.literal_eval)

# hack for now
# in-memory cache for every user session
# we didn't clear any thing yet in-memory
message_objects_map = {}


@app.route("/health", methods=["GET"])
def health():
    return jsonify(success=True)


@app.route("/recommend-product", methods=["GET"])
def recommend_product():
    # example: "Hi! Can you recommend a good moisturizer for me?"
    customer_input = request.args.get('customer_input')
    session_id = request.args.get('session_id')

    if not session_id:
        return jsonify({"error": "Please provide a session_id"}), 400

    if not customer_input:
        return jsonify({"error": "Please provide a prompt"}), 400

    try:
        global product_data_df
        global message_objects_map

        def format_price(sale_price_micro_amount, sale_price_currency):
            price = sale_price_micro_amount / 1000000
            formatted_price = format_currency(
                price, sale_price_currency, locale='en_US')
            return formatted_price

        product_data_df['formatted_price'] = product_data_df.apply(lambda row: format_price(
            row['sale_price_micro_amount'], row['sale_price_currency']), axis=1)
        product_data_df['chat_combined'] = product_data_df.apply(
            lambda row: f"{row['title']}, {row['description']}, {row['google_product_category']}, {row['product_type']}, {row['brand']}, {row['gender']}, {row['formatted_price']}", axis=1)
        create_embedding_start_time = time.time()
        response = create_embedding_with_backoff(
            input=customer_input,
            model="text-embedding-ada-002"
        )
        embeddings_customer_question = response['data'][0]['embedding']
        print("create_embedding: " + str(time.time() - create_embedding_start_time))

        cosine_similarity_start_time = time.time()
        product_data_df['search_products'] = product_data_df.text_embedding.apply(
            lambda x: cosine_similarity(x, embeddings_customer_question))
        product_data_df = product_data_df.sort_values(
            'search_products', ascending=False)
        print("cosine_similarity: " +
              str(time.time() - cosine_similarity_start_time))

        top_2_products_df = product_data_df.drop_duplicates(
            subset=["title"]).head(2)
        sse.publish({'recommend_products': top_2_products_df[attribute_keys].to_json(
            orient="records")}, type="recommend", channel=session_id)

        message_objects = []
        if session_id:
            if session_id not in message_objects_map:
                message_objects_map[session_id] = []
            message_objects = message_objects_map[session_id]

        def append_message_objects(role, content):
            message_objects.append({"role": role, "content": content})

        append_message_objects(
            Role.system.name, "Hey there. I'm your shopping co-pilot. What can I help you find today? Please tell me what you're looking for?")
        append_message_objects(Role.user.name, customer_input)
        append_message_objects(
            Role.user.name, "Please give me a detailed explanation of your recommendations")
        append_message_objects(
            Role.user.name, "Please be friendly and talk to me like a person, don't just give me a list of recommendations")
        append_message_objects(Role.assistant.name,
                               "I found these 2 products I would recommend")
        products_list = []
        for index, row in top_2_products_df.iterrows():
            brand_dict = {'role': Role.assistant.name,
                          "content": f"{row['chat_combined']}"}
            products_list.append(brand_dict)

        message_objects.extend(products_list)
        append_message_objects(
            Role.assistant.name, "Here's my summarized recommendation of products, and why it would suit you:")

        chat_completion_start_time = time.time()
        response = chat_completion_with_backoff(
            model="gpt-3.5-turbo",
            messages=message_objects,
            stream=True
        )
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']
            sse.publish({'text': chunk_message},
                        type="text", channel=session_id)
        print("chat_completion: " + str(time.time() - chat_completion_start_time))
        return jsonify(success=True), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    html = request.json['html']
    pdf = pdfkit.from_string(html, False)

    buffer = io.BytesIO(pdf)
    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='output.pdf')


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


if __name__ == "__main__":
    app.run(debug=True)
