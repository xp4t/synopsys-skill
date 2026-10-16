source $::env(SNPS_FRAMEWORK_ROOT)/templates/common.tcl
snps_main {
    # restore_block_recipe opens a writable copy in SNPS_RESTORE_DIR, not the
    # accepted checkpoint. It also configures the qualified PDK and MCMM setup.
    source [snps_required restore_block_recipe]
    switch -- $::env(SNPS_STAGE) {
        power {
            source [snps_required pg_recipe]
            redirect reports/pg_connectivity.rpt { check_pg_connectivity }
            redirect reports/pg_drc.rpt { check_pg_drc }
        }
        placement {
            place_opt
            redirect reports/legality.rpt { check_legality -verbose }
            redirect reports/congestion.rpt { report_congestion }
        }
        cts {
            source [snps_required cts_recipe]
            clock_opt
            redirect reports/clock_qor.rpt { report_clock_qor }
        }
        routing {
            route_auto
            route_opt
            redirect reports/routes.rpt { check_routes }
        }
        default { error "Unsupported implementation stage: $::env(SNPS_STAGE)" }
    }
    redirect reports/qor.rpt { report_qor }
    redirect reports/timing.rpt { report_timing }
    save_block -as ${top}/$::env(SNPS_STAGE)
    save_lib
    # Produce normalized result.json only after tool-specific report inspection.
}
