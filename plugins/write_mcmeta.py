from beet import Context

def beet_default(ctx: Context):
  ctx.data.min_format = 121
  ctx.data.max_format = 121
  
  for pack in ctx.packs:
    pack.mcmeta.data["id"] = ctx.project_id
    
    pack.description = [
      f"{ctx.project_name} v{ctx.project_version}\n",
      {
        "text": ctx.project_author,
        "color": "#da3eb3"
      }
    ]
