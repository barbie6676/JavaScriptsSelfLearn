import React from "react";

import "./ProductCard.css";

const ProductCard = (props) => {
  return (
    <div className="container" onClick={() => {window.open(props.url, '_blank');}}>
      <div className="card">
        <div className="image">
          <img src={props.image_url} alt="product_image" />
        </div>
        <div className="text">
          <div className="description">
            <p>
              {[props.brand, props.prod, props.description].join(" ")}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
