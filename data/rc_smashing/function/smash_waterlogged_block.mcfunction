# This function is only needed to prevent parsing failures in parent function
# @s = abstract arrow smashing a block
# at @s
# run from smash_block
# with $Name = block state name

$fill ~-0.07 ~-0.07 ~-0.07 ~0.07 ~0.07 ~0.07 water replace $(Name)[waterlogged=true] destroy
