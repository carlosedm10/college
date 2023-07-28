`timescale 1ns/100ps

module tb_FRASE_LCD();
localparam T = 20;

reg CLK, RST_n;
wire NCLK, GREST, HD, VD, DEN;
wire [7:0] R, G, B;

FRASE_LCD f1(CLK,RST_n,NCLK,GREST,HD,VD,DEN,R,G,B);

always
begin
#(T/2) CLK = ~CLK;
end

integer fd;
event cierraFichero;

initial begin
	fd = $fopen ("tb_FRASE.txt", "w");
	@(cierraFichero);
disable guardaFichero;
	$display("Cierro Fichero");
	$fclose(fd);
end

initial begin
	CLK = 0;
	RST_n = 0;
	reset();
@(posedge VD)
-> cierraFichero;
	#10;
	$stop;
end

initial forever begin: guardaFichero
@(posedge NCLK)
	$fwrite(fd,"%0t ps: %b %b %b %b %b %b\n",$time,HD,VD,DEN,R,G,B);
end

task reset;
begin
	@(negedge CLK);
	RST_n = 0;
	repeat(2) @(negedge CLK);
	RST_n = 1;
	end
endtask

endmodule
