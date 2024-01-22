-- 用户权限表
CREATE TABLE IF NOT EXISTS public.dim_role
(
    user_id      SERIAL PRIMARY KEY,
    user_name    VARCHAR,
    password     VARCHAR,
    permission   VARCHAR,
    created_time TIMESTAMP,
    updated_time TIMESTAMP
);

-- 字典类型表
CREATE TABLE IF NOT EXISTS public.dim_dict_type
(
    dict_type_id SERIAL PRIMARY KEY,
    dict_type    VARCHAR,
    status       int, -- 0 停用 1 正常
    notes        VARCHAR,
    create_time  TIMESTAMP,
    create_user  VARCHAR,
    update_time  TIMESTAMP,
    update_user  VARCHAR
);

-- 字典值表
CREATE TABLE IF NOT EXISTS public.dim_dict_data
(
    dict_id      SERIAL PRIMARY KEY,
    dict_name    VARCHAR,
    dict_type_id INT,
    dict_type    VARCHAR,
    dict_value   VARCHAR,
    status       int,
    create_time  TIMESTAMP,
    create_user  VARCHAR,
    update_time  TIMESTAMP,
    update_user  VARCHAR
);

-- 社团维表
CREATE TABLE IF NOT EXISTS public.dim_group
(
    group_id      SERIAL PRIMARY KEY,
    group_name    VARCHAR,
    group_type_id INT,
    group_type    VARCHAR,
    profile_path  VARCHAR,
    photo_path    VARCHAR,
    group_info    VARCHAR,
    create_time   TIMESTAMP,
    create_user   VARCHAR,
    update_time   TIMESTAMP,
    update_user   VARCHAR
);

-- 活动维表
CREATE TABLE IF NOT EXISTS public.dim_activity
(
    activity_id        SERIAL PRIMARY KEY,
    activity_name      VARCHAR,
    activity_status      VARCHAR,
    activity_type_id   INT,
    activity_type      VARCHAR,
    photo_path         VARCHAR,
    number_limit_lower INT,
    number_limit_upper INT,
    price              FLOAT,
    region_id          INT,
    region             VARCHAR,
    group_id           INT,
    group_name         VARCHAR,
    start_time         TIMESTAMP,
    end_time           TIMESTAMP,
    register_end_time  TIMESTAMP,
    activity_info      VARCHAR,
    create_time        TIMESTAMP,
    create_user        VARCHAR,
    update_time        TIMESTAMP,
    update_user        VARCHAR
);


