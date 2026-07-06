package com.wygl.service;

import com.wygl.dto.BillGenerateDTO;
import com.wygl.pojo.Payment;

import java.util.List;

public interface IPaymentService extends BaseService<Payment> {

    List<Payment> findOverduePayments();

    List<Payment> findOverdueByOwnerId(Integer ownerId);

    void generateBills(BillGenerateDTO dto);

    void pay(Integer id);

    void confirm(Integer id, Integer operatorId);
}
