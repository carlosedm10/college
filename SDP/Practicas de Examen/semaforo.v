module semaforo(CLK, RST, EN, T, B, A, R, V);

input CLK, RST, EN, T;
output reg B, A, R, V;

parameter MODULE = 10;

reg [MODULE-1:0] cnt;
reg [1:0] state, nexstate;
//Codificacion estados
localparam S0 = 2'b00, S1 = 2'b01, S2 = 2'b10, S3 = 2'b11;


// Contador:
always @(posedge CLK,  negedge RST)
	if (!RST)
		cnt <= 0; 
	else if (cnt <= MODULE - 1)
		cnt <= cnt + 1;
	else cnt <= 0;

//State memory
always @(posedge CLK,  negedge RST)
	if (!RST)
		state <= S0;
	else
		state <= nexstate;

//State logic
always @(*)	
begin
	case(state)
	S0: nexstate = (T==1)? S1 :S0 ;
	S1: nexstate = S2;
	S2: nexstate =(cnt == MODULE-1)?  S3: S2;
	S3: nexstate = S0;
	default: nexstate = S0;
	endcase
end

//Output logic
always @(*)
begin
	case(state)
	S0: begin B = 1; A = 0; R = 0; V = 1; end
	S1: begin B = 0; A = 1; R = 0; V = 0; end
	S2: begin B = 0; A = 0; R = 1; V = 0; end
	S3: begin B = 0; A = 1; R = 0; V = 0; end
	default: begin B = 0; A = 0; R = 0; V = 0; end
	endcase
end

endmodule
