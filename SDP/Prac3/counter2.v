module counter2 (clock,reset,enable,up_down,fin_cuenta);

parameter MODULE = 5000000; //para que la frecuencia sea de 10Hz
parameter n =$clog2(MODULE);

input clock, reset, enable,up_down;
output fin_cuenta;
reg [n-1:0] cnt;

always @(posedge clock, negedge reset) begin

	if(~reset)
		cnt <= 0;
		
	else if(enable) begin
	
		if(up_down) 
		
			if(cnt == MODULE - 1'b1)
			
				cnt <= 0;
				
			else 
				cnt <= cnt + 1'b1;
			
		
				
		else 
		
			if(cnt == 0)
			
				cnt <= MODULE -1'b1;
				
			else 
				cnt <= cnt - 1'b1;
			
		end
			
	end
			


assign fin_cuenta = (up_down == 1'b1)? ((cnt == MODULE -1)? enable:1'b0):((cnt == 1'b0)? enable:1'b0);
endmodule
