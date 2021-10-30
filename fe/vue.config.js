module.exports = {
  devServer: {
    host: "localhost",
    port: 8084,
    proxy: {
      "/api": {
        target: "http://10.128.207.3:5000/",
        // 允许跨域
        changeOrigin: true,
      },
    },
  },
};
