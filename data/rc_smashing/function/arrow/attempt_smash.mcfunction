# @s = arrow that was at smashing speed, now in block
# at undefined
# run from tick

# mark for reapply if has piercelevel
execute if score @s rc_smashing.PierceLevel matches 1.. run tag @s add rc_smashing.reapply

scoreboard players reset $valid_block rc_smashing.misc
execute at 72756E63-6F77-73-BEC7-F04CE104D run function rc_smashing:arrow/check_block with entity @s inBlockState

execute if score $valid_block rc_smashing.misc matches 1 at @s run function rc_smashing:smash_block with entity @s inBlockState
