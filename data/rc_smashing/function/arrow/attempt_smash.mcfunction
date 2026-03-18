# @s = arrow that was at smashing speed, now in block
# at undefined
# run from tick

scoreboard players set $valid_block rc_smashing.misc 0
execute at 72756E63-6F77-73-BEC7-F04CE104D run function rc_smashing:arrow/check_block with entity @s inBlockState

execute if score $valid_block rc_smashing.misc matches 0 run return fail
execute at @s run function rc_smashing:smash_block with entity @s inBlockState
execute if score @s rc_smashing.PierceLevel matches 1.. run tag @s add rc_smashing.reapply
