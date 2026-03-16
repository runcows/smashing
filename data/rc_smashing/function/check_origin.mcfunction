# @s = #rc_smashing:smasher
# at undefined
# run from tick

execute if score $mob_griefing_enabled rc_smashing.misc matches 1 run return 1
# mob griefing disabled
# | succeed if player origin
execute on origin if entity @s[type=player] run return 1
# | fail if non player entity origin
execute on origin run return fail
# | succeed if non entity origin
return 1
