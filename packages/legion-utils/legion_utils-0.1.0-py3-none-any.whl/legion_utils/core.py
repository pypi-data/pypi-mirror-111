from enum import IntEnum
from typing import Dict, Any, Optional

from robotnikmq import Topic, Message, RobotnikConfig
from typeguard import typechecked


@typechecked
class Priority(IntEnum):
    INFO = 0
    ACTIVITY = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


@typechecked
def broadcast(exchange: str,
              route: str,
              ttl: int,
              priority: Priority,
              contents: Dict[str, Any],
              config: Optional[RobotnikConfig] = None):
    _contents = {'priority': priority.value}
    if ttl != 0:
        _contents['ttl'] = ttl
    _contents.update(contents)
    route += f'.{priority.name.lower()}'
    Topic(exchange=exchange, config=config).broadcast(Message(contents=_contents),
                                                      routing_key=route)


@typechecked
def broadcast_info(exchange: str, route: str, contents: Dict[str, Any],
                   config: Optional[RobotnikConfig] = None):
    broadcast(exchange, route, ttl=0, priority=Priority.INFO, contents=contents, config=config)


@typechecked
def broadcast_activity(exchange: str, route: str, contents: Dict[str, Any],
                       config: Optional[RobotnikConfig] = None):
    broadcast(exchange, route, ttl=0, priority=Priority.ACTIVITY, contents=contents, config=config)


@typechecked
def broadcast_alert(exchange: str,
                    route: str,
                    contents: Dict[str, Any],
                    ttl: int = 30,
                    priority: Priority = Priority.WARNING,
                    config: Optional[RobotnikConfig] = None):
    broadcast(exchange, route, ttl=ttl, priority=priority, contents=contents, config=config)


@typechecked
def broadcast_warning(exchange: str, route: str, contents: Dict[str, Any],
                      ttl: int = 30, config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, contents, ttl=ttl, priority=Priority.WARNING, config=config)


@typechecked
def broadcast_error(exchange: str, route: str, contents: Dict[str, Any],
                    ttl: int = 30, config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, contents, ttl=ttl, priority=Priority.ERROR, config=config)


@typechecked
def broadcast_critical(exchange: str, route: str, contents: Dict[str, Any],
                       ttl: int = 30, config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, contents, ttl=ttl, priority=Priority.CRITICAL, config=config)
