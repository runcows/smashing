# @s = arrow
# at 72756E63-6F77-73-BEC7-F04CE104D (forceload chunk marker)
# run from arrow/attempt_smash
# with $Name = block state name

$setblock ~ ~ ~ $(Name) strict
execute store result score $valid_block rc_smashing.misc if block ~ ~ ~ #rc_smashing:arrow_smashable
setblock ~ ~ ~ air strict
