module default {
    type arch {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type cse {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type dorm {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type emc {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }
    type ide {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type ite {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type mechanical {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type mechatronics {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type school {
        required property board -> str;
        required property num -> str;
        required property is_importance -> bool;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type sim {
        required property board -> str;
        required property num -> str;
        required property title -> str;
        required property writer -> str;
        required property write_date -> cal::local_date;
        required property read_count -> int64;
        required property article_url -> str {
            constraint exclusive;
        };
        required property content -> str;
        multi link files -> Files {
            on target delete allow;
        };
        required property crawled_time -> cal::local_datetime;
    }

    type Files {
        required property file_name -> str;
        required property file_url -> str {
            constraint exclusive;
        };
    }
}
