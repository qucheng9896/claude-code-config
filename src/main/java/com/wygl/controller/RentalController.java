package com.wygl.controller;

import com.wygl.pojo.Rental;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/rental")
public class RentalController extends BaseController<Rental> {
}
