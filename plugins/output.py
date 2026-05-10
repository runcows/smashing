from beet import Context
from beet.contrib.format_json import format_json
from bolt import Module
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from pathlib import Path
import shutil
import zipfile

TEMPLATES = "src/mod_files"
env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape()
)


def clear(ctx: Context):
    shutil.rmtree("out",ignore_errors=True)
    
def beet_default(ctx: Context):
    yield
    ctx.data[Module].clear()
    
    # minify json for release pack
    ctx.require(format_json(indent=None, separators=(",", ":"), final_newline=False))
    
    output_name = f"{ctx.minecraft_version}_{ctx.project_name}_v{ctx.project_version}"
    ctx.data.save(
        path = Path("out") / output_name,
        zipped=True,
        overwrite=True,
    )
    
    # reset for dev output pack
    ctx.require(format_json(indent=2, separators=(",", ":"), final_newline=True))
    
    mod_output(ctx, output_name)

def mod_output(ctx: Context, zip_name: str):
    jar_name = f"{ctx.project_id}-{ctx.project_version}"
    shutil.copy(f"out/{zip_name}.zip", f"out/{jar_name}.jar")
    with zipfile.ZipFile(f"out/{jar_name}.jar", 'a') as jar:
        jar.write('pack.png', arcname=f"{ctx.project_id}_pack.png")
        for root, dirs, files in os.walk(TEMPLATES):
            for file in files:
                relative_path = os.path.join(root,file).removeprefix(f"{TEMPLATES}\\").replace("\\","/")
                template = env.get_template(relative_path)
                rendered_template = template.render(
                    author = ctx.project_author,
                    id = ctx.project_id,
                    name = ctx.project_name,
                    version = ctx.project_version,
                    description = ctx.project_description,
                    modrinth_page = "https://modrinth.com/datapack/rc_smashing",
                    github_page = "https://github.com/runcows/smashing",
                )
                jar.writestr(relative_path, rendered_template)
                
