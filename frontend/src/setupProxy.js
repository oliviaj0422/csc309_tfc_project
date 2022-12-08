
const {createProxyMiddleware} = require('http-proxy-middleware')
 
module.exports = function (app) {
    app.use(
        createProxyMiddleware(
            '/studios', 
            {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                pathRewrite: {
                    '^/studios': '/studios'
                }
            }
        )
    )
}