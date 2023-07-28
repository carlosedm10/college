// --------------------------------------------------------------------
// Universitat Politècnica de València
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// --------------------------------------------------------------------
// Sistemas Digitales Programables
// Curso 2022-23
// --------------------------------------------------------------------
// Nombre del archivo: control_motor.v
//
// Descripción: 
//
// --------------------------------------------------------------------
// Versión: v1.0 | Fecha Modificación: 26/04/2023
//
// Autores: Carlos E Dominguez Martinez, y  Oscar Jimenez Bou
//
// --------------------------------------------------------------------

module control_motor(CLK, RESET, ENABLE, HALF_FULL, UP_DOWN, A, B, C ,D, INH1, INH2);

input CLK, RESET, ENABLE, HALF_FULL, UP_DOWN;
output reg  A, B, C ,D;
output INH1, INH2;

reg [2:0] state, next_state;
localparam S1=3'b000, S2=3'b001, S3=3'b010, S4=3'b011, S5=3'b100, S6=3'b101, S7=3'b110, S8=3'b111; 

always @(posedge CLK or negedge RESET)
begin
if(~RESET)
	state <= S1;
else if (ENABLE)
	state <= next_state;
end

always @(*) begin
case(state)
	S1: next_state = (HALF_FULL == 1) ? ((UP_DOWN == 1) ? S2 : S8) : ((UP_DOWN == 1) ? S3 : S7);
	S2: next_state = (HALF_FULL == 1) ? ((UP_DOWN == 1) ? S3 : S1) : ((UP_DOWN == 1) ? S4 : S8);
	S3: next_state = (HALF_FULL == 1) ? ((UP_DOWN == 1) ? S4 : S2) : ((UP_DOWN == 1) ? S5 : S1);
	S4: next_state = (HALF_FULL == 1) ? ((UP_DOWN == 1) ? S5 : S3) : ((UP_DOWN == 1) ? S6 : S2);
	S5: next_state = (HALF_FULL == 1) ? ((UP_DOWN == 1) ? S6 : S4) : ((UP_DOWN == 1) ? S7 : S3);
	S6: next_state = (HALF_FULL == 1) ? ((UP_DOWN == 1) ? S7 : S5) : ((UP_DOWN == 1) ? S8 : S4);
	S7: next_state = (HALF_FULL == 1) ? ((UP_DOWN == 1) ? S8 : S6) : ((UP_DOWN == 1) ? S1 : S5);
	S8: next_state = (HALF_FULL == 1) ? ((UP_DOWN == 1) ? S1 : S7) : ((UP_DOWN == 1) ? S2 : S6);
	default next_state = S1;
	endcase
end

always @(*) 
case(state)
	S1: begin A = 0 ; B = 1; C = 0; D = 1; end
	S2: begin A = 0 ; B = 0; C = 0; D = 1; end
	S3: begin A = 1 ; B = 0; C = 0; D = 1; end
	S4: begin A = 1 ; B = 0; C = 0; D = 0; end
	S5: begin A = 1 ; B = 0; C = 1; D = 0; end
	S6: begin A = 0 ; B = 0; C = 1; D = 0; end
	S7: begin A = 0 ; B = 1; C = 1; D = 0; end
	S8: begin A = 0 ; B = 1; C = 0; D = 0; end
	default begin A = 0 ; B = 1; C = 0; D = 1; end
endcase
 
assign INH1 = A + B;
assign INH2 = C + D;

//☺

endmodule
