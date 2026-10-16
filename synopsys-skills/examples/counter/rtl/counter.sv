module counter(input logic clk, input logic reset_n, output logic [7:0] count);
  always_ff @(posedge clk or negedge reset_n)
    if (!reset_n) count <= 8'h00;
    else count <= count + 8'h01;
endmodule
