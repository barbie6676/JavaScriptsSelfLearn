import React, { useEffect } from 'react';
import { createClientMessage } from "react-chatbot-kit";
import { startRecommendProducts, recommendProductsStream } from "../utils/gatewayAPIs";

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  useEffect(() => {
    const sse = recommendProductsStream();

    sse.addEventListener(
      "recommend",
      (event) => {
        const message = JSON.parse(event.data);
        if (message.recommend_products !== undefined) {
          const botMessage = createChatBotMessage("", {
            widget: "options",
            payload: {
              recommendProducts: JSON.parse(message.recommend_products),
              originalMessage: message,
            },
          });
          setState((prevState) => ({
            ...prevState,
            messages: [...prevState.messages, botMessage],
          }));
        }
      },
      false
    );

    sse.addEventListener(
      "text",
      (event) => {
        const message = JSON.parse(event.data);
        if (message.text.content !== undefined) {
          setState((prevState) => {
            const messages = prevState.messages;
            const lastMessage = messages[messages.length - 1];
            if (lastMessage.message.endsWith(message.text.content)) {
              return prevState;
            }
            lastMessage.message = lastMessage.message + message.text.content;
            messages[messages.length - 1] = lastMessage;
            return {
              ...prevState,
              messages,
            };
          });
        }
      },
      false
    );

    sse.onerror = (err) => {
      console.error(err);
      if (sse !== undefined && sse !== null) {
        sse.close();
      }
    };

    return () => {
      sse.close();
    };
  }, [createChatBotMessage, setState]);

  const handleGenerateResponse = async (message, sessionId, regenerate) => {
    if (regenerate) {
      const clientMessage = createClientMessage(message);
      setState((prevState) => ({
        ...prevState,
        messages: [...prevState.messages, clientMessage],
      }));
    }
    startRecommendProducts(message, sessionId);
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleGenerateResponse
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;
