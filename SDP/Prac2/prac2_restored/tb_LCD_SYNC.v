`timescale 1ns/100ps

module tb_LCD_SYNC();


localparam T = 20;

reg CLK, RST_n;
wire HD,VD,GREST,NCLK;
wire DEN;
wire [10:0] columna;
wire [9:0] fila;

	
LCD_SYNC t1(CLK,RST_n, NCLK, GREST,HD,VD,DEN,columna,fila);	
	
always 
begin
	#(T/2) CLK = ~CLK;
end

initial
begin

CLK = 0;
RST_n = 0;
#(T*2)
RST_n = 1;

end

always@(*)begin

if(fila==456)

$stop;

end


endmodule
