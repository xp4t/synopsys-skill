source $::env(SNPS_FRAMEWORK_ROOT)/templates/common.tcl
snps_main {
    # Fusion uses NDM technology and logical/physical references, not DC's
    # target_library contract. PDK recipe must create/link design and scenarios.
    source [snps_required fusion_init_recipe]
    compile_fusion -check_only
    compile_fusion
    redirect reports/qor.rpt { report_qor }
    redirect reports/timing.rpt { report_timing }
    save_block -as ${top}/compiled
    save_lib
    # Retrieve compile_fusion manual to select valid -from/-to boundaries.
    # Verify this transformed implementation against original RTL before promotion.
}
