package com.wygl.service.impl;

import com.wygl.constant.MessageConstant;
import com.wygl.dao.HouseDao;
import com.wygl.exception.BusinessException;
import com.wygl.pojo.House;
import com.wygl.service.IHouseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HouseServiceImpl extends BaseServiceImpl<House> implements IHouseService {

    @Autowired
    private HouseDao houseDao;

    @Override
    public void add(House house) {
        if (houseDao.countByBuildingRoom(house.getBuildingId(), house.getRoomNo()) > 0) {
            throw new BusinessException(MessageConstant.HOUSE_EXISTS);
        }
        house.setStatus(1);
        houseDao.insert(house);
    }

    @Override
    public void delete(Integer id) {
        if (houseDao.countUnpaidByHouseId(id) > 0) {
            throw new BusinessException(MessageConstant.HOUSE_HAS_UNPAID);
        }
        houseDao.delete(id);
    }

    @Override
    public List<House> findVacant() {
        return houseDao.findByStatus(0);
    }
}
