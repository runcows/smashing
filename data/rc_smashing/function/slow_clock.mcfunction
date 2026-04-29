# scheduled from init
# scheduled from self

schedule function rc_smashing:slow_clock 5s

execute store result score $mob_griefing_enabled rc_smashing.misc run gamerule mob_griefing

execute store result score $projectiles_can_break_blocks rc_smashing.misc run gamerule projectiles_can_break_blocks
