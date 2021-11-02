module.exports = {
  devServer: {
    host: "localhost",
    port: 8084,
    proxy: {
      "/api": {
        target: "http://10.101.171.160:5000/",
        // 允许跨域
        changeOrigin: true,
      },
    },
  },
};
