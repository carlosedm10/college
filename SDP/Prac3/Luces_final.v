// --------------------------------------------------------------------
// Universitat Politècnica de València
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// --------------------------------------------------------------------
// Sistemas Digitales Programables
// Curso 2022-23
// --------------------------------------------------------------------
// Nombre del archivo: Luces_final.v
//
// Descripción: 
//
// --------------------------------------------------------------------
// Versión: v1.0 | Fecha Modificación: 17/05/2023
//
// Autores: Carlos E Dominguez Martinez, y  Oscar Jimenez Bou
//
// --------------------------------------------------------------------
module Luces_final(SW,CLOCK_50,KEY,LEDG,LEDR);

input CLOCK_50;
input [1:0] SW;
input [2:0] KEY;

output [7:0] LEDG,LEDR;

wire fin_cuenta, enable, up_down,cuenta, fin_cuenta_2;

counter2 c2(CLOCK_50,KEY[0],SW[0],SW[0],fin_cuenta);

contador_up_down cup(CLOCK_50,KEY[0],enable,up_down, ,LEDR[3:0]);

contador_variable cv(CLOCK_50, KEY[0],fin_cuenta, SW[1], LEDR[3:0], fin_cuenta_2, LEDR[7:4]);

FSM_luces_kit_medvedev md(CLOCK_50, KEY[0], fin_cuenta_2, LEDG);

FSM_speed_mealey sm(CLOCK_50, KEY[0], KEY[2:1], enable, up_down);


endmodule
