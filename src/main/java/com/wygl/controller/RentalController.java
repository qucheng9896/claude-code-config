package com.wygl.controller;

import com.wygl.pojo.Rental;
import com.wygl.result.Result;
import com.wygl.service.IRentalService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/rental")
public class RentalController extends BaseController<Rental> {

    @Autowired
    private IRentalService rentalService;

    @GetMapping("/expire")
    public Result expire(@RequestParam(defaultValue = "30") Integer days) {
        List<Rental> list = rentalService.findExpiring(days);
        return new Result(true, list);
    }
}
