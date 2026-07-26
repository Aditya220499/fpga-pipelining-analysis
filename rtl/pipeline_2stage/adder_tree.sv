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

    //=========================================================
    // Input Registers
    //=========================================================

    logic [7:0] a_reg, b_reg, c_reg, d_reg;
    logic [7:0] e_reg, f_reg, g_reg, h_reg;

    //=========================================================
    // Level-1 Combinational
    //=========================================================

    logic [8:0] sum_ab_comb;
    logic [8:0] sum_cd_comb;
    logic [8:0] sum_ef_comb;
    logic [8:0] sum_gh_comb;

    //=========================================================
    // Pipeline Registers
    //=========================================================

    logic [8:0] sum_ab_reg;
    logic [8:0] sum_cd_reg;
    logic [8:0] sum_ef_reg;
    logic [8:0] sum_gh_reg;

    //=========================================================
    // Level-2 + Level-3 Combinational
    //=========================================================

    logic [9:0]  sum_abcd;
    logic [9:0]  sum_efgh;
    logic [10:0] sum_comb;

    //---------------------------------------------------------
    // Combinational Logic
    //---------------------------------------------------------

    always_comb
    begin

        //-------------------------
        // Level-1
        //-------------------------

        sum_ab_comb = a_reg + b_reg;
        sum_cd_comb = c_reg + d_reg;
        sum_ef_comb = e_reg + f_reg;
        sum_gh_comb = g_reg + h_reg;

        //-------------------------
        // Level-2
        //-------------------------

        sum_abcd = sum_ab_reg + sum_cd_reg;
        sum_efgh = sum_ef_reg + sum_gh_reg;

        //-------------------------
        // Level-3
        //-------------------------

        sum_comb = sum_abcd + sum_efgh;

    end

    //---------------------------------------------------------
    // Sequential Logic
    //---------------------------------------------------------

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
        // Pipeline Registers
        //-------------------------

        sum_ab_reg <= sum_ab_comb;
        sum_cd_reg <= sum_cd_comb;
        sum_ef_reg <= sum_ef_comb;
        sum_gh_reg <= sum_gh_comb;

        //-------------------------
        // Output Register
        //-------------------------

        sum <= sum_comb;

    end

endmodule