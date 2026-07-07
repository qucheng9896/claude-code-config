package com.wygl.controller;

import com.wygl.pojo.Parking;
import com.wygl.result.Result;
import com.wygl.service.IParkingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/parking")
public class ParkingController extends BaseController<Parking> {

    @Autowired
    private IParkingService parkingService;

    @GetMapping("/stats")
    public Result stats() {
        return new Result(true, "查询成功", parkingService.getStats());
    }
}
