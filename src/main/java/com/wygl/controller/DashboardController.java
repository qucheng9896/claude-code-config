package com.wygl.controller;

import com.wygl.result.Result;
import com.wygl.service.IDashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/dashboard")
public class DashboardController {

    @Autowired
    private IDashboardService dashboardService;

    @GetMapping("/overview")
    public Result overview() {
        return new Result(true, "查询成功", dashboardService.getOverview());
    }

    @GetMapping("/payment")
    public Result payment() {
        return new Result(true, "查询成功", dashboardService.getPaymentStats());
    }

    @GetMapping("/repair")
    public Result repair() {
        return new Result(true, "查询成功", dashboardService.getRepairStats());
    }

    @GetMapping("/ai")
    public Result aiStats() {
        return new Result(true, "查询成功", dashboardService.getAiStats());
    }
}
