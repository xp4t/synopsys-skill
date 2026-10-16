source $::env(SNPS_FRAMEWORK_ROOT)/templates/common.tcl
snps_main {
    foreach name {top rtl rtl_format target_dbs} { snps_required $name }
    set_app_var target_library $target_dbs
    set_app_var link_library [concat * $target_dbs]
    define_design_lib WORK -path ./WORK
    if {![analyze -format $rtl_format $rtl]} { error "RTL syntax/analysis failed" }
    if {![elaborate $top]} { error "RTL elaboration failed" }
    current_design $top
    if {![link]} { error "Missing hierarchy/library dependency" }
    set clean [check_design]
    redirect reports/design.rpt { check_design }
    redirect reports/hierarchy.rpt { report_hierarchy }
    if {!$clean} { error "RTL design checks failed" }
    # check_design does not prove functional intent. Inspect elaboration logs for
    # inferred latches/multiple drivers and retain simulation/test evidence too.
    snps_result [dict create rtl_elaborated 1 rtl_checked $clean] {} \
        {reports/design.rpt reports/hierarchy.rpt}
}
