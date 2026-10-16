source $::env(SNPS_FRAMEWORK_ROOT)/templates/common.tcl
snps_main {
    foreach name {target_dbs implementation_netlist top sdc spef} { snps_required $name }
    foreach db $target_dbs { read_db $db }
    read_verilog $implementation_netlist
    if {![link_design $top]} { error "PrimeTime link failed" }
    read_sdc $sdc
    read_parasitics -format spef $spef
    source [snps_required signoff_corner_recipe]
    update_timing
    redirect reports/constraints.rpt { check_timing -verbose }
    redirect reports/coverage.rpt { report_analysis_coverage }
    redirect reports/setup.rpt { report_timing -delay_type max -max_paths 20 }
    redirect reports/hold.rpt { report_timing -delay_type min -max_paths 20 }
    # Run each required corner/mode. Inspect annotation coverage, endpoints,
    # path exceptions and units before emitting normalized metrics/checks.
}
