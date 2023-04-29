import React, { useEffect, useRef, useState } from "react";

import "./Options.css";

const Options = (props) => {
  const [userMessage, setUserMessage] = useState(undefined);
  const [products, setProducts] = useState([]);
  const myRef = useRef(null);

  useEffect(() => {
    const domNode = myRef.current.previousSibling;
    const reactInternalInstanceKey = Object.keys(domNode).find(key => key.startsWith('__reactInternalInstance'));
    const reactInternalInstance = domNode[reactInternalInstanceKey];
    const memoizedProps = reactInternalInstance.memoizedProps.children[0]._owner.memoizedProps;
    setUserMessage(memoizedProps.payload.originalMessage);
    setProducts(memoizedProps.payload.recommendProducts);
  }, []);

  const options = [
    { 
      text: "Regenerate", 
      handler: () => props.actionProvider.handleGenerateResponse(userMessage, true), 
      id: 1
    },
    { 
      text: "Try On", 
      handler: () => {}, 
      id: 2 
    },
  ];

  const buttonsMarkup = options.map((option) => (
    <button key={option.id} onClick={option.handler} className="option-button">
      {option.text}
    </button>
  ));

  return <div className="options-container" ref={myRef}>{buttonsMarkup}</div>;
};

export default Options;
