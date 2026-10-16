# Explicit teaching example specification: 100 MHz, one clock, no exceptions.
# Values here are sample requirements, never inferred requirements for user RTL.
create_clock -name core_clk -period 10 [get_ports clk]
set_clock_uncertainty 0.1 [get_clocks core_clk]
set_input_delay -clock core_clk -max 0.5 [get_ports reset_n]
set_input_delay -clock core_clk -min 0.1 [get_ports reset_n]
set_output_delay -clock core_clk -max 0.5 [get_ports count*]
set_output_delay -clock core_clk -min 0.1 [get_ports count*]
set_load 0.01 [get_ports count*]
