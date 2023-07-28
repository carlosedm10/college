module FRASE_LCD1 (CLK,RST_n,NCLK,GREST,HD,VD,DEN,R,G,B);

input CLK, RST_n;
output NCLK,GREST, HD, VD,DEN;
output [7:0] R,G,B;


wire [9:0] fil; 
wire [10:0] col;
wire [6:0] car;
wire [10:0] dir1;
wire [5:0] dir2;	
wire [12:0] address;		
wire q;


reg [9:0] Y;
reg [10:0] X;
reg [2:0] vfil,vcol;


LCD_SYNC lcd3(CLK,RST_n, NCLK, GREST,HD,VD,DEN,col,fil);

//CHAR_ROM

always @(fil, col) // Direccionamiento
begin

	Y = (fil - 35);
	X = (col - 216);

end

assign dir1 = {Y[7:3], X[8:3]} ; 	

TEXTO  t1 ( .address ( dir1 ), .clock ( NCLK ), .q ( car ) );	//Memoria ROM 1920x7



always @(posedge NCLK) begin

	dir2 <= {vfil 


end


assign address = {car,};



ROM_char   ROM_char_inst1 ( .address ( address ), .clock ( NCLK ), .q ( q ) ); //memoria ROM 8192x1

SELEC_COLOR s2(q,R,G,B);



endmodule
