# @s = arrow with rc_smashing.reapply tag
# at undefined
# run from tick

tag @s remove rc_smashing.reapply

# re-set and decrement PierceLevel
execute store result entity @s PierceLevel byte 1 run scoreboard players remove @s rc_smashing.PierceLevel 1

# set Motion
data modify entity @s Motion set from entity @s data.rc_smashing.prev_motion
# | Note: this has issues.
# |   Reapplying the Motion from 2 ticks prior means this arrow reaccelerates, seemingly ignoring drag and gravity.
# |   I have tried to mimic the effects of those on this reapplied motion before. Unfortunately, the Motion tag is quite inaccurate and buggy.
# |   The effects were that the arrow would randomly shoot off in directions that didnt make sense, or accelerate wildly.
# |   Yes, I checked my math. No, it doesn't make sense. This is the best I can do. 
