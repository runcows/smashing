# scheduled from init
# scheduled from self

schedule function rc_smashing:slow_clock 5s

execute store result score $mob_griefing_enabled rc_smashing.misc run gamerule mobGriefing
