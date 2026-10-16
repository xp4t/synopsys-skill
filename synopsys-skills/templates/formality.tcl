source $::env(SNPS_FRAMEWORK_ROOT)/templates/common.tcl
snps_main {
    foreach name {top rtl rtl_format target_dbs implementation_netlist synthesis_svf} { snps_required $name }
    set synopsys_auto_setup true
    set_svf $synthesis_svf
    # Unqualified read_db loads shared technology libraries into current and
    # subsequently opened containers (installed read_db manual, DESCRIPTION).
    if {![read_db $target_dbs]} { error "Shared technology library load failed" }
    switch -- $rtl_format {
        verilog { read_verilog -r $rtl }
        sverilog { read_sverilog -r $rtl }
        vhdl { read_vhdl -r $rtl }
        default { error "Unsupported RTL format: $rtl_format" }
    }
    if {![set_top r:/WORK/$top]} { error "Reference link failed" }
    read_verilog -i $implementation_netlist
    if {![set_top i:/WORK/$top]} { error "Implementation link failed" }
    match
    set equivalent [verify]
    redirect reports/unmatched.rpt { report_unmatched_points }
    redirect reports/failing.rpt { report_failing_points }
    redirect reports/aborted.rpt { report_aborted_points }
    redirect reports/black_boxes.rpt { report_black_boxes }
    redirect reports/dont_verify.rpt { report_dont_verify_points }
    redirect reports/constants.rpt { report_constants }
    # Strict default coverage policy. Methodologies with intentional abstractions
    # need a separately reviewed adapter with explicit proof scope, not exclusions
    # added merely to make verification pass.
    foreach {report pattern} {
        reports/failing.rpt {No failing compare points\.}
        reports/unmatched.rpt {No unmatched points\.}
        reports/aborted.rpt {No aborted compare points\.}
        reports/dont_verify.rpt {Don't verify points:\s+None}
        reports/constants.rpt {User Defined Constants:\s+None}
    } {
        set f [open $report r]; set contents [read $f]; close $f
        if {![regexp $pattern $contents]} { error "Proof coverage needs diagnosis/review: $report" }
    }
    set f [open reports/black_boxes.rpt r]; set contents [read $f]; close $f
    set boxes [regexp -all -inline {Instances\s*:\s*([0-9]+)} $contents]
    if {![llength $boxes] && ![regexp -nocase {no black.box} $contents]} {
        error "Unrecognized black-box coverage report; inspect before promotion"
    }
    foreach {match count} $boxes {
        if {$count != 0} { error "Instantiated black boxes require explicit proof-scope review" }
    }
    save_session outputs/equivalence
    set f [open reports/equivalence.rpt w]
    puts $f "equivalence=$equivalent reference=$top implementation=$implementation_netlist"
    close $f
    if {!$equivalent} { error "Formal equivalence failed; promotion blocked" }
    snps_result [dict create equivalence $equivalent proof_coverage_clean 1] {} \
        {reports/equivalence.rpt reports/unmatched.rpt reports/failing.rpt reports/aborted.rpt reports/black_boxes.rpt reports/dont_verify.rpt reports/constants.rpt}
}
