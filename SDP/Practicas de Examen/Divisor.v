module Divisor (CLK, RST, start, Num, Den, done, er, Coc, Res);

  input start, CLK, RST;
  input [7:0] Num, Den;
  output reg done, er;
  output reg [7:0] Coc, Res;

  reg [7:0] state, nexstate, i, N, D;

  localparam S0 = 0, S1 = 1, D2 = 2 ,S3 = 3;

//State memory
always @(posedge CLK,  negedge RST)
begin
  if (!RST)
  begin
    state <= S0;
    i = 0;
    D = Den;
    N = Num;
  end
  else if(Num > Den)
  begin
    state <= nexstate;
    N <= N - D;
    i = i + 1;
  end
end

      //State logic
always @(*)	
begin
	case(state)
	S0: nexstate = (Den == 0)? S0 :S1 ;
	default: nexstate = S0;
	endcase
end

//Output logic
always @(*)
begin
	case(state)
	S0: begin done = 0; er = 1; Coc = 0; Res = 0; end
	S1: begin done = 1; er = 0; Coc = i; Res = N; end
	default: 
      begin done = 0; er = 0; Coc = 0; Res = 0; end
	endcase
end


endmodule
