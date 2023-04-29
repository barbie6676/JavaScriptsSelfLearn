import React from "react";
import { createChatBotMessage } from "react-chatbot-kit";

import Options from "../components/Options/Options";

const config = {
  botName: "StyleBot",
  initialMessages: [
    createChatBotMessage(`Hey there. I'm your shopping co-pilot. What can I help you find today? Please tell me what you're looking for?`),
  ],
  widgets: [
    {
      widgetName: "options",
      widgetFunc: (props) => <Options {...props} />,
      mapStateToProps: [
        "messages",
      ],
    },
  ],
};

export default config;
