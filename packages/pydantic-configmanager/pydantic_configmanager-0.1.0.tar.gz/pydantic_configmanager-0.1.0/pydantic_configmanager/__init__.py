"""Top-level package for Pydantic Configuration Manager."""

from os import environ
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound='EnvironmentBaseModel')


class EnvironmentBaseModel(BaseModel):
    """Base config class based on a Pydantic Base Model."""

    class Config:
        """Configuratio for the Config class via a... Config class."""

        allow_population_by_field_name = False
        env_prefix = ''
        name_prefix = ''
        env_postfix = ''

        @classmethod
        def alias_generator(cls, fieldname: str) -> str:
            """Create aliases with a prefix."""
            env = str(cls.env_prefix)
            if env:
                env = f"{env}_"
            return f'{cls.name_prefix}{env}{fieldname}{cls.env_postfix}'.upper()

    @classmethod
    def env_config(cls, by_alias: bool = True, include_export=False) -> str:
        """Return settings template as they would go into environment."""
        export = ''
        if include_export:
            export = "export "
        schema = cls.schema(by_alias)
        output: str = f"# {schema.get('description','')}\n"
        output += '# -----\n'
        output += '# These are the supported environment configuration variables.\n'
        output += '# Set these up in your environment.\n'
        output += '\n'
        properties = schema.get('properties', {})
        for property_name, values in properties.items():
            type_value = values.get('type', '')
            if type_value:  # if a type is set, format the output:
                type_value = f", type: {type_value}"
            default_value = values.get('default')
            default_repr = ''  #
            if default_value:
                default_repr = f"{values.get('default')!a}"
            description = f"{values.get('description', values.get('title'))}"
            comment = f"  # {description}{type_value}"
            output_line = f"{export}{property_name}={default_repr}{comment}\n"
            output += output_line
        return output

    @classmethod
    def from_env(cls, **data: Any) -> T:
        """Initialize object from environmnent variables."""
        data = data or {}
        data.update(environ)
        return cls(**data)  # type: ignore
