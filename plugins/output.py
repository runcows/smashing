from beet import Context
from beet.contrib.format_json import format_json
from bolt import Module
from importlib import resources
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os
from pathlib import Path
import shutil


def clear(ctx: Context):
    shutil.rmtree("out",ignore_errors=True)

def beet_default(ctx: Context):
    yield
    ctx.data[Module].clear()
    
    # minify json for release pack
    ctx.require(format_json(indent=None, separators=(",", ":"), final_newline=False))
    
    zip_name = f"{ctx.minecraft_version}_{ctx.project_name}_v{ctx.project_version}"
    ctx.data.save(
        path = Path("out") / zip_name,
        zipped=True,
        overwrite=True,
    )
    
    # reset for dev output pack
    ctx.require(format_json(indent=2, separators=(",", ":"), final_newline=True))
