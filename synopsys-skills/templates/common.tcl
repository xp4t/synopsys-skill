# Shared Tcl helpers. This file uses Tcl 8.6 syntax, not a vendor JSON extension.
proc snps_required {name} {
    upvar #0 $name value
    if {![info exists value] || $value eq ""} { error "Missing configuration variable: $name" }
    return $value
}
proc snps_parameter {name default_value} {
    if {[info exists ::env(SNPS_PARAM_$name)]} { return $::env(SNPS_PARAM_$name) }
    return $default_value
}
proc snps_quote {s} {
    return "\"[string map [list \\ \\\\ \" \\\" \n \\n \r \\r \t \\t] $s]\""
}
proc snps_result {checks metrics reports} {
    set c {}; set m {}; set r {}
    dict for {key value} $checks {
        if {$value ni {0 1}} { error "Check must be Boolean: $key" }
        lappend c "[snps_quote $key]:[expr {$value ? {true} : {false}}]"
    }
    dict for {key value} $metrics {
        if {![string is double -strict $value]} { error "Metric must be numeric: $key" }
        lappend m "[snps_quote $key]:$value"
    }
    foreach report $reports { lappend r [snps_quote $report] }
    set f [open result.json {WRONLY CREAT EXCL}]
    puts $f "\{\"schema_version\":1,\"status\":\"pass\",\"checks\":\{[join $c ,]\},\"metrics\":\{[join $m ,]\},\"reports\":\[[join $r ,]\]\}"
    close $f
}
proc snps_main {body} {
    if {[catch {
        if {[info exists ::env(SNPS_CONFIG_TCL)]} {
            uplevel #0 [list source $::env(SNPS_CONFIG_TCL)]
        }
        file mkdir reports outputs
        uplevel #0 $body
    } message options]} {
        puts stderr "SNPS_STAGE_ERROR: $message"
        if {[dict exists $options -errorinfo]} { puts stderr [dict get $options -errorinfo] }
        exit 1
    }
    exit 0
}
