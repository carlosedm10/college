module contador_variable(clock, reset,enable, modo, entrada, fin_cuenta, cuenta);

parameter width_counter = 4;

input clock, reset,enable, modo;
input [width_counter-1:0] entrada;
output fin_cuenta;
output reg[width_counter-1:0] cuenta;

localparam [width_counter-1:0] modulo_good = 2**width_counter-1'b1;

wire [width_counter-1:0] cuenta_fin;

always@(posedge clock, negedge reset) begin
	if(~reset)
		cuenta <= 0;
	else if(enable)
		if(cuenta == cuenta_fin)
			cuenta <= 0;
		else cuenta <= (cuenta + 1'b1);
end

assign cuenta_fin = (modo == 1'b1)? entrada : modulo_good;
assign fin_cuenta = ((cuenta == cuenta_fin) && (enable == 1'b1))? 1'b1:1'b0;

endmodule
