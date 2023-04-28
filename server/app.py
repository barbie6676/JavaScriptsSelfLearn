import openai
from flask import Flask, jsonify, request
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from enum import Enum
import random
import time


class Role(Enum):
    system = 1
    user = 2
    assistant = 3


app = Flask(__name__)

openai.api_key = "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"

# define a retry decorator


def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (openai.error.RateLimitError,),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specified errors
            except errors as e:
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper


@retry_with_exponential_backoff
def chat_completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


@retry_with_exponential_backoff
def get_embedding_with_backoff(**kwargs):
    return get_embedding(**kwargs)


@retry_with_exponential_backoff
def cosine_similarity_with_backoff(**kwargs):
    return cosine_similarity(**kwargs)


@retry_with_exponential_backoff
def create_embedding_with_backoff(**kwargs):
    return openai.Embedding.create(**kwargs)


product_data = [{
    "prod_id": 1,
    "prod": "moisturizer",
    "brand": "Aveeno",
    "description": "for dry skin",
    "url": "https://www.aveeno.com/products/moisturizing-lotion-for-very-dry-skin",
    "image_url": "https://www.aveeno.com/sites/aveeno_us_2/files/styles/jjbos_adaptive_images_generic-tablet/public/product-images/ave_381371182176_us_skin_relief_moisturizing_lotion_fragrance_free_33oz_00015-min.png"
},
    {
    "prod_id": 2,
    "prod": "foundation",
    "brand": "Maybelline",
    "description": "medium coverage",
    "url": "https://www.amazon.com/Maybelline-Poreless-Foundation-Natural-Oil-Free/dp/B00PFCSURS/ref=asc_df_B00PFCSURS/?tag=hyprod-20&linkCode=df0&hvadid=312127951361&hvpos=&hvnetw=g&hvrand=14075047475504352054&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9031934&hvtargid=pla-360157827499&psc=1",
    "image_url": "https://m.media-amazon.com/images/I/71v7ECrH7lS._SX679_.jpg"
},
    {
    "prod_id": 3,
    "prod": "moisturizer",
    "brand": "CeraVe",
    "description": "for dry skin",
    "url": "https://www.cerave.com/skincare/moisturizers/moisturizing-cream",
    "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products-v4/moisturizing-cream/cerave_moisturizing_cream_16oz_jar_front-700x875-v3.jpg?rev=8bd2516ca01e42328ae905e2e312709e?w=500&hash=BEB029F78EBCDB5C9DFC1B778B97B1BE"
},
    {
    "prod_id": 4,
    "prod": "nail polish",
    "brand": "OPI",
    "description": "raspberry red",
    "url": "https://www.amazon.com/s?k=opi+raspberry+nail+polish&hvadid=177545499339&hvdev=c&hvlocphy=9031934&hvnetw=g&hvqmt=e&hvrand=12899016763763224639&hvtargid=kwd-42288850862&hydadcr=22033_9708579&tag=googhydr-20&ref=pd_sl_28m8rz4iy7_e",
    "image_url": "https://m.media-amazon.com/images/I/61F0LNrjufL._AC_UL800_FMwebp_QL65_.jpg"
},
    {
    "prod_id": 5,
    "prod": "concealer",
    "brand": "Chanel",
    "description": "medium coverage",
    "url": "https://www.chanel.com/us/makeup/face/c/5x1x6x36/concealer/",
    "image_url": "https://puls-img.chanel.com/c_limit,w_3200/q_auto:best,dpr_auto,f_auto/1662565558090-correcteursmakeupplpdesktopwebp_720x2304.webp"
},
    {
    "prod_id": 6,
    "prod": "moisturizer",
    "brand": "Ole Henkrisen",
    "description": "for oily skin",
    "url": "https://olehenriksen.com/collections/moisturizer/products/strength-trainer-peptide-boost-moisturizer",
    "image_url": "https://cdn.shopify.com/s/files/1/0615/7785/5148/products/ST_SILO_01_1_1600x.jpg?v=1679593092"
},
    {
    "prod_id": 7,
    "prod": "moisturizer",
    "brand": "CeraVe",
    "description": "for normal to dry skin",
    "url": "https://www.cerave.com/skincare/dry-skin",
    "image_url": "https://www.cerave.com/-/media/project/loreal/brand-sites/cerave/americas/us/products-v4/moisturizing-cream/cerave_moisturizing_cream_16oz_jar_front-700x875-v3.jpg?rev=8bd2516ca01e42328ae905e2e312709e?w=500&hash=BEB029F78EBCDB5C9DFC1B778B97B1BE"
},
    {
    "prod_id": 8,
    "prod": "moisturizer",
    "brand": "First Aid Beauty",
    "description": "for dry skin",
    "url": "https://www.firstaidbeauty.com/skin-care-products/moisturizers/ultra-repair-face-moisturizer",
    "image_url": "https://cdn11.bigcommerce.com/s-65cfp7jfhx/images/stencil/960w/products/127/3294/1._LEAD_RENDERING__49457.1645198838.jpg?c=1%20960w"
}, {
    "prod_id": 9,
    "prod": "makeup sponge",
    "brand": "Sephora",
    "description": "super-soft, exclusive, latex-free foam",
    "url": "https://www.sephora.com/product/beautyblender-P228913",
    "image_url": "https://www.sephora.com/productimages/sku/s2230829-main-zoom.jpg?imwidth=315"
}]

