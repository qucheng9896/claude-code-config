package com.wygl.service.impl;

import com.wygl.constant.MessageConstant;
import com.wygl.dao.HouseDao;
import com.wygl.dao.PaymentDao;
import com.wygl.dto.BillGenerateDTO;
import com.wygl.exception.BusinessException;
import com.wygl.pojo.House;
import com.wygl.pojo.Payment;
import com.wygl.service.IPaymentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class PaymentServiceImpl extends BaseServiceImpl<Payment> implements IPaymentService {

    @Autowired
    private PaymentDao paymentDao;

    @Autowired
    private HouseDao houseDao;

    @Override
    public List<Payment> findOverduePayments() {
        return paymentDao.findOverdue();
    }

    @Override
    public List<Payment> findOverdueByOwnerId(Integer ownerId) {
        return paymentDao.findOverdueByOwnerId(ownerId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void generateBills(BillGenerateDTO dto) {
        List<House> houses = houseDao.findByStatus(1);
        List<Payment> bills = new ArrayList<>();
        for (House house : houses) {
            if (paymentDao.countByHouseIdAndPeriod(house.getId(), dto.getPeriod()) > 0) {
                continue;
            }
            Payment payment = new Payment();
            payment.setBillNo("BILL" + System.currentTimeMillis() + UUID.randomUUID().toString().substring(0, 4));
            payment.setHouseId(house.getId());
            payment.setOwnerId(house.getOwnerId());
            payment.setTenantId(house.getTenantId());
            payment.setFeeType(dto.getFeeType());
            payment.setAmount(dto.getUnitPrice().multiply(house.getArea()));
            payment.setPeriod(dto.getPeriod());
            payment.setDueDate(LocalDate.parse(dto.getPeriod() + "-01").plusMonths(1).minusDays(1));
            payment.setPayStatus(0);
            bills.add(payment);
        }
        if (!bills.isEmpty()) {
            paymentDao.batchInsert(bills);
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void pay(Integer id) {
        Payment payment = paymentDao.findById(id);
        if (payment == null) {
            throw new BusinessException("账单不存在");
        }
        if (payment.getPayStatus() != 0 && payment.getPayStatus() != 3) {
            throw new BusinessException(MessageConstant.PAY_STATUS_ERROR);
        }
        paymentDao.updatePayStatus(id, 1, "微信");
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void confirm(Integer id, Integer operatorId) {
        Payment payment = paymentDao.findById(id);
        if (payment == null) {
            throw new BusinessException("账单不存在");
        }
        if (payment.getPayStatus() != 1) {
            throw new BusinessException(MessageConstant.PAY_STATUS_ERROR);
        }
        paymentDao.updateConfirmStatus(id);
    }

    @Override
    public void delete(Integer id) {
        Payment payment = paymentDao.findById(id);
        if (payment == null) {
            throw new BusinessException("账单不存在");
        }
        if (payment.getPayStatus() == 2) {
            throw new BusinessException(MessageConstant.BILL_CONFIRMED);
        }
        paymentDao.delete(id);
    }
}
