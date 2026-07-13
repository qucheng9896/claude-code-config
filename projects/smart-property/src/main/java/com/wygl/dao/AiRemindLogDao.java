package com.wygl.dao;

import com.wygl.pojo.AiRemindLog;
import com.github.pagehelper.Page;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface AiRemindLogDao {

    void insert(AiRemindLog log);

    void updateSendStatus(@Param("id") Integer id,
                          @Param("operatorId") Integer operatorId);

    List<AiRemindLog> findPage(@Param("queryString") String queryString);

    List<AiRemindLog> findPending();
}
