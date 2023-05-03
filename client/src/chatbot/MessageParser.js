class MessageParser {
  constructor(actionProvider, state) {
    this.actionProvider = actionProvider;
    this.state = state;
  }

  parse(message) {
    this.actionProvider.handleGenerateResponse(message, this.state.sessionId, false);
  }
}

export default MessageParser;
