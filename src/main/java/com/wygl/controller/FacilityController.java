package com.wygl.controller;

import com.wygl.pojo.Facility;
import com.wygl.result.Result;
import com.wygl.service.IFacilityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/facility")
public class FacilityController extends BaseController<Facility> {

    @Autowired
    private IFacilityService facilityService;

    @GetMapping("/stats")
    public Result stats() {
        return new Result(true, "查询成功", facilityService.getStats());
    }
}
