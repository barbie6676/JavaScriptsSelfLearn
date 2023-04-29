import React, { useEffect, useState } from "react";

import "./Options.css";

const Options = (props) => {
  const [userMessage, setUserMessage] = useState(undefined);

  useEffect(() => {
    const messages = props.messages;
    const lastUserMessage = messages.findLast(message => message.type === 'user');
    setUserMessage(lastUserMessage.message);
  }, []);

  const options = [
    { 
      text: "Regenerate", 
      handler: () => props.actionProvider.handleGenerateResponse(userMessage), 
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

  return <div className="options-container">{buttonsMarkup}</div>;
};

export default Options;
