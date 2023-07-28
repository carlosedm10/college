module FRASE_LCD (CLK,RST_n,NCLK,GREST,HD,VD,DEN,R,G,B);

input CLK, RST_n;
output NCLK,GREST, HD, VD,DEN;
output [7:0] R,G,B;


wire [9:0] fil; 
wire [10:0] col;
wire [6:0] car;
wire [10:0] dir1;
reg [5:0] dir2;	
wire [12:0] address;		
wire q;


reg [9:0] Y;
reg [10:0] X;


LCD_SYNC lcd3(CLK,RST_n, NCLK, GREST,HD,VD,DEN,col,fil);


always @(fil, col) // Direccionamiento
begin

	Y = (fil - 35);
	X = (col - 216);

end

assign dir1 = {Y[8:4], X[9:4]} ; 	

TEXTO  t1 ( .address ( dir1 ), .clock ( NCLK ), .q ( car ) );	//Memoria ROM 1920x7


//Registro
always @(posedge NCLK) begin

	dir2 <= {Y[3:1],X[3:1]};

end


assign address = {car,dir2};


ROM_char   ROM_char_inst1 ( .address ( address ), .clock ( NCLK ), .q ( q ) ); //memoria ROM 8192x1

SELEC_COLOR s2(q,R,G,B);


endmodule
