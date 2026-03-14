# run from #minecraft:tick

# reapply piercing arrow data
execute as @e[type=#minecraft:arrows,tag=rc_smashing.reapply] run function rc_smashing:arrow/reapply_data

# arrow
execute as @e[type=#minecraft:arrows,tag=rc_smashing.at_speed,predicate=rc_smashing:not_moving] \
  run function rc_smashing:arrow/attempt_smash
# trident
execute as @e[tag=rc_smashing.at_speed,predicate=rc_smashing:not_moving,type=trident] \
  run function rc_smashing:trident/attempt_smash

# update speed tracking
tag @e[type=#rc_smashing:smasher,tag=rc_smashing.at_speed,predicate=!rc_smashing:smashing_speed] remove rc_smashing.at_speed
tag @e[type=#rc_smashing:smasher,tag=!rc_smashing.at_speed,tag=!smithed.entity,predicate=rc_smashing:smashing_speed] add rc_smashing.at_speed

# store arrow data
execute as @e[type=#minecraft:arrows,tag=rc_smashing.at_speed] run function rc_smashing:arrow/store_data
