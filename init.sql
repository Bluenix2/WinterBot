-- 8ball features
CREATE SEQUENCE eightball_sqc;

CREATE TABLE eightball (
    id SMALLINT PRIMARY KEY DEFAULT NEXTVAL('eightball_sqc'),
    response TEXT NOT NULL,
    weight SMALLINT NOT NULL DEFAULT 1
);

-- We can't default the id column to the sequence before it's created,
-- and we can't have the sequence owned by the table before it's created.
ALTER SEQUENCE eightball_sqc OWNED BY eightball.id;
