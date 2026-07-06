package com.wygl.controller;

import com.wygl.pojo.Parking;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/parking")
public class ParkingController extends BaseController<Parking> {
}
