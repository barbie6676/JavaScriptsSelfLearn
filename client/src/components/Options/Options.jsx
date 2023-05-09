import React from "react";

import "./Options.css";
import ProductCard from "../ProductCard/ProductCard";
import { generatePdf } from "../../utils/gatewayAPIs";

async function sendHTMLtoServer(button) {
  if (button.classList.contains('option-button__text')) {
    button = button.parentNode;
  }
  button.classList.add("option-button--loading");
  const innerHTML = document.querySelector('.react-chatbot-kit-chat-message-container').innerHTML;
  await generatePdf(innerHTML);
  button.classList.remove("option-button--loading");
}

const Options = (props) => {
  const sessionId = props.sessionId;
  const userMessage = props.payload.originalMessage;
  const products = props.payload.recommendProducts;

  const options = [
    {
      text: "Regenerate",
      handler: () =>
        props.actionProvider.handleGenerateResponse(userMessage, sessionId, true),
      id: 1,
    },
    {
      text: "Export",
      handler: (event) => {
        sendHTMLtoServer(event.target)
      },
      id: 2,
    },
  ];

  const buttonsMarkup = options.map((option) => (
    <button key={option.id} onClick={option.handler} className="option-button">
      <span className="option-button__text">{option.text}</span>
    </button>
  ));

  const productCards = products.map((product) => (
    <ProductCard key={product.snap_product_id} {...product} />
  ));

  return (
    <div className="results-container">
      <div className="products-container">{productCards}</div>
      <div className="options-container">{buttonsMarkup}</div>
    </div>
  );
};

export default Options;
