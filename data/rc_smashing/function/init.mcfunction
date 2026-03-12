scoreboard players set rc_smashing load.status 1
scoreboard players set rc_smashing_minor load.status 0

scoreboard objectives add rc_smashing.misc dummy

# ascii runcows = 114, 117, 110, 99, 111, 119, 115
# HEX = 72 75 6E 63 6F 77 73
# multiply each by the characters remaining
# 7*114 + 6*117 + 5*110 + 4*99 + 3*111 + 2*119 + 1*115  =   3132
forceload add 29999999 3132
# UUID = 72756E63-6F77-73-BEC7-F04CE104D
summon marker 29999999 ~ 3132 {Tags:["rc_smashing.forceload_marker"],UUID:[I;1920298595,1870069875,-1094254577,80613453]}

schedule function rc_smashing:tick 1t
