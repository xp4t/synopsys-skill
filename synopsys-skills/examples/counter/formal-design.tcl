source $::env(SNPS_FRAMEWORK_ROOT)/examples/counter/design.tcl
foreach key {IMPLEMENTATION_NETLIST SYNTHESIS_SVF} {
    if {![info exists ::env($key)] || ![file isfile $::env($key)]} {
        error "Missing configured formal input: $key"
    }
}
set implementation_netlist $::env(IMPLEMENTATION_NETLIST)
set synthesis_svf $::env(SYNTHESIS_SVF)
