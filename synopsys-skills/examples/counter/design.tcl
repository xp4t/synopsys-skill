# The user supplies the logical library and its documented units.
set top counter
set rtl_format sverilog
set rtl [list $::env(SNPS_FRAMEWORK_ROOT)/examples/counter/rtl/counter.sv]
if {![info exists ::env(TARGET_DB)] || ![file isfile $::env(TARGET_DB)]} {
    error "Set TARGET_DB to a suitable local logical library"
}
set target_dbs [list $::env(TARGET_DB)]
set sdc $::env(SNPS_FRAMEWORK_ROOT)/examples/counter/constraints.sdc
