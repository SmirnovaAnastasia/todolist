DROP Table IF EXISTS tasks CASCADE;

CREATE TABLE tasks (
    date_ TEXT,
    doings JSONB NOT NULL
);

CREATE INDEX idx_tasks_date ON tasks(date_);
CREATE INDEX idx_tasks_doings ON tasks USING GIN (doings);
