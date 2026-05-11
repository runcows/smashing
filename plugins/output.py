from beet import Context
from beet.contrib.format_json import format_json
from bolt import Module
from github import Github
from importlib import resources
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
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

MODRINTH_AUTH = os.getenv("MODRINTH_AUTH_KEY")
MODRINTH_API = "https://api.modrinth.com/v2"
MODRINTH_PROJECT_ID = "h3NiCjT1"


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
    if not SMITHED_AUTH:
        raise ValueError("NO SMITHED AUTH KEY")
    if not MODRINTH_AUTH:
        raise ValueError("No MODRINTH AUTH KEY")
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
        raise RuntimeError(f"SMITHED: Failed to get project... {res.status_code} {res.text}")
    project_json = res.json()
    project_versions = project_json["versions"]
    project_display = project_json["display"]
    current_icon = f"https://raw.githubusercontent.com/{REPO_LOCATION}/main/pack.png"
    current_readme = f"https://raw.githubusercontent.com/{REPO_LOCATION}/main/README.md"
    if project_display["icon"] != current_icon or project_display["webPage"] != current_readme:
        print("SMITHED: Updating project readme and icon")
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
            print(f"SMITHED: Failed to update project readme and icon... {res.status_code} {res.text}")
    matching_version = next((v for v in project_versions if v["name"] == ctx.project_version), None)
    if matching_version is not None:
        raise ValueError("SMITHED: Version exists already.")
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
                "supports": ctx.meta["supported_versions"],
                "dependencies": []
            }
        }
    )
    if not (200 <= res.status_code < 300):
        raise ValueError(f"SMITHED: Failed to publish... {res.status_code} {res.text}")
    print(f"SMITHED: {res.text}")
    
    # Modrinth
    USER_AGENT = "Smashing Github Actions"
    res = requests.get(
        f"{MODRINTH_API}/project/{MODRINTH_PROJECT_ID}",
        headers = {'Authorization': MODRINTH_AUTH, 'User-Agent': USER_AGENT}
    )
    if not (200 <= res.status_code < 300):
        raise RuntimeError(f"MODRINTH: Failed to get project... {res.status_code} {res.text}")
    if res.json()["body"] != current_readme:
        print("MODRINTH: Updating Project Description")
        res = requests.patch(
            f"{MODRINTH_API}/project/{MODRINTH_PROJECT_ID}",
            headers = {'Authorization': MODRINTH_AUTH, 'User-Agent': USER_AGENT},
            json = {
                "body": current_readme
            }
        )
        if not (200 <= res.status_code < 300):
            print(f"MODRINTH: Failed to update project description... {res.status_code} {res.text}")
    res = requests.get(
        f"{MODRINTH_API}/project/{MODRINTH_PROJECT_ID}/version",
        headers = {'Authorization': MODRINTH_AUTH, 'User-Agent': USER_AGENT}
    )
    if not (200 <= res.status_code < 300):
        raise RuntimeError(f"MODRINTH: Failed to get project versions... {res.status_code} {res.text}")
    project_json = res.json()
    matching_version = next((v for v in project_json if v["version_number"] == ctx.project_version), None)
    if matching_version is not None:
        raise ValueError("MODRINTH: Version exists already.")
    # - Post Zip
    with open(f"out/{zip_name}.zip", "rb") as zf:
        zip_bytes = zf.read()
    res = requests.post(
        f"{MODRINTH_API}/version",
        headers = {'Authorization': MODRINTH_AUTH, 'User-Agent': USER_AGENT},
        files = {
            "data": json.dumps({
                "name": f"{ctx.project_name} {ctx.project_version}",
                "version_number": ctx.project_version,
                "changelog": COMMIT_MESSAGE,
                "dependencies": [],
                "game_versions": ctx.meta["supported_versions"],
                "version_type": "release",
                "loaders": ["datapack"],
                "featured": False,
                "project_id": MODRINTH_PROJECT_ID,
                "file_parts": [f"{zip_name}.zip"]
            }),
            f"{zip_name}.zip": zip_bytes
        }
    )
    if not (200 <= res.status_code < 300):
        raise ValueError(f"MODRINTH: Failed to publish Zip... {res.status_code} {res.text}")
    print(f"MODRINTH: Successfully Published Zip {res.json()["name"]}")
    # - Post Jar
    with open(f"out/{jar_name}.jar", "rb") as jf:
        jar_bytes = jf.read()
    res = requests.post(
        f"{MODRINTH_API}/version",
        headers = {'Authorization': MODRINTH_AUTH, 'User-Agent': USER_AGENT},
        files = {
            "data": json.dumps({
                "name": f"{ctx.project_name} {ctx.project_version}",
                "version_number": ctx.project_version,
                "changelog": COMMIT_MESSAGE,
                "dependencies": [],
                "game_versions": ctx.meta["supported_versions"],
                "version_type": "release",
                "loaders": ["fabric","quilt","forge","neoforge"],
                "featured": False,
                "project_id": MODRINTH_PROJECT_ID,
                "file_parts": [f"{jar_name}.jar"]
            }),
            f"{jar_name}.jar": jar_bytes
        }
    )
    if not (200 <= res.status_code < 300):
        raise ValueError(f"MODRINTH: Failed to publish Jar... {res.status_code} {res.text}")
    print(f"MODRINTH: Successfully Published Jar {res.json()["name"]}")
