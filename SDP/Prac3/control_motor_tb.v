// --------------------------------------------------------------------
// Universitat Politècnica de València
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// --------------------------------------------------------------------
// Sistemas Digitales Programables
// Curso 2022-23
// --------------------------------------------------------------------
// Nombre del archivo: control_motor_tb.v
//
// Descripción: testbench del codigo que controla el motor
//
// --------------------------------------------------------------------
// Versión: v1.0 | Fecha Modificación: 30/04/2023
//
// Autores: Carlos E Dominguez Martinez, y  Oscar Jimenez Bou
//
// --------------------------------------------------------------------
`timescale 1ns/100ps
module control_motor_tb;
reg CLK, RESET, ENABLE, HALF_FULL, UP_DOWN;
wire A, B, C, D, INH1, INH2;
always #1 CLK = ~CLK; //Definimos el reloj

control_motor cm(CLK, RESET, ENABLE, HALF_FULL, UP_DOWN, A, B, C ,D, INH1, INH2);

initial begin //Inicializacion de las variables
    CLK = 0;
    RESET = 1;
    ENABLE = 0;
    HALF_FULL = 0;
    UP_DOWN = 0;
end

initial begin
    #10;
	// Medio paso 1
    ENABLE = 1;
    HALF_FULL = 1;
    UP_DOWN = 1;
    #100;
	// Medio paso 2
    UP_DOWN = 0;
    #100;
   // Wave 1
    HALF_FULL = 0;
	 UP_DOWN = 1;
    #100;
    // Wave 2
	 UP_DOWN = 0;
    #100;
	// Reset	 
	 RESET = 0;
	 #9 //Tiempo impar para entrar en modo normal
	// Normal 1
    RESET = 1;
	 HALF_FULL = 0;
	 UP_DOWN = 1;
    #100;
    // Normal 2
	 UP_DOWN = 0;
    #100;
    $finish;
end
endmodule
