package com.wygl.service.impl;

import com.wygl.dao.*;
import com.wygl.pojo.AiRemindLog;
import com.wygl.pojo.House;
import com.wygl.pojo.Payment;
import com.wygl.pojo.RepairOrder;
import com.wygl.service.IDashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class DashboardServiceImpl implements IDashboardService {

    @Autowired
    private OwnerDao ownerDao;
    @Autowired
    private HouseDao houseDao;
    @Autowired
    private PaymentDao paymentDao;
    @Autowired
    private RepairOrderDao repairOrderDao;
    @Autowired
    private AiRemindLogDao aiRemindLogDao;

    @Override
    public Map<String, Object> getOverview() {
        Map<String, Object> data = new HashMap<>();

        int ownerCount = ownerDao.findPage(null, null, null).size();
        List<House> houses = houseDao.findPage(null, null, null);
        int houseCount = houses.size();
        int vacantCount = (int) houses.stream().filter(h -> h.getStatus() != null && h.getStatus() == 0).count();

        data.put("ownerCount", ownerCount);
        data.put("houseCount", houseCount);
        data.put("occupiedCount", houseCount - vacantCount);
        data.put("vacantCount", vacantCount);

        List<Payment> payments = paymentDao.findPage(null, null, null);
        BigDecimal totalPaid = payments.stream()
                .filter(p -> p.getPayStatus() != null && (p.getPayStatus() == 1 || p.getPayStatus() == 2))
                .map(p -> p.getAmount() != null ? p.getAmount() : BigDecimal.ZERO)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        BigDecimal totalAmount = payments.stream()
                .map(p -> p.getAmount() != null ? p.getAmount() : BigDecimal.ZERO)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        data.put("totalPaidAmount", totalPaid);
        data.put("totalAmount", totalAmount);
        data.put("paymentRate", totalAmount.compareTo(BigDecimal.ZERO) > 0
                ? totalPaid.multiply(new BigDecimal("100")).divide(totalAmount, 1, RoundingMode.HALF_UP) + "%"
                : "0%");

        return data;
    }

    @Override
    public Map<String, Object> getPaymentStats() {
        Map<String, Object> data = new HashMap<>();

        List<Payment> payments = paymentDao.findPage(null, null, null);
        BigDecimal totalPaid = payments.stream()
                .filter(p -> p.getPayStatus() != null && (p.getPayStatus() == 1 || p.getPayStatus() == 2))
                .map(p -> p.getAmount() != null ? p.getAmount() : BigDecimal.ZERO)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        BigDecimal totalOverdue = payments.stream()
                .filter(p -> p.getPayStatus() != null && (p.getPayStatus() == 0 || p.getPayStatus() == 3))
                .map(p -> p.getAmount() != null ? p.getAmount() : BigDecimal.ZERO)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        data.put("totalPaidAmount", totalPaid);
        data.put("totalOverdueAmount", totalOverdue);
        data.put("totalBills", payments.size());

        return data;
    }

    @Override
    public Map<String, Object> getRepairStats() {
        Map<String, Object> data = new HashMap<>();

        List<RepairOrder> orders = repairOrderDao.findPage(null, null, null);
        long totalOrders = orders.size();
        long completedOrders = orders.stream()
                .filter(r -> r.getStatus() != null && (r.getStatus() == 2 || r.getStatus() == 3))
                .count();

        long totalEvaluated = orders.stream()
                .filter(r -> r.getEvaluation() != null && r.getEvaluation() > 0).count();
        long satisfied = orders.stream()
                .filter(r -> r.getEvaluation() != null && r.getEvaluation() >= 4).count();

        long avgHours = (long) orders.stream()
                .filter(r -> r.getDispatchTime() != null && r.getCreateTime() != null)
                .mapToLong(r -> java.time.Duration.between(
                        r.getCreateTime().toInstant().atZone(java.time.ZoneId.systemDefault()).toLocalDateTime(),
                        r.getDispatchTime().toInstant().atZone(java.time.ZoneId.systemDefault()).toLocalDateTime()
                ).toHours())
                .average().orElse(0);

        data.put("totalOrders", totalOrders);
        data.put("completedOrders", completedOrders);
        data.put("avgResponseTime", avgHours > 0 ? avgHours + "h" : "-");
        data.put("satisfactionRate", totalEvaluated > 0
                ? Math.round(satisfied * 100.0 / totalEvaluated) + "%" : "-");

        return data;
    }

    @Override
    public Map<String, Object> getAiStats() {
        Map<String, Object> data = new HashMap<>();
        try {
            List<AiRemindLog> logs = aiRemindLogDao.findPending();
            data.put("totalReminds", logs != null ? logs.size() : 0);
            data.put("sentReminds", 0);
            data.put("successRate", "0%");
        } catch (Exception e) {
            data.put("totalReminds", 0);
            data.put("sentReminds", 0);
            data.put("successRate", "0%");
        }
        data.put("recoveredAmount", new BigDecimal("0"));
        return data;
    }
}
