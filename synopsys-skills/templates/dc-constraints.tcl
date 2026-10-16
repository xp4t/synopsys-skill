source $::env(SNPS_FRAMEWORK_ROOT)/templates/common.tcl
snps_main {
    foreach name {top rtl rtl_format target_dbs sdc} { snps_required $name }
    set_app_var target_library $target_dbs
    set_app_var link_library [concat * $target_dbs]
    define_design_lib WORK -path ./WORK
    if {![analyze -format $rtl_format $rtl]} { error "Analysis failed" }
    if {![elaborate $top]} { error "Elaboration failed" }
    current_design $top
    if {![link]} { error "Link failed" }
    read_sdc $sdc
    redirect reports/clocks.rpt { report_clock }
    redirect reports/constraints.rpt { check_timing }
    # Validate clocks/IO/exceptions/unconstrained classes against the approved
    # requirements, using a report adapter for this design/methodology. A command
    # return value alone does not establish path coverage. Emit result.json only
    # after that adapter's evidence checks; the runner rejects its absence.
}
