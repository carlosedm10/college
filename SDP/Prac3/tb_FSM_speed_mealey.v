`timescale 1ns / 100ps
module tb_FSM_speed_mealey();

reg clock;
reg reset;
wire enable;
wire up_down;
reg [1:0] key;

// Instanciar la máquina de estados
FSM_speed_mealey dut(clock, reset, key, enable, up_down);

// Generador de reloj
always #5 clock = ~clock;

// Estímulo
initial begin
    // Inicializar señales
    clock = 0;
    reset = 0;
    key = 2'b00;

    // Reset
    #5 reset = 1;

    // Prueba 1: key = 2'b10 (enable = 1, up_down = 1)
    #20 key = 2'b01;
    #30 key = 2'b00;

    // Prueba 2: key = 2'b01 (enable = 1, up_down = 0)
    #10 key = 2'b01;
    #40 key = 2'b00;

    // Prueba 3: key = 2'b11 (enable = 0, up_down = 0)
    #20 key = 2'b11;
    #30 key = 2'b00;

    // Terminar simulación
    #50 $finish;
end

endmodule
