import axios from "axios";

// const baseURL = "http://127.0.0.1:5000/";
// const streamURL = "http://127.0.0.1:5000/";
const baseURL = "https://stylebot.tryforma.com/server/";
const streamURL = "https://stylebot.tryforma.com/stream/";

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

export const recommendProductsStream = (sessionId) => {
  return new EventSource(streamURL + "stream?channel=" + sessionId);
};

export const startRecommendProducts = async (customerInput, sessionId) => {
  try {
    await axiosInstance.get(`recommend-product`, {
      params: {
        customer_input: customerInput,
        session_id: sessionId,
      },
    });
  } catch (ex) {
    console.error("failed to get recommended product " + ex);
  }
};

export const generatePdf = async (innerHTML) => {
  try {
    const response = await axiosInstance.post(
      `generate-pdf`,
      { html: innerHTML },
      { responseType: "blob" }
    );
    const blob = response.data;
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "output.pdf";
    link.click();
    URL.revokeObjectURL(url);
  } catch (ex) {
    console.error("Failed to generate PDF " + ex);
  }
};
