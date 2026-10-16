source $::env(SNPS_FRAMEWORK_ROOT)/templates/common.tcl
snps_main {
    foreach name {top tech_file ndm_libraries implementation_netlist sdc core_utilization core_offset} { snps_required $name }
    create_lib outputs/design.ndm -technology $tech_file -ref_libs $ndm_libraries
    read_verilog -top $top $implementation_netlist
    if {![link_block]} { error "Physical library link failed" }
    read_sdc $sdc
    initialize_floorplan -core_utilization [snps_parameter core_utilization $core_utilization] -core_offset $core_offset
    # Supply reviewed macro/IO/MCMM/RC initialization as a PDK-specific Tcl recipe.
    source [snps_required floorplan_recipe]
    redirect reports/design.rpt { check_design }
    redirect reports/qor.rpt { report_qor }
    save_block -as ${top}/floorplan
    save_lib
    # An agent must inspect reports and produce result.json; command completion
    # does not prove a legal floorplan, connected supplies or correct corners.
}
