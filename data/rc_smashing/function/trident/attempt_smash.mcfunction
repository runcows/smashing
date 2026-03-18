# @s = trident that was at smashing speed, now in block
# at undefined
# run from tick

scoreboard players set $valid_block rc_smashing.misc 0
execute at 72756E63-6F77-73-BEC7-F04CE104D run function rc_smashing:trident/check_block with entity @s inBlockState

execute if score $valid_block rc_smashing.misc matches 1 at @s run function rc_smashing:smash_block with entity @s inBlockState
