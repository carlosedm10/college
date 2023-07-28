module IMAGEN_LCD(CLK,RST_n,NCLK,GREST,HD,VD,DEN,R,G,B);

input CLK, RST_n;
output NCLK,GREST, HD, VD,DEN;
output [7:0] R,G,B;

wire [9:0] fil;
wire [10:0] col;

wire [20:0] address;
wire [15:0] data; //Data

reg [9:0] Y;
reg [10:0] X;


LCD_SYNC lcd2(CLK,RST_n, NCLK, GREST,HD,VD,DEN,col,fil);

always @(fil, col) // Direccionamiento
begin

	Y = (fil - 35);
	X = (col - 216);

end

assign address = Y[9:1]*512 + X[10:1]; 		

ROM_image ROM_image_inst ( .address(address) , .clock ( NCLK ) , .q ( data ) ); //ROM

assign R = {data[15:11],3'd000};
assign G = {data[10:5],2'd00};
assign B = {data[4:0],3'd000};			

//♥

endmodule
