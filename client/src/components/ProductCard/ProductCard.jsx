import React from "react";

import "./ProductCard.css";

const ProductCard = (props) => {
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
