from datetime import datetime
from typing import Any, Callable, Optional, TypeVar

from rx.core import Observable, abc, typing
from rx.disposable import CompositeDisposable
from rx.scheduler import TimeoutScheduler

_T = TypeVar("_T")


def take_until_with_time_(
    end_time: typing.AbsoluteOrRelativeTime,
    scheduler: Optional[abc.SchedulerBase] = None,
) -> Callable[[Observable[_T]], Observable[_T]]:
    def take_until_with_time(source: Observable[_T]) -> Observable[_T]:
        """Takes elements for the specified duration until the specified end
        time, using the specified scheduler to run timers.

        Examples:
            >>> res = take_until_with_time(source)

        Args:
            source: Source observale to take elements from.

        Returns:
            An observable sequence with the elements taken
            until the specified end time.
        """

        def subscribe(
            observer: abc.ObserverBase[_T],
            scheduler_: Optional[abc.SchedulerBase] = None,
        ) -> abc.DisposableBase:
            _scheduler = scheduler or scheduler_ or TimeoutScheduler.singleton()

            if isinstance(end_time, datetime):
                scheduler_method = _scheduler.schedule_absolute
            else:
                scheduler_method = _scheduler.schedule_relative

            def action(scheduler: abc.SchedulerBase, state: Any = None):
                observer.on_completed()

            task = scheduler_method(end_time, action)
            return CompositeDisposable(
                task, source.subscribe(observer, scheduler=scheduler_)
            )

        return Observable(subscribe)

    return take_until_with_time


__all__ = ["take_until_with_time_"]
