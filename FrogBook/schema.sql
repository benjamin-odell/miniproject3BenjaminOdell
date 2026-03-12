DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    battles integer not null default 0
);

CREATE TABLE frog(
    id integer primary key autoincrement,
    user_id integer not null,
    created timestamp not null default current_timestamp,
    name TEXT not null,
    img text not null,
    elo integer not null default 1000,
    battles integer not null default 0,
    wins integer not null default 0,
    foreign key (user_id) references user (id)
);

create table battles(
    id integer primary key autoincrement,
    user_id integer not null,
    frog1_id integer not null,
    frog2_id integer not null,
    winner_id integer not null,
    created timestamp not null default current_timestamp,
    foreign key (user_id) references user (id),
    foreign key (frog1_id) references frog (id),
    foreign key (frog2_id) references frog (id),
    foreign key (winner_id) references frog (id)
);