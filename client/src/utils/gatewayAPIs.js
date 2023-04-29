import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000/',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 20000,
    validateStatus: function (status) {
        return status >= 200 && status < 500; // default
    }
});

export const getRecommendProducts = async (customerInput) => {
    try {
        const res = await axiosInstance.post(`recommend-product`, {
            'customer_input': customerInput
        });
        return res.data;
    } catch (ex) {
        console.error('failed to get recommended product');
    }
};
