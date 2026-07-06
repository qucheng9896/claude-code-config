package com.wygl.dao;

import com.wygl.pojo.Owner;
import org.apache.ibatis.annotations.Param;

public interface OwnerDao extends BaseDao<Owner> {

    Owner findByPhone(@Param("phone") String phone);

    int countByPhone(@Param("phone") String phone);

    int countHousesByOwnerId(@Param("ownerId") Integer ownerId);
}
