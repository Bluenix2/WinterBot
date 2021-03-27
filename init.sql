-- Automation/Purge
CREATE TABLE purges (
    channel_id BIGINT PRIMARY KEY
);

-- Automation/Reactions
CREATE TABLE reactions (
    message_id BIGINT PRIMARY KEY
)

-- Automation/Roles
CREATE TABLE roles (
    message_id BIGINT NOT NULL,
    reaction VARCHAR NOT NULL,
    role_id BIGINT NOT NULL,

    PRIMARY KEY(message_id, reaction)
)

-- Miscellanous/8Ball
CREATE SEQUENCE eightball_sqc;

CREATE TABLE eightball (
    id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('eightball_sqc'),
    response TEXT NOT NULL,
    weight SMALLINT NOT NULL DEFAULT 1
);

-- We can't default the id column to the sequence before it's created,
-- and we can't have the sequence owned by the table before it's created.
ALTER SEQUENCE eightball_sqc OWNED BY eightball.id;
