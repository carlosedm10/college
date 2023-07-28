module contador_up_down(clock,reset,enable,up_down,fin_cuenta,cuenta);

parameter MODULE =16; 
parameter n =$clog2(MODULE);

input clock, reset, enable, up_down;
output fin_cuenta;
output reg [n-1:0] cuenta;

always @(posedge clock, negedge reset) begin

	if(~reset)
		cuenta <= 0;
		
	else if(enable) begin
	
		if(up_down) 
		
			if(cuenta == MODULE - 1'b1)
			
				cuenta <= 0;
				
			else 
				cuenta <= cuenta + 1'b1;
			
		
				
		else 
		
			if(cuenta == 0)
			
				cuenta <= MODULE -1'b1;
				
			else 
				cuenta <= cuenta - 1'b1;
			
		end
			
	end

assign fin_cuenta = (up_down == 1'b1)? ((cuenta == MODULE - 1'b1)? enable:1'b0):((cuenta == 1'b0)? enable:1'b0);
endmodule
