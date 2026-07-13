package com.wygl.constant;

public class MessageConstant {

    public static final String LOGIN_SUCCESS = "登录成功";
    public static final String LOGIN_FAIL = "登录失败";
    public static final String USERNAME_NOT_FOUND = "账号不存在";
    public static final String PASSWORD_ERROR = "密码错误";
    public static final String USER_DISABLED = "账号已停用";
    public static final String TOKEN_INVALID = "Token无效或已过期";
    public static final String TOKEN_MISSING = "请先登录";

    public static final String ADD_SUCCESS = "新增成功";
    public static final String EDIT_SUCCESS = "修改成功";
    public static final String DELETE_SUCCESS = "删除成功";

    public static final String USERNAME_EXISTS = "该用户名已存在";
    public static final String PARKING_NO_EXISTS = "该车位编号已存在";
    public static final String PHONE_EXISTS = "该手机号已注册";
    public static final String HOUSE_EXISTS = "该房屋已存在";
    public static final String BILL_EXISTS = "该周期账单已存在";
    public static final String OWNER_HAS_HOUSES = "该业主下还有房屋，无法删除";
    public static final String HOUSE_HAS_UNPAID = "该房屋有未缴账单，无法删除";
    public static final String BILL_CONFIRMED = "已确认到账的账单不可删除";
    public static final String PAY_STATUS_ERROR = "账单状态异常，无法操作";

    public static final String PASSWORD_CHANGE_SUCCESS = "密码修改成功";
    public static final String OLD_PASSWORD_ERROR = "原密码错误";

    public static final String PERMISSION_DENIED = "权限不足";
    public static final String SYSTEM_ERROR = "系统异常，请联系管理员";
    public static final String DB_ERROR = "数据库操作异常，请稍后重试";

    public static final String AI_NO_OVERDUE = "该业主无逾期账单";
    public static final String AI_GENERATE_SUCCESS = "AI催缴消息生成成功";
    public static final String AI_SEND_SUCCESS = "催缴消息已发送";

    public static final String TENANT_NOT_FOUND = "租户不存在";
    public static final String REPAIR_NOT_FOUND = "工单不存在";
}
