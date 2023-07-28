`timescale 1ns/100ps

module tb_COUNT();


localparam T = 20;

reg CLK, RST_n,EN;
wire TC;
wire [11-1:0] cuenta;

	COUNT c1(CLK,RST_n,EN,cuenta,TC);
	
always 
begin
	#(T/2) CLK = ~CLK;
end

initial
begin
	CLK = 0;
	RST_n = 0;
	EN = 1;
	#(T*10)
	RST_n =1;
	#(T*2000)
	$stop;
	end

endmodule
