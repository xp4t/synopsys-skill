puts "SNPS_COMMANDS_BEGIN"
foreach command [lsort [info commands]] { puts "SNPS_COMMAND $command" }
puts "SNPS_COMMANDS_END"
puts "SNPS_HELP_BEGIN"
help -groups
help -verbose help
man help
if {[llength [info commands list_licenses]]} { list_licenses }
puts "SNPS_HELP_END"
exit
