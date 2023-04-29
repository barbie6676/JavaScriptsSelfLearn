class ActionProvider {
  constructor(createChatBotMessage, setStateFunc) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
  }

  handleGenerateResponse = (message) => {
    const botMessage = this.createChatBotMessage(
      "Hello friend.",
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
