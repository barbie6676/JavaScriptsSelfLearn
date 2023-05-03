import { getRecommendProducts } from "../utils/gatewayAPIs";

class ActionProvider {
  constructor(createChatBotMessage, setStateFunc, createClientMessage) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
    this.createClientMessage = createClientMessage;
  }

  handleGenerateResponse = async (message, sessionId, regenerate) => {
    if (regenerate) {
      const clientMessage = this.createClientMessage(message);
      this.addMessageToState(clientMessage);
    }
    const response = await getRecommendProducts(message, sessionId);
    const botMessage = this.createChatBotMessage(response.text, {
      widget: "options",
      payload: {
        recommendProducts: JSON.parse(response["recommend_products"]),
        originalMessage: message,
      },
    });
    this.addMessageToState(botMessage);
  };

  addMessageToState = (message) => {
    this.setState((prevState) => ({
      ...prevState,
      messages: [...prevState.messages, message],
    }));
  };
}

export default ActionProvider;
