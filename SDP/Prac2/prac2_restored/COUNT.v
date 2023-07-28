module COUNT(CLK, RST_n,EN, cuenta,TC);

parameter modulo = 1056;
parameter n = $clog2(modulo-1);

input CLK, RST_n,EN;
output TC;
output reg [n-1:0] cuenta;

always @(posedge CLK, negedge RST_n) begin

	if(~RST_n)
		cuenta <= 0;
	else if(EN)
		if(cuenta == modulo -1)
		
			cuenta <= 0;
		else 
			cuenta <= cuenta + 1;
end
assign TC = ((cuenta == modulo - 1) && (EN==1)) ? 1:0;

endmodule
