package com.wygl.dao;

import com.wygl.dto.BillGenerateDTO;
import com.wygl.pojo.Payment;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface PaymentDao extends BaseDao<Payment> {

    List<Payment> findByStatus(@Param("status") Integer status);

    List<Payment> findOverdue();

    List<Payment> findOverdueByOwnerId(@Param("ownerId") Integer ownerId);

    int countByHouseIdAndPeriod(@Param("houseId") Integer houseId, @Param("period") String period);

    void batchInsert(@Param("list") List<Payment> list);

    void updatePayStatus(@Param("id") Integer id, @Param("payStatus") Integer payStatus, @Param("payMethod") String payMethod);

    void updateConfirmStatus(@Param("id") Integer id);
}
