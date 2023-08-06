from typing import Any

from . import hookimpl, systemd
from .ctx import BaseContext, Context
from .model import Instance
from .pgbackrest import BackupType, backup


def systemd_timer(instance: Instance) -> str:
    """Return systemd timer name for 'instance'.

    >>> from pglift.settings import Settings
    >>> instance = Instance("test", "13", Settings())
    >>> systemd_timer(instance)
    'postgresql-backup@13-test.timer'
    """
    return f"postgresql-backup@{instance.version}-{instance.name}.timer"


@hookimpl  # type: ignore[misc]
def instance_configure(ctx: BaseContext, instance: Instance, **kwargs: Any) -> None:
    """Enable scheduled backup job for configured instance."""
    if ctx.settings.scheduler == "systemd":
        unit = systemd_timer(instance)
        systemd.enable(ctx, unit)


@hookimpl  # type: ignore[misc]
def instance_drop(ctx: BaseContext, instance: Instance) -> None:
    """Disable scheduled backup job when instance is being dropped."""
    if ctx.settings.scheduler == "systemd":
        systemd.disable(ctx, systemd_timer(instance), now=True)


@hookimpl  # type: ignore[misc]
def instance_start(ctx: BaseContext, instance: Instance) -> None:
    """Start schedule backup job at instance startup."""
    if ctx.settings.scheduler == "systemd":
        systemd.start(ctx, systemd_timer(instance))


@hookimpl  # type: ignore[misc]
def instance_stop(ctx: BaseContext, instance: Instance) -> None:
    """Stop schedule backup job when instance is stopping."""
    if ctx.settings.scheduler == "systemd":
        systemd.stop(ctx, systemd_timer(instance))


# This entry point is used by systemd 'postgresql-backup@' service.
if __name__ == "__main__":  # pragma: nocover
    import argparse
    import sys

    from .pm import PluginManager
    from .settings import SETTINGS

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "stanza", metavar="<version>-<name>", help="instance identifier"
    )

    def do_backup(
        ctx: BaseContext, instance: Instance, args: argparse.Namespace
    ) -> None:
        return backup(ctx, instance, type=BackupType(args.type))

    parser.set_defaults(func=do_backup)
    parser.add_argument(
        "--type",
        choices=[t.name for t in BackupType],
        default=BackupType.default().name,
    )

    args = parser.parse_args()
    ctx = Context(plugin_manager=PluginManager.get(), settings=SETTINGS)
    try:
        instance = Instance.from_stanza(args.stanza, settings=SETTINGS)
    except ValueError as e:
        parser.error(str(e))
    if not instance.exists():
        print(f"error: instance {instance} not found", file=sys.stderr)
        sys.exit(1)
    args.func(ctx, instance, args)
