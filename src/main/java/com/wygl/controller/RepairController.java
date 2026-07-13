package com.wygl.controller;

import com.wygl.pojo.RepairOrder;
import com.wygl.result.Result;
import com.wygl.service.IRepairService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/repair")
public class RepairController extends BaseController<RepairOrder> {

    @Autowired
    private IRepairService repairService;

    @PutMapping("/dispatch/{id}")
    public Result dispatch(@PathVariable Integer id,
                           @RequestParam Integer workerId,
                           @RequestParam String workerName) {
        return repairService.dispatch(id, workerId, workerName);
    }

    @PutMapping("/evaluate/{id}")
    public Result evaluate(@PathVariable Integer id,
                           @RequestParam Integer evaluation) {
        return repairService.evaluate(id, evaluation);
    }
}
