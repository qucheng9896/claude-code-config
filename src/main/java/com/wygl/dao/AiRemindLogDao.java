package com.wygl.dao;

import com.wygl.pojo.AiRemindLog;
import com.github.pagehelper.Page;

public interface AiRemindLogDao {

    void insert(AiRemindLog log);

    void updateSendStatus(@Param("id") Integer id, 
                          @Param("operatorId") Integer operatorId);

    Page<AiRemindLog> findPage(@Param("queryString") String queryString);

    List<AiRemindLog> findPending();
}
