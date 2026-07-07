package com.wygl.dao;

import com.wygl.pojo.House;
import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.Map;

public interface HouseDao extends BaseDao<House> {

    int countByBuildingRoom(@Param("buildingId") Integer buildingId, @Param("roomNo") String roomNo);

    int countUnpaidByHouseId(@Param("houseId") Integer houseId);

    List<House> findByStatus(@Param("status") Integer status);

    Map<String, Object> selectStats();
}
