import inspect
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

import click

from cytomat.climate_controller import ClimateController
from cytomat.config import default_config_file, load_config, save_config
from cytomat.cytomat import Cytomat
from cytomat.maintenance_controller import MaintenanceController
from cytomat.plate_handler import PlateHandler
from cytomat.serial_port import usable_serial_ports
from cytomat.shaker_controller import ShakerController

ControllerSpec = tuple[str, str, str, type[Any]]
CONTROLLERS: tuple[ControllerSpec, ...] = (
    ("plate-handler", "plate_handler", "ph", PlateHandler),
    ("maintenance-controller", "maintenance_controller", "mc", MaintenanceController),
    ("climate-controller", "climate_controller", "cc", ClimateController),
    ("shaker-controller", "shaker_controller", "sc", ShakerController),
)

COMMAND_ALIASES: dict[str, dict[str, str]] = {
    "plate-handler": {
        "open-transfer-door": "door-open",
        "close-transfer-door": "door-close",
        "initialize": "init",
    }
}


class AliasedGroup(click.Group):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._alias_to_primary: dict[str, str] = {}

    def add_alias(self, primary: str, alias: str) -> None:
        self._alias_to_primary[alias] = primary

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        resolved = self._alias_to_primary.get(cmd_name, cmd_name)
        return super().get_command(ctx, resolved)

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        rows: list[tuple[str, str]] = []
        aliases_by_primary: dict[str, list[str]] = defaultdict(list)
        for alias, primary in self._alias_to_primary.items():
            aliases_by_primary[primary].append(alias)

        for subcommand in self.list_commands(ctx):
            command = self.get_command(ctx, subcommand)
            if command is None or command.hidden:
                continue
            aliases = sorted(aliases_by_primary.get(subcommand, []))
            label = (
                subcommand if not aliases else f"{subcommand} [{', '.join(aliases)}]"
            )
            rows.append((label, command.get_short_help_str()))

        if rows:
            with formatter.section("Commands"):
                formatter.write_dl(rows)


@click.group(cls=AliasedGroup)
def main() -> None:
    """Command line interface for open-cytomat."""


def _connection_options(command: Callable[..., Any]) -> Callable[..., Any]:
    command = click.option(
        "--port",
        type=str,
        default=None,
        help=(
            "Serial port. If omitted, COM_port is read from --config-file, "
            "then auto-detected when exactly one usable port is available."
        ),
    )(command)
    command = click.option(
        "--config-file",
        type=click.Path(path_type=Path, dir_okay=False),
        default=default_config_file,
        show_default=True,
        help="Path to JSON config file.",
    )(command)
    return command


@main.group("action", cls=AliasedGroup)
@_connection_options
@click.pass_context
def action(ctx: click.Context, port: str | None, config_file: Path) -> None:
    """Run controller actions or initialize CLI config."""
    ctx.ensure_object(dict)
    ctx.obj["port"] = port
    ctx.obj["config_file"] = config_file


main.add_alias("action", "a")


@action.command("initialize")
@click.option(
    "--com-port",
    "com_port",
    type=str,
    required=False,
    help="Serial COM port to save as COM_port.",
)
@click.option(
    "--port", "com_port", type=str, required=False, help="Alias for --com-port."
)
@click.pass_context
def initialize_config(ctx: click.Context, com_port: str | None) -> None:
    """Initialize/update config JSON with COM_port."""
    state = ctx.find_object(dict) or {}
    config_file = state.get("config_file", default_config_file())
    config = load_config(config_file)
    if com_port is not None:
        config.com_port = com_port
    target = save_config(config, config_file)
    click.echo(f"Saved config: {target}")
    click.echo(f"COM_port={config.com_port}")


cast(AliasedGroup, action).add_alias("initialize", "init")


def _resolve_port(ctx: click.Context) -> str:
    state = ctx.find_object(dict)
    if state is None:
        raise click.UsageError("Could not resolve action state from Click context")

    cached = state.get("resolved_port")
    if cached:
        return cached

    explicit_port = state.get("port")
    if explicit_port:
        state["resolved_port"] = explicit_port
        return explicit_port

    config_file = state.get("config_file", default_config_file())
    configured_port = load_config(config_file).com_port
    if configured_port:
        state["resolved_port"] = configured_port
        return configured_port

    discovered_ports = usable_serial_ports()
    if len(discovered_ports) == 1:
        discovered_port = discovered_ports[0]
        state["resolved_port"] = discovered_port
        click.echo(f"Auto-detected serial port: {discovered_port}", err=True)
        return discovered_port

    if not discovered_ports:
        raise click.UsageError(
            "No serial port configured and no usable serial ports were auto-detected. "
            "Pass --port, or set COM_port via `action initialize --com-port ...`."
        )

    raise click.UsageError(
        "Multiple usable serial ports found: "
        f"{', '.join(discovered_ports)}. "
        "Pass --port, or set COM_port via `action initialize --com-port ...`."
    )


def _resolve_cytomat(ctx: click.Context) -> Cytomat:
    state = ctx.find_object(dict)
    if state is None:
        raise click.UsageError("Could not resolve action state from Click context")

    if "cytomat" not in state:
        state["cytomat"] = Cytomat(_resolve_port(ctx))
    return state["cytomat"]


def _kebab(name: str) -> str:
    return name.replace("_", "-")


def _option_type(parameter: inspect.Parameter) -> click.ParamType | type[Any]:
    annotation = parameter.annotation
    if annotation is inspect._empty:
        return str
    if annotation in (int, float, str):
        return annotation
    if annotation is bool:
        return bool
    return str


def _invoke_factory(controller_attr: str, method_name: str) -> Callable[..., None]:
    def _invoke(**kwargs: Any) -> None:
        ctx = click.get_current_context()
        cytomat = _resolve_cytomat(ctx)
        controller = getattr(cytomat, controller_attr)
        method = getattr(controller, method_name)
        result = method(**kwargs)
        if result is not None:
            click.echo(result)

    return _invoke


def _register_controller_commands() -> None:
    for group_name, controller_attr, group_alias, controller_cls in CONTROLLERS:
        group = AliasedGroup(group_name)

        for method_name, method in inspect.getmembers(
            controller_cls, predicate=inspect.isfunction
        ):
            if method_name.startswith("_"):
                continue

            signature = inspect.signature(method)
            params = [
                parameter
                for parameter in signature.parameters.values()
                if parameter.name != "self"
                and parameter.kind
                in (
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                )
            ]

            callback = _invoke_factory(controller_attr, method_name)
            for parameter in reversed(params):
                callback = click.option(
                    f"--{_kebab(parameter.name)}",
                    required=parameter.default is inspect._empty,
                    default=(
                        None
                        if parameter.default is inspect._empty
                        else parameter.default
                    ),
                    type=_option_type(parameter),
                )(callback)

            command_name = _kebab(method_name)
            command_help = (
                (method.__doc__ or "").strip().splitlines()[0]
                if method.__doc__
                else None
            )
            command = click.command(name=command_name, help=command_help)(callback)
            group.add_command(command)

            alias = COMMAND_ALIASES.get(group_name, {}).get(command_name)
            if alias:
                group.add_alias(command_name, alias)

        action_group = cast(AliasedGroup, action)
        action_group.add_command(group)
        action_group.add_alias(group_name, group_alias)


_register_controller_commands()


if __name__ == "__main__":
    main()
