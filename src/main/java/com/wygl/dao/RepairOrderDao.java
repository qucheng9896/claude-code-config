package com.wygl.dao;

import com.wygl.pojo.RepairOrder;
import org.apache.ibatis.annotations.Param;

public interface RepairOrderDao extends BaseDao<RepairOrder> {

    int dispatch(@Param("id") Integer id, @Param("workerId") Integer workerId, @Param("workerName") String workerName);

    int evaluate(@Param("id") Integer id, @Param("evaluation") Integer evaluation);
}
