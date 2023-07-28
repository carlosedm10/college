module SELEC_COLOR (sel,R,G,B);

input sel;
output reg [7:0] R,G,B;

always @(*) 
begin
	if(~sel)
	begin
		R = 8'd255;
		G = 8'd255;
		B = 8'd255;
	end
	else 
	begin
		R = 8'd0;
		G = 8'd0;
		B = 8'd0;
   end
end
endmodule
