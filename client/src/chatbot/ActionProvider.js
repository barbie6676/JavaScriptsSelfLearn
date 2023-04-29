import { getRecommendProducts } from "../utils/gatewayAPIs";

class ActionProvider {
  constructor(createChatBotMessage, setStateFunc) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
  }

  handleGenerateResponse = async (message) => {
    const response = await getRecommendProducts(message);
    const botMessage = this.createChatBotMessage(
      response.text,
      {
        widget: "options",
      }
    );
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
