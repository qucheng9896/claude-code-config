package com.wygl.service.impl;

import com.wygl.dao.BuildingDao;
import com.wygl.pojo.Building;
import com.wygl.service.IBuildingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class BuildingServiceImpl extends BaseServiceImpl<Building> implements IBuildingService {

    @Autowired
    private BuildingDao buildingDao;

    @Override
    public Map<String, Object> getHouseStats() {
        List<Map<String, Object>> stats = buildingDao.selectHouseStats();
        int totalHouses = buildingDao.countAllHouses();
        int occupiedHouses = buildingDao.countOccupiedHouses();
        Map<String, Object> result = new HashMap<>();
        result.put("buildingStats", stats);
        result.put("totalHouses", totalHouses);
        result.put("occupiedHouses", occupiedHouses);
        return result;
    }
}
