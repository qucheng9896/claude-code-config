package com.wygl.controller;

import com.wygl.pojo.Building;
import com.wygl.result.Result;
import com.wygl.service.IBuildingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/building")
public class BuildingController extends BaseController<Building> {

    @Autowired
    private IBuildingService buildingService;

    @GetMapping("/stats")
    public Result stats() {
        return new Result(true, "查询成功", buildingService.getHouseStats());
    }
}
