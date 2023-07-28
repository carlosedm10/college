`timescale 1ns / 100ps

module tb_contador_variable();
reg clock, reset,enable,modo;
reg [3:0] entrada;
wire fin_cuenta;
wire [3:0] cuenta;

// Instanciar el contador
contador_variable #(4) contador_inst (
    .clock(clock),
    .reset(reset),
    .enable(enable),
    .modo(modo),
    .entrada(entrada),
    .fin_cuenta(fin_cuenta),
    .cuenta(cuenta)
);
// Generador de reloj
always #5 clock = ~clock;

// Estímulo
initial begin
    // Inicializar señales
    clock = 0;
    reset = 0;
    enable = 0;
    modo = 0;
    entrada = 4'b0000;

    // Reset
   #5 reset = 1;

    // Prueba 1: Contar con modo = 0 (cuenta hasta el módulo máximo)
     enable = 1;
    modo = 0;

    // Prueba 2: Contar con modo = 1 (cuenta hasta el valor de entrada)
    #100 entrada = 4'b0110; // Cuenta hasta 6
    
    #10 modo = 1;

    // Terminar simulación
    #1000 $finish;
end
endmodule
