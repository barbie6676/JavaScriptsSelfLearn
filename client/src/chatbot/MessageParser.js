class MessageParser {
  constructor(actionProvider) {
    this.actionProvider = actionProvider;
  }

  parse(message) {
    this.actionProvider.handleGenerateResponse(message, false);
  }
}

export default MessageParser;
