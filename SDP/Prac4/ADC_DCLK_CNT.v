module ADC_DCLK_CNT(CLK, RST_n,Enable,TC);

parameter modulo = 80;
parameter n = $clog2(modulo-1);

input CLK, RST_n,Enable;
output TC;
 reg [n-1:0] cuenta;

always @(posedge CLK, negedge RST_n) begin

	if(~RST_n)
		cuenta <= 0;
	else if(Enable)
		if(cuenta == modulo -1)
		
			cuenta <= 0;
		else 
			cuenta <= cuenta + 1;
end
assign TC = ((cuenta == modulo - 1) && (Enable==1)) ? 1:0;

endmodule
