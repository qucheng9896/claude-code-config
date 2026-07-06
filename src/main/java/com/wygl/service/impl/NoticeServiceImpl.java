package com.wygl.service.impl;

import com.wygl.dao.NoticeDao;
import com.wygl.pojo.Notice;
import com.wygl.service.INoticeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class NoticeServiceImpl extends BaseServiceImpl<Notice> implements INoticeService {

    @Autowired
    private NoticeDao noticeDao;
}
