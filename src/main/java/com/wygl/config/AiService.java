package com.wygl.config;

import okhttp3.*;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.node.ObjectNode;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

/**
 * AI大模型服务 — 支持切换到真实API调用
 * 默认使用模拟回复，配置API_KEY后自动切换
 */
public class AiService {

    private static final String API_URL = "https://api.deepseek.com/v1/chat/completions";
    private static final String API_KEY = "";  // 填入你的 DeepSeek API Key
    private static final String MODEL = "deepseek-chat";

    private static final OkHttpClient client = new OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .build();

    private static final ObjectMapper mapper = new ObjectMapper();

    public static String generateRemindMessage(String prompt) {
        if (API_KEY == null || API_KEY.isEmpty()) {
            return simulateReply(prompt);
        }
        return callDeepSeek(prompt);
    }

    private static String callDeepSeek(String prompt) {
        try {
            ObjectNode body = mapper.createObjectNode();
            body.put("model", MODEL);
            body.putArray("messages")
                .addObject().put("role", "system").put("content", "你是物业管理AI助手，生成友好催缴通知，不超过100字。")
                .addObject().put("role", "user").put("content", prompt);
            body.put("max_tokens", 200);
            body.put("temperature", 0.7);

            Request request = new Request.Builder()
                    .url(API_URL)
                    .addHeader("Authorization", "Bearer " + API_KEY)
                    .addHeader("Content-Type", "application/json")
                    .post(RequestBody.create(body.toString(), MediaType.parse("application/json")))
                    .build();

            try (Response response = client.newCall(request).execute()) {
                if (!response.isSuccessful()) return simulateReply(prompt);
                JsonNode root = mapper.readTree(response.body().string());
                return root.path("choices").get(0).path("message").path("content").asText();
            }
        } catch (IOException e) {
            return simulateReply(prompt);
        }
    }

    private static String simulateReply(String prompt) {
        return "您好，您的物业费账单逾期未缴，请尽快登录系统或到物业处缴纳，以免影响您的信用记录。如有疑问请联系物业客服。感谢配合！";
    }
}
