`timescale 1ns / 1ps

module adder_tree_tb;

logic clk;

logic [7:0] a;
logic [7:0] b;
logic [7:0] c;
logic [7:0] d;
logic [7:0] e;
logic [7:0] f;
logic [7:0] g;
logic [7:0] h;

logic [10:0] sum;

adder_tree dut
(
    .clk(clk),
    .a(a),
    .b(b),
    .c(c),
    .d(d),
    .e(e),
    .f(f),
    .g(g),
    .h(h),
    .sum(sum)
);

//////////////////////////////////////////////////////////
// Clock Generation
//////////////////////////////////////////////////////////

initial
    clk = 0;

always #5 clk = ~clk;

//////////////////////////////////////////////////////////
// Test Stimulus
//////////////////////////////////////////////////////////

initial
begin

    a = 0;
    b = 0;
    c = 0;
    d = 0;
    e = 0;
    f = 0;
    g = 0;
    h = 0;

    @(posedge clk);

    a = 10;
    b = 20;
    c = 30;
    d = 40;
    e = 50;
    f = 60;
    g = 70;
    h = 80;

    @(posedge clk);

    a = 100;
    b = 50;
    c = 25;
    d = 10;
    e = 5;
    f = 15;
    g = 20;
    h = 30;

    @(posedge clk);

    a = 255;
    b = 255;
    c = 255;
    d = 255;
    e = 255;
    f = 255;
    g = 255;
    h = 255;

    repeat(3)
        @(posedge clk);

    $finish;

end

endmodule