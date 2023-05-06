import React from 'react';

const MessageParser = ({ children, actions }) => {
  const parse = (child, message) => {
    const state = child.props.state;
    actions.handleGenerateResponse(message, state.sessionId, false);
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          parse: (message) => parse(child, message),
          actions,
        });
      })}
    </div>
  );
};

export default MessageParser;
