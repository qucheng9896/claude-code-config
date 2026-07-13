package com.wygl.dao;

import com.wygl.pojo.Building;
import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.Map;

public interface BuildingDao extends BaseDao<Building> {

    List<Map<String, Object>> selectHouseStats();

    int countAllHouses();

    int countOccupiedHouses();
}
