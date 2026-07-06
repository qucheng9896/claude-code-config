package com.wygl.service.impl;

import com.wygl.dao.RentalDao;
import com.wygl.pojo.Rental;
import com.wygl.service.IRentalService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RentalServiceImpl extends BaseServiceImpl<Rental> implements IRentalService {

    @Autowired
    private RentalDao rentalDao;
}
