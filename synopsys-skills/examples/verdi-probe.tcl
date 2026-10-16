puts "SNPS_PROBE_BEGIN"
foreach c [lsort [info commands]] {puts "SNPS_COMMAND $c"}
puts "SNPS_PROBE_END"
exit
