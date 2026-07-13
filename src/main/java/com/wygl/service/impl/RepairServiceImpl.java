package com.wygl.service.impl;

import com.wygl.constant.MessageConstant;
import com.wygl.dao.RepairOrderDao;
import com.wygl.pojo.RepairOrder;
import com.wygl.result.Result;
import com.wygl.service.IRepairService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RepairServiceImpl extends BaseServiceImpl<RepairOrder> implements IRepairService {

    @Autowired
    private RepairOrderDao repairOrderDao;

    @Override
    public Result dispatch(Integer id, Integer workerId, String workerName) {
        RepairOrder order = repairOrderDao.findById(id);
        if (order == null) {
            return new Result(false, MessageConstant.REPAIR_NOT_FOUND);
        }
        if (order.getStatus() != null && order.getStatus() != 0) {
            return new Result(false, "工单状态不是待派单，无法派单");
        }
        repairOrderDao.dispatch(id, workerId, workerName);
        return new Result(true, "派单成功");
    }

    @Override
    public Result evaluate(Integer id, Integer evaluation) {
        RepairOrder order = repairOrderDao.findById(id);
        if (order == null) {
            return new Result(false, MessageConstant.REPAIR_NOT_FOUND);
        }
        if (order.getStatus() != null && order.getStatus() != 1) {
            return new Result(false, "工单未完成，无法评价");
        }
        repairOrderDao.evaluate(id, evaluation);
        return new Result(true, "评价成功");
    }
}
