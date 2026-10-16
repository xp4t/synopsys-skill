module tb;
  logic clk=0, reset_n=0;
  logic [7:0] count;
  counter dut(.*);
  always #5 clk=~clk;
  initial begin
    repeat (2) @(negedge clk);
    if (count !== 0) $fatal(1,"reset failed");
    reset_n=1;
    for (int i=1; i<=20; i++) begin
      @(negedge clk);
      if (count !== i[7:0]) $fatal(1,"count failed expected %0d actual %0d",i,count);
    end
    $display("COUNTER_TEST_PASS");
    $finish;
  end
  initial begin #1000; $fatal(1,"timeout"); end
endmodule
