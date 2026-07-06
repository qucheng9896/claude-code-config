package com.wygl.controller;

import com.wygl.pojo.Notice;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/notice")
public class NoticeController extends BaseController<Notice> {
}
