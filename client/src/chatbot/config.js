import React from "react";
import { v4 as uuidv4 } from "uuid";
import { createChatBotMessage } from "react-chatbot-kit";

import Options from "../components/Options/Options";

const config = {
  botName: "StyleBot",
  initialMessages: [
    createChatBotMessage(
      `Hey there. I'm your shopping co-pilot. What can I help you find today? Please tell me what you're looking for?`
    ),
  ],
  state: {
    sessionId: uuidv4(),
  },
  widgets: [
    {
      widgetName: "options",
      widgetFunc: (props) => <Options {...props} />,
      mapStateToProps: ["messages", "sessionId"],
    },
  ],
};

export default config;
