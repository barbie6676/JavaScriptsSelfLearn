import React from "react";

import "./ProductCard.css";

const ProductCard = (props) => {

  const formatter = new Intl.NumberFormat(undefined, {
    style: "currency",
    currency: props.sale_price_currency,
  })
  const formattedPrice = formatter.format(props.sale_price_micro_amount / 1000000);

  return (
    <div
      className="container"
      onClick={() => {
        window.open(props.link, "_blank");
      }}
    >
      <div className="card">
        <div className="image">
          <img src={props.image_link} alt="product_image" />
        </div>
        <div className="text">
          <div className="description">
            <p style={{ margin: "5px" }}>{props.brand}</p>
            <p style={{ margin: "5px" }}>{props.title}</p>
            <p style={{ margin: "5px" }}>{formattedPrice}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
