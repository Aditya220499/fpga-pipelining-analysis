`timescale 1ns / 1ps

module adder_tree
(
    input  logic        clk,

    input  logic [7:0]  a,
    input  logic [7:0]  b,
    input  logic [7:0]  c,
    input  logic [7:0]  d,
    input  logic [7:0]  e,
    input  logic [7:0]  f,
    input  logic [7:0]  g,
    input  logic [7:0]  h,

    output logic [10:0] sum
);

    //============================================================
    // Stage-0 : Input Registers
    //============================================================

    logic [7:0] a_reg;
    logic [7:0] b_reg;
    logic [7:0] c_reg;
    logic [7:0] d_reg;
    logic [7:0] e_reg;
    logic [7:0] f_reg;
    logic [7:0] g_reg;
    logic [7:0] h_reg;

    //============================================================
    // Combinational Datapath
    //============================================================

    //-----------------------------
    // Level-1
    //-----------------------------

    logic [8:0] sum_ab;
    logic [8:0] sum_cd;
    logic [8:0] sum_ef;
    logic [8:0] sum_gh;

    //-----------------------------
    // Level-2
    //-----------------------------

    logic [9:0] sum_abcd;
    logic [9:0] sum_efgh;

    //-----------------------------
    // Level-3
    //-----------------------------

    logic [10:0] sum_comb;

    always_comb
    begin

        //-------------------------
        // Level-1
        //-------------------------

        sum_ab = a_reg + b_reg;
        sum_cd = c_reg + d_reg;
        sum_ef = e_reg + f_reg;
        sum_gh = g_reg + h_reg;

        //-------------------------
        // Level-2
        //-------------------------

        sum_abcd = sum_ab + sum_cd;
        sum_efgh = sum_ef + sum_gh;

        //-------------------------
        // Level-3
        //-------------------------

        sum_comb = sum_abcd + sum_efgh;

    end

    //============================================================
    // Sequential Logic
    //============================================================

    always_ff @(posedge clk)
    begin

        //-------------------------
        // Input Registers
        //-------------------------

        a_reg <= a;
        b_reg <= b;
        c_reg <= c;
        d_reg <= d;
        e_reg <= e;
        f_reg <= f;
        g_reg <= g;
        h_reg <= h;

        //-------------------------
        // Output Register
        //-------------------------

        sum <= sum_comb;

    end

endmodule