package com.wygl.controller;

import com.wygl.pojo.Visitor;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/visitor")
public class VisitorController extends BaseController<Visitor> {
}
