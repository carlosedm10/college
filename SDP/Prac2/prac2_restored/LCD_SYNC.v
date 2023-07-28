module LCD_SYNC(CLK,RST_n, NCLK, GREST,HD,VD,DEN,columna,fila);

input CLK, RST_n;
output HD,VD,GREST,NCLK;
output reg DEN;
output [10:0] columna;
output [9:0] fila;

wire tc1, tc2;

pll_ltm pll_ltm_inst( .inclk0(CLK), .c0(NCLK)); //Modulo PPL 

COUNT HCOUNT(NCLK,RST_n,1, columna,tc1);
defparam HCOUNT.modulo = 1056;

COUNT VCOUNT(NCLK, RST_n,tc1, fila,tc2);
defparam VCOUNT.modulo = 525;

always @(columna or fila) begin

	if ((columna > 215 && columna < 1016) && (fila > 34 && fila < 515)) 
		DEN <= 1; 
	else 
		DEN <= 0;

end
assign HD = ~tc1;
assign VD = ~tc2;
assign GREST = RST_n;
 //♥

endmodule
