package com.wygl.service.impl;

import com.wygl.dao.RepairOrderDao;
import com.wygl.pojo.RepairOrder;
import com.wygl.service.IRepairService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RepairServiceImpl extends BaseServiceImpl<RepairOrder> implements IRepairService {

    @Autowired
    private RepairOrderDao repairOrderDao;
}
