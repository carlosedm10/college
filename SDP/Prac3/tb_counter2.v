`timescale 1ns/100ps

module tb_counter2();

reg clock;
reg reset;
reg enable;
reg up_down;
wire fin_cuenta;

// Instanciar el contador
counter2 dut(clock,reset,enable,up_down,fin_cuenta);
defparam dut.MODULE = 10;

// Generador de reloj
always #5 clock = ~clock;

// Estímulo
initial begin
    // Inicializar señales
    clock = 0;
    reset = 0;
    enable = 0;
    up_down = 0;

    // Reset
    #10 reset = 1;

    // Prueba 1: Contar hacia arriba
    enable = 1;
    up_down = 1;

    // Prueba 2: Contar hacia abajo
    #50 up_down = 0;

    // Terminar simulación
    #50 $finish;
end

endmodule


