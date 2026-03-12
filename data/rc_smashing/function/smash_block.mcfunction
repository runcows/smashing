# @s = abstract arrow smashing a block
# at @s
# run from arrow/attempt_smash
# run from trident/attempt_smash
# with $Name = block state name

execute if data entity @s inBlockState.Properties{waterlogged:"true"} run return run function rc_smashing:smash_waterlogged_block with entity @s inBlockState
$fill ~-0.07 ~-0.07 ~-0.07 ~0.07 ~0.07 ~0.07 air replace $(Name) destroy
