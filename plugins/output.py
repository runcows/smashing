from beet import Context
from beet.contrib.format_json import format_json
from bolt import Module
from pathlib import Path
import shutil

def beet_default(ctx: Context):
    yield
    ctx.data[Module].clear()
    
    # minify json for release pack
    ctx.require(format_json(indent=None, separators=(",", ":"), final_newline=False))
    
    ctx.data.save(
        path = Path("out") / f"{ctx.minecraft_version}_{ctx.project_name}_v{ctx.project_version}",
        zipped=True,
        overwrite=True,
    )
    
    # reset for dev output pack
    ctx.require(format_json(indent=2, separators=(",", ":"), final_newline=True))

def clear(ctx: Context):
    shutil.rmtree("out",ignore_errors=True)
