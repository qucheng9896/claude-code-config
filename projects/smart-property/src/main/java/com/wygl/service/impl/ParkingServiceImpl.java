package com.wygl.service.impl;

import com.wygl.constant.MessageConstant;
import com.wygl.dao.ParkingDao;
import com.wygl.exception.BusinessException;
import com.wygl.pojo.Parking;
import com.wygl.service.IParkingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Map;

@Service
public class ParkingServiceImpl extends BaseServiceImpl<Parking> implements IParkingService {

    @Autowired
    private ParkingDao parkingDao;

    @Override
    public void add(Parking parking) {
        if (parkingDao.countByParkingNo(parking.getParkingNo()) > 0) {
            throw new BusinessException(MessageConstant.PARKING_NO_EXISTS);
        }
        parkingDao.insert(parking);
    }

    @Override
    public Map<String, Object> getStats() {
        return parkingDao.selectStats();
    }
}
