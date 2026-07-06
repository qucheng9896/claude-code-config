package com.wygl.service.impl;

import com.wygl.dao.ParkingDao;
import com.wygl.pojo.Parking;
import com.wygl.service.IParkingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ParkingServiceImpl extends BaseServiceImpl<Parking> implements IParkingService {

    @Autowired
    private ParkingDao parkingDao;
}