# TODO: assume we always don't have customer order data
customer_order_data = []

product_data_df = pd.DataFrame(product_data)
product_data_df['combined'] = product_data_df.apply(
    lambda row: f"{row['brand']}, {row['prod']}, {row['description']}", axis=1)
product_data_df['text_embedding'] = product_data_df.combined.apply(
    lambda x: get_embedding_with_backoff(text=x, engine='text-embedding-ada-002'))

customer_order_df = pd.DataFrame(customer_order_data)
customer_order_df['combined'] = customer_order_df.apply(
    lambda row: f"{row['brand']}, {row['prod']}, {row['description']}", axis=1)
customer_order_df['text_embedding'] = customer_order_df.combined.apply(
    lambda x: get_embedding_with_backoff(text=x, engine='text-embedding-ada-002'))


@app.route("/", methods=["GET"])
def home():
    return "Welcome to the StyleBot Flask App!"


@app.route("/recommend-product", methods=["POST"])
def recommend_product():
    data = request.get_json()
    # customer_input = data.get("customer_input")
    customer_input = "Hi! Can you recommend a good moisturizer for me?"

    if not customer_input:
        return jsonify({"error": "Please provide a prompt"}), 400

    try:
        response = create_embedding_with_backoff(
            input=customer_input,
            model="text-embedding-ada-002"
        )
        embeddings_customer_question = response['data'][0]['embedding']

        customer_order_df['search_purchase_history'] = customer_order_df.text_embedding.apply(
            lambda x: cosine_similarity_with_backoff(x, embeddings_customer_question))
        customer_order_df = customer_order_df.sort_values(
            'search_purchase_history', ascending=False)

        product_data_df['search_products'] = product_data_df.text_embedding.apply(
            lambda x: cosine_similarity_with_backoff(x, embeddings_customer_question))
        product_data_df = product_data_df.sort_values(
            'search_products', ascending=False)

        top_3_purchases_df = customer_order_df.head(3)
        top_3_products_df = product_data_df.head(3)

        message_objects = []

        def append_message_objects(role, content):
            message_objects.append({"role": role, "content": content})

        append_message_objects(
            Role.system.name, "Hey there. I'm your shopping co-pilot. What can I help you find today? Please tell me what you're looking for?")
        append_message_objects(Role.user.name, customer_input)
        prev_purchases = ". ".join(
            [f"{row['combined']}" for index, row in top_3_purchases_df.iterrows()])
        append_message_objects(
            Role.user.name, f"Here're my latest product orders: {prev_purchases}")
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

        response = chat_completion_with_backoff(
            model="gpt-3.5-turbo",
            messages=message_objects
        )
        generated_text = response.choices[0].message['content'].strip()
        return jsonify({"generated_text": generated_text, "recommend_products": top_3_products_df.to_json(orient="records")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
