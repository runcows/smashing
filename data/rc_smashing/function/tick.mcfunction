# scheduled from init
# scheduled from self

schedule function rc_smashing:tick 1t

# arrow
execute as @e[type=#minecraft:arrows,tag=rc_smashing.at_speed,tag=!smithed.entity,predicate=rc_smashing:not_moving] \
  run function rc_smashing:arrow/attempt_smash
# trident
execute as @e[tag=rc_smashing.at_speed,tag=!smithed.entity,predicate=rc_smashing:not_moving,type=trident] \
  run function rc_smashing:trident/attempt_smash

tag @e[type=#rc_smashing:smasher,tag=rc_smashing.at_speed,tag=!smithed.entity,predicate=!rc_smashing:smashing_speed] remove rc_smashing.at_speed
tag @e[type=#rc_smashing:smasher,tag=!rc_smashing.at_speed,tag=!smithed.entity,predicate=rc_smashing:smashing_speed] add rc_smashing.at_speed
