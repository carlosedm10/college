`timescale 1ns/100ps

module tb_contador_up_down();

reg clock;
reg reset;
reg enable;
reg up_down;
wire fin_cuenta;
wire [3:0] cuenta;

// Instanciar el contador
contador_up_down dut(clock,reset,enable,up_down,fin_cuenta,cuenta);

// Generador de reloj
always #5 clock = ~clock;

// Estímulo
initial begin
    // Inicializar señales
    clock = 0;
    reset = 0;
    enable = 0;
    up_down = 0;
    reset = 0;
	 

    // Prueba 1: Contar hacia arriba
	 #10 reset=1;
    enable = 1;
    up_down = 1;


    // Prueba 2: Contar hacia abajo
    #80 up_down = 0;

    // Terminar simulación
    #100 $finish;
end

endmodule
