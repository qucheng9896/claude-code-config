package com.wygl.config;

/**
 * AI服务配置
 * 实际部署时修改此处的API地址和密钥
 */
public class AiConfig {

    /**
     * 是否启用真实AI调用
     * true = 调用真实大模型API（需配置 API_KEY）
     * false = 使用本地模拟模板（演示/开发模式）
     */
    public static final boolean AI_ENABLED = false;

    /**
     * 真实AI服务地址（示例：OpenAI / 通义千问 / DeepSeek）
     */
    public static final String AI_API_URL = "https://api.deepseek.com/v1/chat/completions";

    /**
     * AI API密钥（生产环境应从环境变量或配置中心读取）
     */
    public static final String AI_API_KEY = "your-api-key-here";

    /**
     * AI模型名称
     */
    public static final String AI_MODEL = "deepseek-chat";

    /**
     * AI调用超时（秒）
     */
    public static final int AI_TIMEOUT = 30;
}
