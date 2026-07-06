package com.wygl.service.ai;

import com.wygl.pojo.AiRemindLog;
import com.wygl.dto.QueryPageBean;
import com.wygl.result.PageResult;

/**
 * AI催缴记录服务接口
 */
public interface IAiRemindLogService {

    /**
     * 保存催缴记录（AI生成后、发送前）
     */
    void saveRemindLog(AiRemindLog log);

    /**
     * 发送催缴（更新状态 + 记录操作日志）
     */
    void sendRemind(Integer logId, Integer operatorId);

    /**
     * 分页查询催缴记录
     */
    PageResult findPage(QueryPageBean queryPageBean);

    /**
     * 查询全部待发送的催缴记录
     */
    List<AiRemindLog> findPending();
}
