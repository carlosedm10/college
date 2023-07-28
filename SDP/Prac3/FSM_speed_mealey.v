module FSM_speed_mealey(clock, reset, key, enable, up_down);

input clock, reset;
input [1:0] key; //1 -> Mas velocidad, 0 -> menos velocidad.

output reg up_down, enable;
reg estado_actual, estado_siguiente;

localparam s0 = 1'b0;
localparam s1 = 1'b1;

always@(posedge clock, negedge reset)
	begin
		if(!reset)	
			estado_actual <= s0;
		else
			estado_actual <= estado_siguiente;
	end

always @(estado_actual, key)
	begin
	
		if(estado_actual == s0)
		
			case (key)
			2'b10:	begin estado_siguiente = s1; enable = 1; up_down = 1; end
			2'b01: 	begin estado_siguiente = s1; enable = 1; up_down = 0; end
			default: begin estado_siguiente = s0; enable = 0; up_down = 0; end
			endcase
			
		else
		
			case (key)
			2'b11:	begin estado_siguiente = s0; enable = 0; up_down = 0; end
			default:	begin estado_siguiente = s1; enable = 0; up_down = 0; end
		endcase

	end 
	
endmodule 
