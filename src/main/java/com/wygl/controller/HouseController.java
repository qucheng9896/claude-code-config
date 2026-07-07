package com.wygl.controller;

import com.wygl.pojo.House;
import com.wygl.result.Result;
import com.wygl.service.IHouseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/house")
public class HouseController extends BaseController<House> {

    @Autowired
    private IHouseService houseService;

    @GetMapping("/vacant")
    public Result vacant() {
        List<House> list = houseService.findVacant();
        return new Result(true, "查询成功", list);
    }

    @GetMapping("/stats")
    public Result stats() {
        return new Result(true, "查询成功", houseService.getStats());
    }
}
