source $::env(SNPS_FRAMEWORK_ROOT)/templates/common.tcl
snps_main {
    foreach name {top rtl rtl_format target_dbs sdc} { snps_required $name }
    set_app_var target_library $target_dbs
    set_app_var link_library [concat * $target_dbs]
    define_design_lib WORK -path ./WORK
    set_svf outputs/synthesis.svf
    if {![analyze -format $rtl_format $rtl]} { error "RTL analysis failed" }
    if {![elaborate $top]} { error "RTL elaboration failed" }
    current_design $top
    if {![link]} { error "Design link failed" }
    if {![check_design]} { error "Initial design checks failed" }
    read_sdc $sdc
    redirect reports/constraints.rpt { check_timing }
    # Preserve the approved SDC: this template never changes clocks or exceptions.
    if {![compile -map_effort [snps_parameter synthesis_map_effort medium]]} { error "Synthesis failed" }
    set clean [check_design]
    set unmapped [get_cells -hierarchical -filter {is_unmapped == true}]
    if {[sizeof_collection $unmapped] != 0 || !$clean} { error "Unmapped cells or design errors" }
    redirect reports/design.rpt { check_design }
    redirect reports/area.rpt { report_area }
    redirect reports/timing.rpt { report_timing -max_paths 10 }
    redirect reports/power.rpt { report_power }
    redirect reports/qor.rpt { report_qor }
    redirect reports/units.rpt { report_units }
    write_file -format ddc -hierarchy -output outputs/mapped.ddc
    write_file -format verilog -hierarchy -output outputs/mapped.v
    write_sdc outputs/mapped.sdc
    set_svf -off
    # Design-object attributes vary across releases; retain the report as evidence.
    # Extract only the documented report_area total, retaining the source report.
    set f [open reports/area.rpt r]
    set area_report [read $f]
    close $f
    if {![regexp {Total cell area:\s+([0-9.eE+-]+)} $area_report -> area_library_units]} {
        error "No total cell area found in report_area output"
    }
    set f [open reports/timing.rpt r]
    set timing_report [read $f]
    close $f
    set slacks [regexp -all -inline {slack\s+\((?:MET|VIOLATED)\)\s+([0-9.eE+-]+)} $timing_report]
    if {![llength $slacks]} { error "No reported slack available for comparison" }
    set minimum_slack Inf
    foreach {match value} $slacks {
        if {$value < $minimum_slack} { set minimum_slack $value }
    }
    snps_result [dict create mapped 1 design_checks_clean $clean constraints_preserved 1] \
        [dict create area_library_units $area_library_units worst_reported_slack_library_time_units $minimum_slack] \
        {reports/design.rpt reports/area.rpt reports/timing.rpt reports/power.rpt reports/qor.rpt reports/constraints.rpt reports/units.rpt}
}
