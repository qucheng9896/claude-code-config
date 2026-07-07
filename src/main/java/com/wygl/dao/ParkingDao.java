package com.wygl.dao;

import com.wygl.pojo.Parking;
import org.apache.ibatis.annotations.Param;

import java.util.Map;

public interface ParkingDao extends BaseDao<Parking> {

    int countByParkingNo(@Param("parkingNo") String parkingNo);

    Map<String, Object> selectStats();
}
