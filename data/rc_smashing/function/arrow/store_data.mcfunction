# @s = arrow at speed, by definition this excludes arrows tagged for reapply
# at undefined
# run from tick

# store PierceLevel
execute store result score @s rc_smashing.PierceLevel run data get entity @s PierceLevel

# store Motion
data modify entity @s data.rc_smashing.prev_motion set from entity @s Motion
