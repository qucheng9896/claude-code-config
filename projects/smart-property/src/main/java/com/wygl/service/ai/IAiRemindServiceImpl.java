package com.wygl.service.ai;

import com.wygl.dao.PaymentDao;
import com.wygl.pojo.Owner;
import com.wygl.pojo.Payment;
import com.wygl.dao.OwnerDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class IAiRemindServiceImpl implements IAiRemindService {

    @Autowired
    private PaymentDao paymentDao;
    @Autowired
    private OwnerDao ownerDao;

    /**
     * AI催缴消息模板（模拟大模型输出）
     * 实际部署时替换为：调用 OpenAPI / 通义千问 / DeepSeek 等 API
     */
    @Override
    public String generateRemindMessage(Integer ownerId, List<Payment> overduePayments) {
        Owner owner = ownerDao.findById(ownerId);
        if (owner == null || overduePayments == null || overduePayments.isEmpty()) {
            return null;
        }

        // 汇总逾期信息
        double totalAmount = overduePayments.stream()
                .mapToDouble(p -> p.getAmount().doubleValue()).sum();
        long maxOverdueDays = overduePayments.stream()
                .mapToLong(p -> ChronoUnit.DAYS.between(
                        p.getDueDate().toInstant().atZone(java.time.ZoneId.systemDefault()).toLocalDate(), LocalDate.now()))
                .max().orElse(0);

        StringBuilder detail = new StringBuilder();
        for (Payment p : overduePayments) {
            detail.append(String.format("- %s %s: ¥%.2f（周期: %s）\n",
                    p.getFeeType(), p.getHouseId(), p.getAmount(), p.getPeriod()));
        }

        // 构造 prompt（实际部署时发送给大模型）
        String prompt = String.format(
            "你是一个物业管理系统的AI助手。请为以下业主生成一条友好但明确的催缴通知消息：\n" +
            "业主姓名：%s\n" +
            "逾期总金额：¥%.2f\n" +
            "最长逾期天数：%d天\n" +
            "逾期账单明细：\n%s\n" +
            "要求：语气礼貌但正式，说明金额和逾期天数，提醒尽快缴纳，不超过100字。",
            owner.getName(), totalAmount, maxOverdueDays, detail.toString()
        );

        // ========== 模拟AI输出（实际使用时替换为API调用） ==========
        String aiMessage = simulateAiCall(owner.getName(), totalAmount, maxOverdueDays, detail.toString());
        // ===========================================================

        return aiMessage;
    }

    @Override
    public Map<Integer, String> batchGenerateRemindMessages() {
        Map<Integer, String> result = new HashMap<>();
        // 查询所有逾期账单
        List<Payment> overdueList = paymentDao.findByStatus(3); // 3=逾期
        // 按业主分组
        Map<Integer, List<Payment>> grouped = new HashMap<>();
        for (Payment p : overdueList) {
            grouped.computeIfAbsent(p.getOwnerId(), k -> new java.util.ArrayList<>()).add(p);
        }
        // 逐个生成催缴消息
        for (Map.Entry<Integer, List<Payment>> entry : grouped.entrySet()) {
            String msg = generateRemindMessage(entry.getKey(), entry.getValue());
            if (msg != null) {
                result.put(entry.getKey(), msg);
            }
        }
        return result;
    }

    /**
     * 模拟AI调用（实际部署时移除，替换为真实大模型HTTP调用）
     */
    private String simulateAiCall(String name, double amount, long days, String detail) {
        return String.format(
            "%s 您好，您有物业费账单逾期未缴，总金额 ¥%.2f，已逾期 %d 天。请尽快登录系统或到物业处缴纳，" +
            "以免影响您的信用记录。如有疑问请联系物业客服。感谢配合！",
            name, amount, days
        );
    }
}
