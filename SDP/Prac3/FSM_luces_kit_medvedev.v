module FSM_luces_kit_medvedev(clock, reset, enable, LEDG);
  input clock, reset, enable;
  reg [3:0] cuenta;
  output reg [7:0] LEDG;
  
  
  localparam ESTADO_0 =  4'b0000;
  localparam ESTADO_1 =  4'b0001;
  localparam ESTADO_2 =  4'b0010;
  localparam ESTADO_3 =  4'b0011;
  localparam ESTADO_4 =  4'b0100;
  localparam ESTADO_5 =  4'b0101;
  localparam ESTADO_6 =  4'b0110;
  localparam ESTADO_7 =  4'b0111;
  localparam ESTADO_8 =  4'b1000;
  localparam ESTADO_9 =  4'b1001;
  localparam ESTADO_10 = 4'b1010;
  localparam ESTADO_11 = 4'b1011;
  localparam ESTADO_12 = 4'b1100;
  localparam ESTADO_13 = 4'b1101;

  reg [3:0] estado_actual, estado_siguiente; // Declaración de los registros que guardan el estado actual y el estado siguiente
  
  //State memory
  always @(posedge clock, negedge reset) begin
    if (~reset) begin
      estado_actual <= ESTADO_0;
      cuenta <= ESTADO_0;
    end else begin
      estado_actual <= estado_siguiente;
      cuenta <= estado_actual;
    end
  end
  
  //Next state logic
  always @(estado_actual or enable) begin
    case(estado_actual)
    ESTADO_0: if(enable) estado_siguiente = ESTADO_1; else estado_siguiente = estado_actual;
    ESTADO_1: if(enable) estado_siguiente = ESTADO_2; else estado_siguiente = estado_actual;
    ESTADO_2: if(enable) estado_siguiente = ESTADO_3; else estado_siguiente = estado_actual;
    ESTADO_3: if(enable) estado_siguiente = ESTADO_4; else estado_siguiente = estado_actual;
    ESTADO_4: if(enable) estado_siguiente = ESTADO_5; else estado_siguiente = estado_actual;
    ESTADO_5: if(enable) estado_siguiente = ESTADO_6; else estado_siguiente = estado_actual;
    ESTADO_6: if(enable) estado_siguiente = ESTADO_7; else estado_siguiente = estado_actual;
    ESTADO_7: if(enable) estado_siguiente = ESTADO_8; else estado_siguiente = estado_actual;
    ESTADO_8: if(enable) estado_siguiente = ESTADO_9; else estado_siguiente = estado_actual;
    ESTADO_9: if(enable) estado_siguiente = ESTADO_10; else estado_siguiente = estado_actual;
		ESTADO_10: if(enable) estado_siguiente = ESTADO_11; else estado_siguiente = estado_actual;
		ESTADO_11: if(enable) estado_siguiente = ESTADO_12; else estado_siguiente = estado_actual;
		ESTADO_12: if(enable) estado_siguiente = ESTADO_13; else estado_siguiente = estado_actual;
		ESTADO_13: if(enable) estado_siguiente = ESTADO_0; else estado_siguiente = estado_actual;
		default:   estado_siguiente = ESTADO_0;
	endcase
end
	
	//Output logic
	always @(estado_actual) begin
		case(estado_actual)
		ESTADO_0:  LEDG = 8'b10000000;
		ESTADO_1:  LEDG = 8'b01000000;
      ESTADO_2:  LEDG = 8'b00100000;
      ESTADO_3:  LEDG = 8'b00010000;
      ESTADO_4:  LEDG = 8'b00001000;
      ESTADO_5:  LEDG = 8'b00000100;
      ESTADO_6:  LEDG = 8'b00000010;
      ESTADO_7:  LEDG = 8'b00000001;
      ESTADO_8:  LEDG = 8'b00000010;
      ESTADO_9:  LEDG = 8'b00000100;
		ESTADO_10: LEDG = 8'b00001000;
		ESTADO_11: LEDG = 8'b00010000;
		ESTADO_12: LEDG = 8'b00100000;
		ESTADO_13: LEDG = 8'b01000000;
		default:   LEDG = 8'b00000000;
	endcase
end
endmodule

