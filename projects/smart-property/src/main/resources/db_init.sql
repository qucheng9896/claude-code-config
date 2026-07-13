-- ====================================================================
-- 物业管理系统 — 完整建表 SQL（18 张表 + 3 个视图）
-- 覆盖前端全部 19 个页面的数据需求
-- ====================================================================

DROP DATABASE IF EXISTS property_management;
CREATE DATABASE property_management
    DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE property_management;

-- ==================== 权限模块 ====================

-- ① t_role — 角色表
CREATE TABLE t_role (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(20) NOT NULL UNIQUE COMMENT '角色名称',
    role_desc VARCHAR(100) COMMENT '角色描述',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1启用/0停用',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- ② t_permission — 权限表（自关联树形）
CREATE TABLE t_permission (
    id INT PRIMARY KEY AUTO_INCREMENT,
    parent_id INT NOT NULL DEFAULT 0 COMMENT '父ID(0=一级菜单)',
    perm_name VARCHAR(50) NOT NULL COMMENT '权限名称',
    perm_key VARCHAR(50) NOT NULL UNIQUE COMMENT '权限标识',
    perm_type TINYINT NOT NULL DEFAULT 1 COMMENT '1菜单/2按钮',
    icon VARCHAR(50) COMMENT '图标',
    sort_order INT DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_parent (parent_id),
    INDEX idx_type (perm_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限表';

-- ③ t_role_permission — 角色权限关联
CREATE TABLE t_role_permission (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    perm_id INT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_role_perm (role_id, perm_id),
    CONSTRAINT fk_rp_role FOREIGN KEY (role_id) REFERENCES t_role(id) ON DELETE CASCADE,
    CONSTRAINT fk_rp_perm FOREIGN KEY (perm_id) REFERENCES t_permission(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色权限关联';

-- ==================== 用户模块 ====================

-- ④ t_user — 用户登录表
CREATE TABLE t_user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '登录账号',
    password VARCHAR(64) NOT NULL COMMENT 'MD5密码',
    name VARCHAR(50) NOT NULL COMMENT '真实姓名',
    phone VARCHAR(20) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '邮箱',
    avatar VARCHAR(200) COMMENT '头像URL',
    role_id INT NOT NULL COMMENT '角色ID',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1正常/0停用',
    last_login_time DATETIME COMMENT '最后登录时间',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_role (role_id),
    INDEX idx_username (username),
    CONSTRAINT fk_user_role FOREIGN KEY (role_id) REFERENCES t_role(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ==================== 业主/租户模块 ====================

-- ⑤ t_owner — 业主（产权人）
CREATE TABLE t_owner (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '业主姓名',
    phone VARCHAR(20) NOT NULL UNIQUE COMMENT '联系电话',
    id_card VARCHAR(18) UNIQUE COMMENT '身份证号',
    user_id INT COMMENT '关联用户账号',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1正常/0停用',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_phone (phone),
    CONSTRAINT fk_owner_user FOREIGN KEY (user_id) REFERENCES t_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='业主表';

-- ⑥ t_tenant — 租户表
CREATE TABLE t_tenant (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '租户姓名',
    phone VARCHAR(20) NOT NULL UNIQUE COMMENT '联系电话',
    id_card VARCHAR(18) UNIQUE COMMENT '身份证号',
    user_id INT COMMENT '关联用户账号',
    emergency_contact VARCHAR(50) COMMENT '紧急联系人',
    emergency_phone VARCHAR(20) COMMENT '紧急联系电话',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1正常/0已退租/2黑名单',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    CONSTRAINT fk_tenant_user FOREIGN KEY (user_id) REFERENCES t_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='租户表';

-- ==================== 房产管理模块 ====================

-- ⑦ t_building — 楼栋表
CREATE TABLE t_building (
    id INT PRIMARY KEY AUTO_INCREMENT,
    building_name VARCHAR(50) NOT NULL UNIQUE COMMENT '楼栋名称(如:A座)',
    floors INT NOT NULL DEFAULT 1 COMMENT '层数',
    units INT NOT NULL DEFAULT 1 COMMENT '单元数',
    total_households INT NOT NULL DEFAULT 0 COMMENT '总户数',
    occupancy_rate DECIMAL(5,2) DEFAULT 0.00 COMMENT '入住率(%)',
    build_year YEAR COMMENT '建筑年份',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_build_year (build_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='楼栋表';

-- ⑧ t_house — 房屋表（住宅）
CREATE TABLE t_house (
    id INT PRIMARY KEY AUTO_INCREMENT,
    building_id INT NOT NULL COMMENT '楼栋ID',
    room_no VARCHAR(20) NOT NULL COMMENT '房间号',
    area DECIMAL(10,2) NOT NULL COMMENT '建筑面积(㎡)',
    owner_id INT NOT NULL COMMENT '产权人(业主)',
    tenant_id INT COMMENT '当前租户(为空=空置)',
    house_type VARCHAR(20) COMMENT '户型(如:两室一厅)',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1已入住/0空置',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_building_room (building_id, room_no),
    INDEX idx_owner (owner_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_status (status),
    CONSTRAINT fk_house_building FOREIGN KEY (building_id) REFERENCES t_building(id),
    CONSTRAINT fk_house_owner FOREIGN KEY (owner_id) REFERENCES t_owner(id),
    CONSTRAINT fk_house_tenant FOREIGN KEY (tenant_id) REFERENCES t_tenant(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房屋表';

-- ⑨ t_shop — 商铺表
CREATE TABLE t_shop (
    id INT PRIMARY KEY AUTO_INCREMENT,
    shop_no VARCHAR(30) NOT NULL UNIQUE COMMENT '商铺编号',
    area DECIMAL(10,2) NOT NULL COMMENT '面积(㎡)',
    owner_id INT COMMENT '产权人(为空=物业自持)',
    tenant_id INT COMMENT '当前租户',
    monthly_rent DECIMAL(10,2) COMMENT '月租金',
    business_scope VARCHAR(100) COMMENT '经营范围',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1在租/0空置/3自用',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_owner (owner_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_status (status),
    CONSTRAINT fk_shop_owner FOREIGN KEY (owner_id) REFERENCES t_owner(id) ON DELETE SET NULL,
    CONSTRAINT fk_shop_tenant FOREIGN KEY (tenant_id) REFERENCES t_tenant(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商铺表';

-- ⑩ t_parking — 车位表
CREATE TABLE t_parking (
    id INT PRIMARY KEY AUTO_INCREMENT,
    parking_no VARCHAR(30) NOT NULL UNIQUE COMMENT '车位编号',
    area VARCHAR(50) COMMENT '所属区域(如:B1-A区)',
    type VARCHAR(20) NOT NULL DEFAULT '地下车位' COMMENT '类型(地下/地面/充电桩)',
    size DECIMAL(6,2) COMMENT '面积(㎡)',
    owner_id INT COMMENT '产权人(为空=物业自持)',
    tenant_id INT COMMENT '当前租户',
    monthly_rent DECIMAL(10,2) COMMENT '月租金',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1租赁/2产权/0空闲',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_owner (owner_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_status (status),
    INDEX idx_area (area),
    CONSTRAINT fk_parking_owner FOREIGN KEY (owner_id) REFERENCES t_owner(id) ON DELETE SET NULL,
    CONSTRAINT fk_parking_tenant FOREIGN KEY (tenant_id) REFERENCES t_tenant(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车位表';

-- ⑪ t_facility — 公共设施表
CREATE TABLE t_facility (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '设施名称',
    type VARCHAR(30) NOT NULL COMMENT '类型(电梯/配电房/水泵房/消防/绿化/道路)',
    location VARCHAR(100) COMMENT '位置',
    quantity VARCHAR(50) COMMENT '数量/面积',
    maintainer VARCHAR(50) COMMENT '维护负责人',
    last_check DATE COMMENT '上次检修日期',
    next_check DATE COMMENT '下次检修日期',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1正常/2需维修/3检修中',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_next_check (next_check)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公共设施表';

-- ==================== 租赁管理模块 ====================

-- ⑫ t_rental — 租赁合同表
CREATE TABLE t_rental (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rental_no VARCHAR(32) NOT NULL UNIQUE COMMENT '合同编号',
    owner_id INT NOT NULL COMMENT '出租方(业主)',
    tenant_id INT NOT NULL COMMENT '承租方(租户)',
    house_id INT NOT NULL COMMENT '房屋ID',
    start_date DATE NOT NULL COMMENT '起租日',
    end_date DATE NOT NULL COMMENT '到期日',
    monthly_rent DECIMAL(10,2) NOT NULL COMMENT '月租金',
    deposit DECIMAL(10,2) COMMENT '押金',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1有效/0已到期/2提前终止',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_owner (owner_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_house (house_id),
    INDEX idx_status (status),
    INDEX idx_end_date (end_date),
    CONSTRAINT fk_rental_owner FOREIGN KEY (owner_id) REFERENCES t_owner(id),
    CONSTRAINT fk_rental_tenant FOREIGN KEY (tenant_id) REFERENCES t_tenant(id),
    CONSTRAINT fk_rental_house FOREIGN KEY (house_id) REFERENCES t_house(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='租赁合同表';

-- ==================== 收费管理模块 ====================

-- ⑬ t_payment — 缴费记录表
CREATE TABLE t_payment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bill_no VARCHAR(32) NOT NULL UNIQUE COMMENT '账单编号',
    house_id INT NOT NULL COMMENT '房屋ID',
    tenant_id INT NOT NULL COMMENT '缴费人(租户)',
    owner_id INT NOT NULL COMMENT '收款方(业主)',
    fee_type VARCHAR(20) NOT NULL COMMENT '费用类型(物业费/水电费/停车费/租金/公摊/滞纳金)',
    amount DECIMAL(10,2) NOT NULL COMMENT '应缴金额',
    period VARCHAR(20) NOT NULL COMMENT '费用周期(如2025-01)',
    due_date DATE COMMENT '截止日期',
    pay_status TINYINT NOT NULL DEFAULT 0 COMMENT '0未缴/1已缴/2已确认/3逾期',
    pay_time DATETIME COMMENT '缴费时间',
    pay_method VARCHAR(20) COMMENT '支付方式(微信/支付宝/银行转账/现金)',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_tenant_status (tenant_id, pay_status),
    INDEX idx_house_period (house_id, period),
    INDEX idx_period (period),
    INDEX idx_status (pay_status),
    INDEX idx_due_date (due_date),
    CONSTRAINT fk_pay_house FOREIGN KEY (house_id) REFERENCES t_house(id),
    CONSTRAINT fk_pay_tenant FOREIGN KEY (tenant_id) REFERENCES t_tenant(id),
    CONSTRAINT fk_pay_owner FOREIGN KEY (owner_id) REFERENCES t_owner(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='缴费记录表';

-- ==================== AI 催缴模块 ====================

-- ⑭ t_ai_remind_log — AI 催缴记录
CREATE TABLE t_ai_remind_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tenant_id INT NOT NULL COMMENT '被催缴人(租户)',
    house_id INT NOT NULL COMMENT '房屋',
    payment_ids VARCHAR(500) COMMENT '关联账单IDs(逗号分隔)',
    overdue_amount DECIMAL(10,2) NOT NULL COMMENT '逾期金额',
    overdue_days INT NOT NULL COMMENT '逾期天数',
    ai_prompt TEXT COMMENT '发送给AI的prompt',
    ai_message TEXT COMMENT 'AI生成的催缴消息',
    send_channel VARCHAR(20) DEFAULT '短信' COMMENT '发送渠道(短信/微信/电话)',
    send_status TINYINT NOT NULL DEFAULT 0 COMMENT '0待发送/1已发送/2发送失败',
    send_time DATETIME COMMENT '发送时间',
    operator_id INT COMMENT '操作管理员ID',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tenant (tenant_id),
    INDEX idx_status (send_status),
    CONSTRAINT fk_ai_tenant FOREIGN KEY (tenant_id) REFERENCES t_tenant(id),
    CONSTRAINT fk_ai_house FOREIGN KEY (house_id) REFERENCES t_house(id),
    CONSTRAINT fk_ai_operator FOREIGN KEY (operator_id) REFERENCES t_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI催缴记录表';

-- ==================== 安防门禁模块 ====================

-- ⑮ t_visitor — 访客表
CREATE TABLE t_visitor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '访客姓名',
    phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    owner_id INT NOT NULL COMMENT '被访业主',
    house_id INT NOT NULL COMMENT '被访房屋',
    reserve_time DATETIME COMMENT '预约时间',
    access_method VARCHAR(20) DEFAULT '临时密码' COMMENT '通行方式(临时密码/人脸授权/刷卡)',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '0待核验/1已核验/2已过期/3已取消',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_owner (owner_id),
    INDEX idx_house (house_id),
    INDEX idx_status (status),
    INDEX idx_reserve_time (reserve_time),
    CONSTRAINT fk_visitor_owner FOREIGN KEY (owner_id) REFERENCES t_owner(id),
    CONSTRAINT fk_visitor_house FOREIGN KEY (house_id) REFERENCES t_house(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='访客表';

-- ⑯ t_access_record — 门禁通行记录表
CREATE TABLE t_access_record (
    id INT PRIMARY KEY AUTO_INCREMENT,
    access_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '通行时间',
    person_name VARCHAR(50) NOT NULL COMMENT '姓名',
    identity_type TINYINT NOT NULL COMMENT '身份(1业主/2租户/3访客/4外来)',
    person_id INT COMMENT '对应人员ID',
    house_id INT COMMENT '所属房屋',
    access_method VARCHAR(20) COMMENT '通行方式(人脸/手机/刷卡/临时密码)',
    device_name VARCHAR(50) COMMENT '门口机名称',
    result TINYINT NOT NULL DEFAULT 1 COMMENT '1通过/0拒绝',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_access_time (access_time),
    INDEX idx_person (identity_type, person_id),
    INDEX idx_house (house_id),
    INDEX idx_result (result)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='门禁通行记录表';

-- ==================== 报修服务模块 ====================

-- ⑰ t_repair_order — 报修工单表
CREATE TABLE t_repair_order (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(32) NOT NULL UNIQUE COMMENT '工单编号',
    reporter VARCHAR(50) NOT NULL COMMENT '报修人',
    house_id INT NOT NULL COMMENT '报修房屋',
    issue_type VARCHAR(30) NOT NULL COMMENT '问题类型(水电/电梯/门禁/公共设施)',
    urgency TINYINT NOT NULL DEFAULT 1 COMMENT '紧急程度(1一般/2紧急/3特急)',
    description VARCHAR(500) COMMENT '问题描述',
    worker_id INT COMMENT '派单维修工',
    worker_name VARCHAR(50) COMMENT '维修工姓名',
    dispatch_time DATETIME COMMENT '派单时间',
    finish_time DATETIME COMMENT '完成时间',
    evaluation TINYINT COMMENT '评价(1-5星)',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '0待派单/1维修中/2已完成/3已评价',
    remark VARCHAR(200) COMMENT '备注',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_house (house_id),
    INDEX idx_worker (worker_id),
    INDEX idx_status (status),
    INDEX idx_urgency (urgency),
    INDEX idx_create_time (create_time),
    CONSTRAINT fk_repair_house FOREIGN KEY (house_id) REFERENCES t_house(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报修工单表';

-- ==================== 社区服务模块 ====================

-- ⑱ t_notice — 公告通知表
CREATE TABLE t_notice (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT COMMENT '内容',
    type VARCHAR(20) NOT NULL COMMENT '类型(通知/公告/福利/投票/投诉)',
    scope VARCHAR(50) DEFAULT '全体业主' COMMENT '发布范围',
    read_count INT DEFAULT 0 COMMENT '已读人数',
    total_count INT DEFAULT 0 COMMENT '总人数',
    publish_date DATE COMMENT '发布日期',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1发布中/0已撤回',
    operator_id INT COMMENT '发布人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_publish_date (publish_date),
    CONSTRAINT fk_notice_operator FOREIGN KEY (operator_id) REFERENCES t_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公告通知表';

-- ==================== 员工管理模块 ====================

-- ⑲ t_employee — 物业员工表
CREATE TABLE t_employee (
    id INT PRIMARY KEY AUTO_INCREMENT,
    emp_no VARCHAR(20) NOT NULL UNIQUE COMMENT '工号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    phone VARCHAR(20) NOT NULL COMMENT '手机号',
    position VARCHAR(30) COMMENT '岗位',
    department VARCHAR(30) COMMENT '部门(管理层/工程部/安保部/客服部)',
    hire_date DATE COMMENT '入职日期',
    attendance_days INT DEFAULT 0 COMMENT '本月出勤天数',
    order_count INT DEFAULT 0 COMMENT '本月工单数',
    rating DECIMAL(3,1) DEFAULT 5.0 COMMENT '评分(0-5)',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1在职/2休假/0离职',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_department (department),
    INDEX idx_status (status),
    INDEX idx_position (position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='物业员工表';

-- ==================== 操作审计日志 ====================

-- ⑳ t_operation_log — 操作审计日志
CREATE TABLE t_operation_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INT COMMENT '操作用户',
    module VARCHAR(50) COMMENT '功能模块',
    operation VARCHAR(100) NOT NULL COMMENT '操作描述',
    method VARCHAR(200) COMMENT '请求方法',
    params TEXT COMMENT '请求参数',
    ip VARCHAR(40) COMMENT 'IP地址',
    duration INT COMMENT '执行时长(ms)',
    status TINYINT DEFAULT 1 COMMENT '1成功/0失败',
    error_msg TEXT COMMENT '错误信息',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_module (module),
    INDEX idx_time (create_time),
    CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES t_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';

-- ==================== 视图 ====================

-- 视图1：租户缴费统计
CREATE VIEW v_tenant_payment_summary AS
SELECT
    t.id AS tenant_id,
    t.name AS tenant_name,
    t.phone,
    b.building_name,
    h.room_no,
    COUNT(CASE WHEN p.pay_status = 0 OR p.pay_status = 3 THEN 1 END) AS unpaid_count,
    SUM(CASE WHEN p.pay_status = 0 OR p.pay_status = 3 THEN p.amount ELSE 0 END) AS unpaid_amount,
    SUM(CASE WHEN p.pay_status = 2 THEN p.amount ELSE 0 END) AS confirmed_amount,
    MAX(CASE WHEN p.pay_status = 3 THEN p.due_date END) AS earliest_overdue
FROM t_tenant t
LEFT JOIN t_house h ON h.tenant_id = t.id
LEFT JOIN t_building b ON h.building_id = b.id
LEFT JOIN t_payment p ON p.tenant_id = t.id
WHERE t.status = 1
GROUP BY t.id, t.name, t.phone, b.building_name, h.room_no;

-- 视图2：月度收缴汇总
CREATE VIEW v_monthly_summary AS
SELECT
    p.period,
    p.fee_type,
    COUNT(*) AS total_bills,
    SUM(CASE WHEN p.pay_status IN(1,2) THEN 1 ELSE 0 END) AS paid_bills,
    SUM(CASE WHEN p.pay_status IN(0,3) THEN 1 ELSE 0 END) AS unpaid_bills,
    SUM(p.amount) AS total_amount,
    SUM(CASE WHEN p.pay_status IN(1,2) THEN p.amount ELSE 0 END) AS paid_amount,
    ROUND(SUM(CASE WHEN p.pay_status IN(1,2) THEN p.amount ELSE 0 END) /
          NULLIF(SUM(p.amount), 0) * 100, 1) AS pay_rate
FROM t_payment p
GROUP BY p.period, p.fee_type
ORDER BY p.period DESC, p.fee_type;

-- 视图3：租赁状态一览
CREATE VIEW v_rental_status AS
SELECT
    r.rental_no,
    o.name AS owner_name,
    t.name AS tenant_name,
    t.phone AS tenant_phone,
    CONCAT(b.building_name, '-', h.room_no) AS house_address,
    h.area,
    r.monthly_rent,
    r.start_date,
    r.end_date,
    r.status,
    CASE
        WHEN r.end_date < CURDATE() THEN '已到期'
        WHEN r.end_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN '即将到期'
        ELSE '正常履行'
    END AS rental_state,
    DATEDIFF(r.end_date, CURDATE()) AS remaining_days
FROM t_rental r
JOIN t_owner o ON r.owner_id = o.id
JOIN t_tenant t ON r.tenant_id = t.id
JOIN t_house h ON r.house_id = h.id
JOIN t_building b ON h.building_id = b.id
ORDER BY r.end_date ASC;

-- ==================== 初始化数据 ====================

INSERT INTO t_role (id, role_name, role_desc) VALUES
(1, '系统管理员', '全部权限'),
(2, '业主', '查看名下房屋/租户/账单'),
(3, '租户', '查看本人房屋/账单/在线缴费');

INSERT INTO t_permission (parent_id, perm_name, perm_key, perm_type, sort_order) VALUES
(0, '概览', 'dashboard:menu', 1, 1),
(1, '数据概览', 'dashboard:view', 1, 1),
(0, '房产管理', 'property:menu', 1, 2),
(3, '楼栋管理', 'building:list', 1, 1),
(3, '住宅管理', 'house:list', 1, 2),
(3, '商铺管理', 'shop:list', 1, 3),
(3, '车位管理', 'parking:list', 1, 4),
(3, '公共设施', 'facility:list', 1, 5),
(0, '人员管理', 'people:menu', 1, 3),
(9, '业主管理', 'owner:list', 1, 1),
(9, '租户管理', 'tenant:list', 1, 2),
(9, '物业员工', 'employee:list', 1, 3),
(9, '访客管理', 'visitor:list', 1, 4),
(0, '租赁管理', 'rental:menu', 1, 4),
(14, '住宅合同', 'rental:house', 1, 1),
(14, '商铺合同', 'rental:shop', 1, 2),
(14, '车位租赁', 'rental:parking', 1, 3),
(14, '到期预警', 'rental:expire', 1, 4),
(0, '收费管理', 'payment:menu', 1, 5),
(19, '住宅物业费', 'payment:property', 1, 1),
(19, '商铺物业费', 'payment:shop_fee', 1, 2),
(19, '公摊水电', 'payment:shared', 1, 3),
(19, '停车费', 'payment:parking_fee', 1, 4),
(19, '滞纳金', 'payment:latefee', 1, 5),
(19, 'AI智能催缴', 'payment:ai_remind', 2, 6),
(0, '安防门禁', 'security:menu', 1, 6),
(26, '门禁记录', 'access:records', 1, 1),
(26, '人脸管理', 'access:face', 1, 2),
(26, '访客预约', 'visitor:reserve', 1, 3),
(0, '报修服务', 'repair:menu', 1, 7),
(30, '工单列表', 'repair:list', 1, 1),
(30, '待派单', 'repair:pending', 1, 2),
(30, '维修中', 'repair:processing', 1, 3),
(30, '已完成', 'repair:done', 1, 4),
(0, '社区服务', 'community:menu', 1, 8),
(35, '公告发布', 'notice:list', 1, 1),
(35, '节假日福利', 'notice:holiday', 1, 2),
(35, '投诉建议', 'notice:complaint', 1, 3),
(35, '在线投票', 'notice:vote', 1, 4),
(0, '经营报表', 'report:menu', 1, 9),
(40, '收缴明细表', 'report:payment', 1, 1),
(40, '租赁报表', 'report:rental', 1, 2),
(40, '工单报表', 'report:repair', 1, 3),
(40, '年度汇总', 'report:year', 1, 4),
(0, '系统管理', 'system:menu', 1, 10),
(45, '用户管理', 'user:list', 1, 1),
(45, '角色管理', 'role:list', 1, 2),
(45, '权限管理', 'perm:list', 1, 3),
(45, '操作日志', 'log:list', 1, 4),
(45, '数据备份', 'backup', 1, 5),
(3, '新增楼栋', 'building:add', 2, 1),
(3, '新增住宅', 'house:add', 2, 1),
(3, '新增商铺', 'shop:add', 2, 1),
(3, '新增车位', 'parking:add', 2, 1),
(3, '新增设施', 'facility:add', 2, 1),
(9, '新增业主', 'owner:add', 2, 1),
(9, '新增租户', 'tenant:add', 2, 1),
(9, '新增员工', 'employee:add', 2, 1),
(19, '生成账单', 'payment:generate', 2, 1),
(19, '确认到账', 'payment:confirm', 2, 3),
(30, '派单', 'repair:dispatch', 2, 1),
(35, '发布公告', 'notice:add', 2, 1),
(45, '新增用户', 'user:add', 2, 1),
(45, '编辑用户', 'user:edit', 2, 2),
(45, '删除用户', 'user:delete', 2, 3);

INSERT INTO t_role_permission (role_id, perm_id)
SELECT 1, id FROM t_permission;

INSERT INTO t_role_permission (role_id, perm_id) VALUES
(2,1),(2,4),(2,9),(2,14),(2,19),
(3,1),(3,19);

-- 初始化管理员（密码: 123456 MD5: e10adc3949ba59abbe56e057f20f883e）
INSERT INTO t_user (username, password, name, phone, role_id) VALUES
('admin', 'e10adc3949ba59abbe56e057f20f883e', '系统管理员', '13900000000', 1);

-- 初始化楼栋
INSERT INTO t_building (id, building_name, floors, units, total_households, occupancy_rate, build_year) VALUES
(1, 'A座', 24, 2, 96, 98.00, 2020),
(2, 'B座', 24, 2, 96, 96.00, 2020),
(3, 'C座', 18, 3, 108, 88.00, 2021),
(4, 'D座', 12, 2, 48, 92.00, 2022),
(5, 'E座', 28, 2, 112, 45.00, 2024);

-- 初始化业主（100个，每人名下约2-4套房）
INSERT INTO t_owner (id, name, phone, id_card, status) VALUES
(1, '王大明', '13800000001', '330102198501011234', 1),
(2, '李小红', '13800000002', '330102199002022345', 1),
(3, '张伟', '13800000003', '330102198703033456', 1),
(4, '刘芳', '13800000004', '330102199104044567', 1),
(5, '陈强', '13800000005', '330102198805055678', 1),
(6, '赵敏', '13800000006', '330102199206066789', 1),
(7, '孙磊', '13800000007', '330102198607077890', 1),
(8, '周婷', '13800000008', '330102199308088901', 1),
(9, '吴刚', '13800000009', '330102198909099012', 1),
(10, '郑丽', '13800000010', '330102199410101234', 1),
(11, '王军', '13800000011', '330102198511112345', 1),
(12, '李娜', '13800000012', '330102199012123456', 1),
(13, '张敏', '13800000013', '330102198713134567', 1),
(14, '刘洋', '13800000014', '330102199114145678', 1),
(15, '陈静', '13800000015', '330102198815156789', 1),
(16, '杨帆', '13800000016', '330102199216167890', 1),
(17, '黄磊', '13800000017', '330102198617178901', 1),
(18, '林峰', '13800000018', '330102199318189012', 1),
(19, '何静', '13800000019', '330102198919191234', 1),
(20, '罗成', '13800000020', '330102199420202345', 1),
(21, '马超', '13800000021', '330102199501012456', 1),
(22, '宋佳', '13800000022', '330102199602023567', 1),
(23, '韩磊', '13800000023', '330102198703034678', 1),
(24, '冯颖', '13800000024', '330102198804045789', 1),
(25, '朱军', '13800000025', '330102198905056890', 1),
(26, '秦岚', '13800000026', '330102199006067901', 1),
(27, '许巍', '13800000027', '330102199107078012', 1),
(28, '何平', '13800000028', '330102199208089123', 1),
(29, '吕超', '13800000029', '330102199309090234', 1),
(30, '施洁', '13800000030', '330102199410101345', 1),
(31, '孔明', '13800000031', '330102198511112456', 1),
(32, '曹颖', '13800000032', '330102198612123567', 1),
(33, '严华', '13800000033', '330102198713134678', 1),
(34, '华敏', '13800000034', '330102198814145789', 1),
(35, '金鑫', '13800000035', '330102198915156890', 1),
(36, '魏巍', '13800000036', '330102199016167901', 1),
(37, '陶然', '13800000037', '330102199117178012', 1),
(38, '姜涛', '13800000038', '330102199218189123', 1),
(39, '戚薇', '13800000039', '330102199319190234', 1),
(40, '谢峰', '13800000040', '330102199420201345', 1),
(41, '邹丽', '13800000041', '330102198501212456', 1),
(42, '潘安', '13800000042', '330102198602223567', 1),
(43, '范伟', '13800000043', '330102198703234678', 1),
(44, '彭磊', '13800000044', '330102198804245789', 1),
(45, '鲁静', '13800000045', '330102198905256890', 1),
(46, '韦强', '13800000046', '330102199006267901', 1),
(47, '昌明', '13800000047', '330102199107278012', 1),
(48, '苗蕾', '13800000048', '330102199208289123', 1),
(49, '凤英', '13800000049', '330102199309290234', 1),
(50, '花蕊', '13800000050', '330102199410201345', 1),
(51, '任杰', '13800000051', '330102198511212456', 1),
(52, '袁媛', '13800000052', '330102198612223567', 1),
(53, '柳青', '13800000053', '330102198713234678', 1),
(54, '邓超', '13800000054', '330102198814245789', 1),
(55, '鲍明', '13800000055', '330102198915256890', 1),
(56, '史进', '13800000056', '330102199016267901', 1),
(57, '唐蕾', '13800000057', '330102199117278012', 1),
(58, '费翔', '13800000058', '330102199218289123', 1),
(59, '廉芳', '13800000059', '330102199319290234', 1),
(60, '岑溪', '13800000060', '330102199420301345', 1),
(61, '薛涛', '13800000061', '330102198501312456', 1),
(62, '贺强', '13800000062', '330102198602323567', 1),
(63, '倪萍', '13800000063', '330102198703334678', 1),
(64, '汤敏', '13800000064', '330102198804345789', 1),
(65, '滕飞', '13800000065', '330102198905356890', 1),
(66, '殷悦', '13800000066', '330102199006367901', 1),
(67, '罗兰', '13800000067', '330102199107378012', 1),
(68, '毕成', '13800000068', '330102199208389123', 1),
(69, '郝蕾', '13800000069', '330102199309390234', 1),
(70, '邬娜', '13800000070', '330102199410301345', 1),
(71, '安琪', '13800000071', '330102198511312456', 1),
(72, '常亮', '13800000072', '330102198612323567', 1),
(73, '乐天', '13800000073', '330102198713334678', 1),
(74, '于洋', '13800000074', '330102198814345789', 1),
(75, '时雨', '13800000075', '330102198915356890', 1),
(76, '傅强', '13800000076', '330102199016367901', 1),
(77, '皮特', '13800000077', '330102199117378012', 1),
(78, '卞洁', '13800000078', '330102199218389123', 1),
(79, '齐峰', '13800000079', '330102199319390234', 1),
(80, '康宁', '13800000080', '330102199420401345', 1),
(81, '伍明', '13800000081', '330102198501412456', 1),
(82, '余芬', '13800000082', '330102198602423567', 1),
(83, '元昊', '13800000083', '330102198703434678', 1),
(84, '卜凡', '13800000084', '330102198804445789', 1),
(85, '顾城', '13800000085', '330102198905456890', 1),
(86, '孟晓', '13800000086', '330102199006467901', 1),
(87, '平伟', '13800000087', '330102199107478012', 1),
(88, '黄蓉', '13800000088', '330102199208489123', 1),
(89, '穆青', '13800000089', '330102199309490234', 1),
(90, '萧峰', '13800000090', '330102199410401345', 1),
(91, '尹航', '13800000091', '330102198511412456', 1),
(92, '江波', '13800000092', '330102198612423567', 1),
(93, '童蕾', '13800000093', '330102198713434678', 1),
(94, '颜骏', '13800000094', '330102198814445789', 1),
(95, '郭靖', '13800000095', '330102198915456890', 1),
(96, '林夕', '13800000096', '330102199016467901', 1),
(97, '钟意', '13800000097', '330102199117478012', 1),
(98, '徐晨', '13800000098', '330102199218489123', 1),
(99, '邱雨', '13800000099', '330102199319490234', 1),
(100, '骆冰', '13800000100', '330102199420501345', 1);

-- 初始化租户（15个）
INSERT INTO t_tenant (id, name, phone, id_card, status) VALUES
(1, '陈租客', '13900000011', '330103199503033456', 1),
(2, '刘租客', '13900000012', '330103199804044567', 1),
(3, '黄租客', '13900000013', '330103199605055678', 1),
(4, '林租客', '13900000014', '330103199706066789', 1),
(5, '吴租客', '13900000015', '330103199907077890', 1),
(6, '郑租客', '13900000016', '330103199508088901', 1),
(7, '王租客', '13900000017', '330103199809099012', 1),
(8, '冯租客', '13900000018', '330103199610101234', 1),
(9, '卫租客', '13900000019', '330103199711112345', 1),
(10, '蒋租客', '13900000020', '330103199912123456', 1),
(11, '沈租客', '13900000021', '330103199513134567', 1),
(12, '韩租客', '13900000022', '330103199814145678', 1),
(13, '杨租客', '13900000023', '330103199615156789', 1),
(14, '朱租客', '13900000024', '330103199716167890', 1),
(15, '秦租客', '13900000025', '330103199917178901', 1);

-- ========================================
-- 批量生成房屋数据（460户）
-- A座:96  B座:96  C座:108  D座:48  E座:112
-- 先用 owner_id=1 占位，插入后再按 id 均分业主
-- ========================================
INSERT INTO t_house (building_id, room_no, area, owner_id, tenant_id, house_type, status)
SELECT
    b.id AS building_id,
    CONCAT(h.floor, LPAD((u.n - 1) * 2 + r.n, 2, '0')) AS room_no,
    ROUND(70 + (h.row_num * 7 % 80) + 0.37, 2) AS area,
    1 AS owner_id,
    CASE WHEN (h.row_num * 17 % 100) < 85
         THEN 1 + ((h.row_num * 19) % 15)
         ELSE NULL END AS tenant_id,
    ELT(1 + ((h.row_num * 23) % 5), '两室一厅', '三室一厅', '三室两厅', '两室两厅', '一室一厅') AS house_type,
    CASE WHEN (h.row_num * 17 % 100) < 85 THEN 1 ELSE 0 END AS status
FROM (
    SELECT b.id AS building_id, b.floors, b.units,
           tens.n * 10 + ones.n AS floor,
           ROW_NUMBER() OVER (PARTITION BY b.id ORDER BY tens.n * 10 + ones.n) AS row_num
    FROM t_building b
    JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
          UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) tens
        ON tens.n BETWEEN 0 AND CEIL(b.floors / 10)
    JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
          UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) ones
        ON ones.n BETWEEN 0 AND 9
       AND tens.n * 10 + ones.n BETWEEN 1 AND b.floors
) h
JOIN t_building b ON b.id = h.building_id
JOIN (SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
      UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) u
    ON u.n BETWEEN 1 AND b.units
JOIN (SELECT 1 AS n UNION SELECT 2) r
    ON r.n BETWEEN 1 AND 2;

-- 按 id 均分业主（每人4-5套房，100位业主）
UPDATE t_house SET owner_id = 1 + ((id - 1) % 100);

-- ========================================
-- 批量生成租赁合同（为已入住房屋生成）
-- ========================================
INSERT INTO t_rental (rental_no, owner_id, tenant_id, house_id, start_date, end_date, monthly_rent, deposit, status)
SELECT
    CONCAT('HT2025', LPAD(h.id, 6, '0')) AS rental_no,
    h.owner_id, h.tenant_id, h.id AS house_id,
    DATE_SUB(CURDATE(), INTERVAL ((h.id * 7) % 6) MONTH) AS start_date,
    DATE_ADD(CURDATE(), INTERVAL (6 + (h.id * 11) % 18) MONTH) AS end_date,
    ROUND(1500 + (h.id * 13 % 3000) + 0.5, 2) AS monthly_rent,
    ROUND((1500 + (h.id * 13 % 3000)) * 2, 2) AS deposit,
    1 AS status
FROM t_house h WHERE h.status = 1;

-- ========================================
-- 批量生成缴费账单（每户6个月，每月1笔）
-- ========================================
INSERT INTO t_payment (bill_no, house_id, tenant_id, owner_id, fee_type, amount, period, due_date, pay_status)
SELECT
    CONCAT('BILL2025', LPAD((h.id - 1) * 6 + m.m, 6, '0')) AS bill_no,
    h.id AS house_id,
    COALESCE(h.tenant_id, h.owner_id) AS tenant_id,
    h.owner_id,
    ELT(1 + (((h.id * 17 + m.m * 31) % 3)), '物业费', '水电费', '停车费') AS fee_type,
    ROUND(100 + (h.id * 13 + m.m * 29) % 400 + 0.5, 2) AS amount,
    DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL (m.m - 1) MONTH), '%Y-%m') AS period,
    LAST_DAY(DATE_SUB(CURDATE(), INTERVAL (m.m - 1) MONTH)) AS due_date,
    (h.id * 7 + m.m * 11) % 4 AS pay_status
FROM t_house h
CROSS JOIN (SELECT 1 AS m UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) m
WHERE h.tenant_id IS NOT NULL;

-- ========================================
-- 批量生成商铺（36间）
-- ========================================
INSERT INTO t_shop (id, shop_no, area, owner_id, tenant_id, monthly_rent, business_scope, status)
SELECT
    n.n AS id,
    CONCAT('S', 1 + FLOOR(n.n / 18), 'F-', LPAD(n.n, 3, '0')) AS shop_no,
    ROUND(40 + (n.n * 17 % 160) + 0.42, 2) AS area,
    CASE WHEN (n.n * 23 % 100) < 30 THEN 1 + (n.n % 100) ELSE NULL END AS owner_id,
    CASE WHEN (n.n * 19 % 100) < 70 THEN 1 + (n.n * 11 % 15) ELSE NULL END AS tenant_id,
    ROUND(2000 + (n.n * 7 % 6000) + 0.5, 2) AS monthly_rent,
    ELT(1 + (n.n * 3 % 10), '便利店', '餐饮', '药店', '美容美发', '教育培训', '房产中介', '水果店', '干洗店', '快递驿站', '社区超市') AS business_scope,
    CASE WHEN (n.n * 29 % 100) < 85 THEN 1 ELSE 0 END AS status
FROM (SELECT @row := @row + 1 AS n FROM
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) b,
    (SELECT @row := 0) init
) n
WHERE n.n BETWEEN 1 AND 36;

-- ========================================
-- 批量生成车位（580个）
-- B1: A-D各3层×30个 = 360个  编号 B1-A01-1F ~ B1-D30-3F
-- B2: A-D各2层×30个 = 220个  编号 B2-A01-1F ~ B2-D30-2F
-- ========================================
INSERT INTO t_parking (id, parking_no, area, type, size, owner_id, tenant_id, monthly_rent, status)
SELECT
    n.n AS id,
    CASE
        WHEN n.n <= 360 THEN
            CONCAT('B1-',
                ELT(1 + FLOOR((n.n - 1) / 90), 'A', 'B', 'C', 'D'),
                LPAD(1 + ((n.n - 1) % 30), 2, '0'), '-',
                1 + FLOOR(((n.n - 1) % 90) / 30), 'F')
        ELSE
            CONCAT('B2-',
                ELT(1 + FLOOR((n.n - 361) / 60), 'A', 'B', 'C', 'D'),
                LPAD(1 + ((n.n - 361) % 30), 2, '0'), '-',
                1 + FLOOR(((n.n - 361) % 60) / 30), 'F')
    END AS parking_no,
    CASE
        WHEN n.n <= 360 THEN CONCAT('B1-', ELT(1 + FLOOR((n.n - 1) / 90), 'A', 'B', 'C', 'D'), '区')
        ELSE CONCAT('B2-', ELT(1 + FLOOR((n.n - 361) / 60), 'A', 'B', 'C', 'D'), '区')
    END AS area,
    ELT(1 + (n.n * 3 % 10),
        CASE WHEN n.n <= 50 THEN '充电桩车位' ELSE '地下车位' END,
        '地下车位', '地下车位', '地下车位', '地下车位',
        '地面车位', '地面车位', '地面车位',
        '充电桩车位', '充电桩车位') AS type,
    ROUND(12 + (n.n * 7 % 3) + 0.5, 2) AS size,
    CASE WHEN (n.n * 11 % 100) < 20 THEN 1 + (n.n % 100) ELSE NULL END AS owner_id,
    CASE WHEN (n.n * 17 % 100) < 60 THEN 1 + (n.n * 19 % 15) ELSE NULL END AS tenant_id,
    CASE WHEN (n.n * 23 % 100) < 70 THEN ROUND(200 + (n.n * 29 % 200), 0) ELSE NULL END AS monthly_rent,
    CASE WHEN (n.n * 7 % 100) < 60 THEN 1 WHEN (n.n * 11 % 100) < 80 THEN 0 ELSE 2 END AS status
FROM (SELECT @row := @row + 1 AS n FROM
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b,
    (SELECT 0 UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) c,
    (SELECT @row := 0) init
) n
WHERE n.n BETWEEN 1 AND 580;

-- 初始化公共设施
INSERT INTO t_facility (id, name, type, location, quantity, maintainer, last_check, next_check, status) VALUES
(1, '1栋电梯A', '电梯', '1栋1单元', '2台(1000kg)', '张师傅', '2025-01-01', '2025-02-01', 1),
(2, '1栋电梯B', '电梯', '1栋2单元', '2台(1000kg)', '张师傅', '2025-01-01', '2025-02-01', 2),
(3, '1号配电房', '配电房', 'B1层东侧', '1间(80㎡)', '李电工', '2024-12-15', '2025-03-15', 1),
(4, '消防泵房', '水泵房', 'B2层西侧', '1间(60㎡)', '王师傅', '2024-12-20', '2025-03-20', 3),
(5, '中央绿化带', '绿化', '小区中央', '8200㎡', '绿化工-赵', '2025-01-05', '2025-01-12', 1),
(6, '北门道闸', '道路', '北大门', '2套', '物业-安保', '2025-01-02', '2025-04-02', 1);

-- 初始化员工
INSERT INTO t_employee (id, emp_no, name, phone, position, department, hire_date, attendance_days, order_count, rating, status) VALUES
(1, 'E001', '张师傅', '1380000001', '维修技工', '工程部', '2020-03-15', 26, 48, 4.9, 1),
(2, 'E002', '李电工', '1380000002', '维修技工', '工程部', '2020-05-20', 25, 41, 4.8, 1),
(3, 'E003', '王主管', '1380000003', '安保主管', '安保部', '2019-08-01', 26, 0, 4.7, 1),
(4, 'E007', '刘保洁', '1380000007', '保洁员', '客服部', '2021-02-10', 24, 0, 4.5, 2),
(5, 'E012', '赵队长', '1380000012', '安保队长', '安保部', '2018-06-01', 26, 0, 4.9, 1);

-- 初始化报修工单
INSERT INTO t_repair_order (id, order_no, reporter, house_id, issue_type, urgency, description, worker_id, worker_name, dispatch_time, status) VALUES
(1, 'WX2501008', '陈租客', 1, '水管漏水', 2, '厨房水管破裂漏水', 1, '张师傅', '2025-01-08 10:00', 1),
(2, 'WX2501009', '刘租客', 3, '电梯故障', 3, '电梯突然停止运行', 2, '李师傅', '2025-01-08 11:00', 0),
(3, 'WX2501010', '王大明', 2, '门禁失灵', 1, '门禁刷卡无响应', 1, '张师傅', '2025-01-08 14:30', 2);

-- 初始化公告
INSERT INTO t_notice (id, title, content, type, scope, read_count, total_count, publish_date, status) VALUES
(1, '关于2025年春节放假及安全检查的通知', '请各位业主注意...', '通知', '全体业主', 420, 520, '2025-01-20', 1),
(2, '春节期间物业费优惠及门禁时间调整公告', '春节期间...', '公告', '全体业主+租户', 380, 610, '2025-01-18', 1),
(3, '元宵节猜灯谜活动汤圆福利发放', '元宵节当天...', '福利', '全体住户', 256, 610, '2025-01-15', 1);

-- 初始化访客
INSERT INTO t_visitor (id, name, phone, owner_id, house_id, reserve_time, access_method, status) VALUES
(1, '张先生', '13900123456', 1, 1, '2025-01-08 14:00', '临时密码', 1),
(2, '李女士', '13800567890', 2, 3, '2025-01-08 16:30', '人脸授权', 0);

-- 初始化门禁记录
INSERT INTO t_access_record (id, access_time, person_name, identity_type, person_id, house_id, access_method, device_name, result) VALUES
(1, '2025-01-08 08:32:15', '王大明', 1, 1, 1, '人脸识别', '南门1号机', 1),
(2, '2025-01-08 08:45:22', '陈租客', 2, 1, 1, '手机开门', '南门1号机', 1),
(3, '2025-01-08 09:12:08', '访客-张先生', 3, 1, 1, '临时密码', '北门2号机', 1),
(4, '2025-01-08 14:28:33', '未知人员', 4, NULL, NULL, '未知', '东门1号机', 0),
(5, '2025-01-08 18:05:47', '刘租客', 2, 2, 3, '刷卡', '南门2号机', 1);
