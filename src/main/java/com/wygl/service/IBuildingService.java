package com.wygl.service;

import com.wygl.pojo.Building;

import java.util.Map;

public interface IBuildingService extends BaseService<Building> {

    Map<String, Object> getHouseStats();
}
