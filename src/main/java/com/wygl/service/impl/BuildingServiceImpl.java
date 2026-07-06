package com.wygl.service.impl;

import com.wygl.dao.BuildingDao;
import com.wygl.pojo.Building;
import com.wygl.service.IBuildingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class BuildingServiceImpl extends BaseServiceImpl<Building> implements IBuildingService {

    @Autowired
    private BuildingDao buildingDao;
}
