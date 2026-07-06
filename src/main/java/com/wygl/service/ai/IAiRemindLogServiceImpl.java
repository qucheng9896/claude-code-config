package com.wygl.service.ai;

import com.wygl.dao.AiRemindLogDao;
import com.wygl.dto.QueryPageBean;
import com.wygl.pojo.AiRemindLog;
import com.wygl.result.PageResult;
import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class IAiRemindLogServiceImpl implements IAiRemindLogService {

    @Autowired
    private AiRemindLogDao aiRemindLogDao;

    @Override
    public void saveRemindLog(AiRemindLog log) {
        aiRemindLogDao.insert(log);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void sendRemind(Integer logId, Integer operatorId) {
        aiRemindLogDao.updateSendStatus(logId, operatorId);
    }

    @Override
    public PageResult findPage(QueryPageBean queryPageBean) {
        if (queryPageBean.getQueryString() != null && "null".equals(queryPageBean.getQueryString())) {
            queryPageBean.setQueryString(null);
        }
        PageHelper.startPage(queryPageBean.getCurrentPage(), queryPageBean.getPageSize());
        Page<AiRemindLog> page = aiRemindLogDao.findPage(queryPageBean.getQueryString());
        return new PageResult(page.getTotal(), page.getResult());
    }

    @Override
    public List<AiRemindLog> findPending() {
        return aiRemindLogDao.findPending();
    }
}
