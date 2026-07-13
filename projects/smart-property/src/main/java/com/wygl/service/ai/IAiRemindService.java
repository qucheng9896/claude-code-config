package com.wygl.service.ai;

import com.wygl.pojo.Payment;
import java.util.List;
import java.util.Map;

/**
 * AI催缴服务接口
 * 封装大模型调用：生成个性化催缴消息
 */
public interface IAiRemindService {

    /**
     * 为指定业主生成AI催缴消息
     * @param ownerId 业主ID
     * @param overduePayments 逾期账单列表
     * @return AI生成的催缴消息文本
     */
    String generateRemindMessage(Integer ownerId, List<Payment> overduePayments);

    /**
     * 批量生成催缴消息（预览模式）
     * @return key=ownerId, value=催缴消息
     */
    Map<Integer, String> batchGenerateRemindMessages();
}
