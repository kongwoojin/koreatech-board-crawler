module default {
    scalar type Department extending enum<ARCH, CSE, DORM, EMC, IDE, ITE, MECHANICAL, MECHATRONICS, SCHOOL, SIM>;

    scalar type Category extending enum<None, Notice, EA, CA, Work, ETC>;

    type notice {
        required property department -> Department;
        required property board -> str;
        required property num -> str;
        required property is_notice -> bool;
        required property category -> Category;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property notice_start_date -> cal::local_date;
        required property notice_end_date -> cal::local_date;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property init_crawled_time -> cal::local_datetime;
        required property update_crawled_time -> cal::local_datetime;
    }

    type Files {
        required property file_name -> str;
        required property file_url -> str {
            constraint exclusive;
        };
    }
}
