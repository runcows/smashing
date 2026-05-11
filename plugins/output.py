from beet import Context
from beet.contrib.format_json import format_json
from bolt import Module
from github import Github
from importlib import resources
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from pathlib import Path
import requests
import shutil
import zipfile

TEMPLATES = resources.files("src") / "mod_files"
COMMIT_MESSAGE = os.getenv("COMMIT_MSG")
GH_TOKEN = os.getenv("GH_TOKEN")
REPO_LOCATION = "runcows/smashing"
SMITHED_AUTH = os.getenv("SMITHED_AUTH_KEY")

SMITHED_API = "https://api.smithed.dev/v2"


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
    
    jar_name = mod_output(ctx, zip_name)
    
    if GH_TOKEN:
        publish(ctx, zip_name, jar_name)
    else:
        print("No github token. Not publishing.")


def mod_output(ctx: Context, zip_name: str) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape()
    )
    jar_name = f"{ctx.project_id}-{ctx.project_version}"
    shutil.copy(f"out/{zip_name}.zip", f"out/{jar_name}.jar")
    with zipfile.ZipFile(f"out/{jar_name}.jar", 'a') as jar:
        jar.write('pack.png', arcname=f"{ctx.project_id}_pack.png")
        for root, dirs, files in os.walk(TEMPLATES):
            for file in files:
                relative_path = os.path.join(root,file).removeprefix(f"{TEMPLATES}").removeprefix("/").removeprefix("\\").replace("\\","/")
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
    return jar_name


def publish(ctx: Context, zip_name: str, jar_name: str):
    # github release
    g = Github(GH_TOKEN)
    repo = g.get_repo(REPO_LOCATION)
    release = repo.create_git_release(
        tag=f"v{ctx.project_version}",
        name=f"v{ctx.project_version}",
        message=COMMIT_MESSAGE,
        draft=False,
        prerelease=False
    )
    release.upload_asset(path=f"out/{zip_name}.zip")
    gh_release_download_link = ""
    for asset in release.get_assets():
        gh_release_download_link = asset.browser_download_url
        break
    print(f"Github Release Asset Link : {gh_release_download_link}")
    
    # Smithed
    res = requests.get(f"{SMITHED_API}/packs/{ctx.project_id}")
    if not (200 <= res.status_code < 300):
        print(f"Failed to get project... {res.status_code} {res.text}")
        return
    project_json = res.json()
    project_versions = project_json["versions"]
    project_display = project_json["display"]
    current_icon = f"https://raw.githubusercontent.com/{REPO_LOCATION}/main/pack.png"
    current_readme = f"https://raw.githubusercontent.com/{REPO_LOCATION}/main/README.md"
    if project_display["icon"] != current_icon or project_display["webPage"] != current_readme:
        print("updating project readme and icon")
        res = requests.patch(
            f"{SMITHED_API}/packs/{ctx.project_id}",
            params = {'token': SMITHED_AUTH},
            json = {
                "data": {
                    "display": {
                        "icon": current_icon,
                        "webPage": current_readme
                    }
                }
            }
        )
        if not (200 <= res.status_code < 300):
            print(f"Failed to update project description... {res.status_code} {res.text}")
    matching_version = next((v for v in project_versions if v["name"] == ctx.project_version), None)
    if matching_version is not None:
        raise ValueError("Version exists already.")
    res = requests.post(
        f"{SMITHED_API}/packs/{ctx.project_id}/versions",
        params = {'token': SMITHED_AUTH, 'version': ctx.project_version},
        json = {
            "data": {
                "downloads": {
                    "datapack": gh_release_download_link,
                    "resourcepack": ""
                },
                "name": ctx.project_version,
                "supports": ctx.minecraft_version,
                "dependencies": []
            }
        }
    )
    if not (200 <= res.status_code < 300):
        print(f"Failed to publish... {res.status_code} {res.text}")
        return
    print(res.text)