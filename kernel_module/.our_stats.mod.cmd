savedcmd_our_stats.mod := printf '%s\n'   our_stats.o | awk '!x[$$0]++ { print("./"$$0) }' > our_stats.mod
