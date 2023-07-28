module BARRAS_LCD(CLK,RST_n,NCLK,GREST,HD,VD,DEN,R,G,B);

input CLK, RST_n;
output NCLK,GREST, HD, VD,DEN;
output reg [7:0] R,G,B;

wire [10:0]col;

LCD_SYNC lcd1(CLK,RST_n, NCLK, GREST,HD,VD,DEN,col,);

/*
800/8colores = 100 pixeles

area visualizacion = 800x480

colocacion pantalla =>
 desde [216,35].......[1015,35]
-----------------------------------PANTALLA---------------------
 hasta [216,514]......[1015,514]
*/

always@(col )begin

if( col < 315) begin //blanco
R <= 8'd255;
G <= 8'd255;
B <= 8'd255;
end

else if( col < 415)begin //amarillo
R <= 8'd255;
G <= 8'd255;
B <= 8'd0;
end

else if( col < 515)begin //azul claro
R <= 8'd0;
G <= 8'd255;
B <= 8'd255;
end


else if( col < 615)begin //verde
R <= 8'd0;
G <= 8'd255;
B <= 8'd0;
end

else if( col < 715)begin //rosa
R <= 8'd255;
G <= 8'd0;
B <= 8'd255;
end


else if( col < 815)begin //rojo
R <= 8'd255;
G <= 8'd0;
B <= 8'd0;
end


else if( col < 915)begin //azul
R <= 8'd0;
G <= 8'd0;
B <= 8'd255;
end


else begin //negro
R <= 8'd0;
G <= 8'd0;
B <= 8'd0;
end

end




endmodule
