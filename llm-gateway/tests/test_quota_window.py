"""Which requests fall inside the counting window."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from gateway.config import EPOCH

TZ = ZoneInfo("UTC")


def test_term_window_opens_at_term_start(cfg):
    # The fixture's term starts 2020-01-01.
    during = datetime(2020, 6, 1, 12, 0, tzinfo=TZ)
    assert cfg.period_start(during) == datetime(2020, 1, 1, tzinfo=TZ)


def test_usage_before_term_start_still_counts(cfg):
    """Otherwise keys handed out early would be unmetered until day one.

    A term dated in the future is the normal state of affairs when keys are
    distributed in the week before the first class. Counting from that future
    date would mean every request until then is free and unrecorded against
    the allowance.
    """
    cfg.term_start = datetime(2030, 9, 1).date()
    before = datetime(2030, 8, 20, 9, 0, tzinfo=TZ)
    assert cfg.period_start(before) == EPOCH


def test_day_window_is_local_midnight(cfg):
    cfg.period = "day"
    now = datetime(2026, 3, 5, 23, 59, tzinfo=TZ)
    assert cfg.period_start(now) == datetime(2026, 3, 5, 0, 0, tzinfo=TZ)


def test_week_window_starts_monday(cfg):
    cfg.period = "week"
    thursday = datetime(2026, 3, 5, 10, 0, tzinfo=TZ)
    assert thursday.weekday() == 3
    monday = cfg.period_start(thursday)
    assert monday == datetime(2026, 3, 2, 0, 0, tzinfo=TZ)
    assert monday.weekday() == 0


def test_week_window_is_stable_within_the_week(cfg):
    cfg.period = "week"
    monday = cfg.period_start(datetime(2026, 3, 2, 0, 1, tzinfo=TZ))
    sunday = cfg.period_start(datetime(2026, 3, 8, 23, 59, tzinfo=TZ))
    assert monday == sunday
    # ...and rolls over the moment the next week starts.
    assert cfg.period_start(datetime(2026, 3, 9, 0, 1, tzinfo=TZ)) == monday + timedelta(days=7)
