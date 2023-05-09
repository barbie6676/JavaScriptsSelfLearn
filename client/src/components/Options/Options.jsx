import React from "react";

import "./Options.css";
import ProductCard from "../ProductCard/ProductCard";

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
      handler: () => {},
      id: 2,
    },
  ];

  const buttonsMarkup = options.map((option) => (
    <button key={option.id} onClick={option.handler} className="option-button">
      {option.text}
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
