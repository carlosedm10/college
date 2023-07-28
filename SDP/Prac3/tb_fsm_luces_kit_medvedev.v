`timescale 1ns/100ps
module tb_fsm_luces_kit_medvedev;
  
reg clk, reset; // Inputs
wire [7:0] LEDG; // Outputs
  
FSM_luces_kit_medvedev dut(clk, reset, LEDG);  // Instanciamos el modulo
    
always #5 clk = ~clk; // Generamos el reloj
  
  // Inicializamos las variables
  initial begin
    clk = 0;
    reset = 0;
    #10 reset = 1;
  end
  
  // Creamos un limite de 100 tiempos de reloj
  integer i;4
  initial begin
    for (i = 0; i < 100; i = i + 1) begin
      #5;
    end
    $finish;
  end
  
endmodule
