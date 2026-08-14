import json
from pathlib import Path

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CytomatConfig(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    com_port: str | None = Field(
        default=None,
        alias="COM_port",
        validation_alias=AliasChoices("COM_port", "com_port"),
    )


def default_config_file() -> Path:
    return Path.home() / ".config" / "open-cytomat" / "config.json"


def load_config(config_file: Path | None = None) -> CytomatConfig:
    target = config_file or default_config_file()
    if not target.exists():
        return CytomatConfig()

    with target.open("r", encoding="utf-8") as handle:
        return CytomatConfig.model_validate(json.load(handle))


def save_config(config: CytomatConfig, config_file: Path | None = None) -> Path:
    target = config_file or default_config_file()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(config.model_dump(by_alias=True, exclude_none=True), handle, indent=2)
        handle.write("\n")
    return target
