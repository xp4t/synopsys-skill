source $::env(SNPS_FRAMEWORK_ROOT)/examples/counter/design.tcl
if {[info exists ::env(SNPS_RESTORE_DIR)]} {
    set implementation_netlist $::env(SNPS_RESTORE_DIR)/mapped.v
    set synthesis_svf $::env(SNPS_RESTORE_DIR)/synthesis.svf
}
