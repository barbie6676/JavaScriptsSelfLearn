import axios from "axios";

const baseURL = "http://127.0.0.1:5000/";
// const baseURL = "https://stylebot.tryforma.com/server/";

const axiosInstance = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 20000,
  validateStatus: function (status) {
    return status >= 200 && status < 500; // default
  },
});

export const recommendProductsStream = () => {
  return new EventSource(baseURL + "stream");
};

export const startRecommendProducts = (customerInput, sessionId) => {
  try {
    axiosInstance.get(`recommend-product`, {
      params: {
        customer_input: customerInput,
        session_id: sessionId,
      },
    });
  } catch (ex) {
    console.error("failed to get recommended product " + ex);
  }
};
