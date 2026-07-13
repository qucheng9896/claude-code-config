package com.wygl.service;

import com.wygl.pojo.RepairOrder;
import com.wygl.result.Result;

public interface IRepairService extends BaseService<RepairOrder> {

    Result dispatch(Integer id, Integer workerId, String workerName);

    Result evaluate(Integer id, Integer evaluation);
}
