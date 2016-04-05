-- We take advantage of MySQL events to keep records clean
-- No info is lost, since attempts are logged as well
create event if not exists LoginAttemptsCleanup
    on schedule every 1 hour
    do delete from LoginAttempt
        where timestamp < (now() - interval 1 hour);

-- Activate the event scheduler
set global event_scheduler = on;

