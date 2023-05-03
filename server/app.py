import openai
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from enum import Enum
import backoff
import time
import ast


class Role(Enum):
    system = 1
    user = 2
    assistant = 3


app = Flask(__name__)
CORS(app)

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
]

# Lucy Catalog
# SELECT * FROM `snapchat-pcs-prod.v1.products_20230427`
# where catalog_id='6aada195-bba1-4ad5-8e1e-d88dc9ad7cec'

# Uncomment if you use a new catalog
# get_embedding_start_time = time.time()
# product_data_df = pd.read_csv('lucy_catalog.csv')
# product_data_df['combined'] = product_data_df.apply(
#     lambda row: f"{row['title']}, {row['description']}, {row['google_product_category']}, {row['product_type']}, {row['brand']}, {row['gender']}", axis=1)
# product_data_df['text_embedding'] = product_data_df.combined.apply(
#     lambda x: get_embedding_with_backoff(text=x, engine='text-embedding-ada-002'))
# product_data_df.to_csv('example.csv', index=False)
# print("get_embedding: " + str(time.time() - get_embedding_start_time))

# comment if you use a new catalog
product_data_df = pd.read_csv('example.csv')
product_data_df['text_embedding'] = product_data_df['text_embedding'].apply(
    ast.literal_eval)


@app.route("/", methods=["GET"])
def home():
    return "Welcome to the StyleBot Flask App!"


@app.route("/recommend-product", methods=["POST"])
def recommend_product():
    data = request.get_json()
    # example: "Hi! Can you recommend a good moisturizer for me?"
    customer_input = data.get("customer_input")

    if not customer_input:
        return jsonify({"error": "Please provide a prompt"}), 400

    try:
        global product_data_df
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

        top_3_products_df = product_data_df.head(3)

        message_objects = []

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
                               "I found these 3 products I would recommend")
        products_list = []
        for index, row in top_3_products_df.iterrows():
            brand_dict = {'role': Role.assistant.name,
                          "content": f"{row['combined']}"}
            products_list.append(brand_dict)

        message_objects.extend(products_list)
        append_message_objects(
            Role.assistant.name, "Here's my summarized recommendation of products, and why it would suit you:")

        chat_completion_start_time = time.time()
        response = chat_completion_with_backoff(
            model="gpt-3.5-turbo",
            messages=message_objects
        )
        generated_text = response.choices[0].message['content'].strip()
        print("chat_completion: " + str(time.time() - chat_completion_start_time))
        return jsonify({"text": generated_text, "recommend_products": top_3_products_df[attribute_keys].to_json(orient="records")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
