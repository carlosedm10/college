module FSM(CLK,RST_n, Enable1, Enable2, ADC_CS, ADC_PENIRQ_n, Ena_Trans,Fin_Trans)

input CLK,RST_n, Enable1, Enable2;
output ADC_CS, ADC_PENIRQ_n, Ena_Trans,Fin_Trans;


  
  localparam ESTADO_0 =  2'b00;
  localparam ESTADO_1 =  2'b01;
  localparam ESTADO_2 =  2'b10;
  localparam ESTADO_3 =  2'b11;
  

  reg [3:0] estado_actual, estado_siguiente; // Declaración de los registros que guardan el estado actual y el estado siguiente
  
  //State memory
  always @(posedge clock, negedge reset) begin
    if (~reset) begin
      estado_actual <= ESTADO_0;
      cuenta <= ESTADO_0;
    end else begin
      estado_actual <= estado_siguiente;
      cuenta <= estado_actual;
    end
  end
  
  //Next state logic
  always @(estado_actual or enable) begin
    case(estado_actual)
      ESTADO_0: if(enable) estado_siguiente = ESTADO_1; else estado_siguiente = estado_actual;
      ESTADO_1: if(enable) estado_siguiente = ESTADO_2; else estado_siguiente = estado_actual;
      ESTADO_2: if(enable) estado_siguiente = ESTADO_3; else estado_siguiente = estado_actual;
      ESTADO_3: if(enable) estado_siguiente = ESTADO_4; else estado_siguiente = estado_actual;
      ESTADO_4: if(enable) estado_siguiente = ESTADO_5; else estado_siguiente = estado_actual;
		default:   estado_siguiente = ESTADO_0;
	endcase
end
	
	//Output logic
	always @(estado_actual) begin
		case(estado_actual)
		ESTADO_0: begin Ena_Trans<=0; Fin_Trans <=0; ADC_CS<=0 end;
		ESTADO_1: begin Ena_Trans<=0; Fin_Trans <=0; ADC_CS<=0 end;
        ESTADO_2: begin Ena_Trans<=1; Fin_Trans <=0; ADC_CS<=1 end;
        ESTADO_3: begin Ena_Trans<=0; Fin_Trans <=1; ADC_CS<=0 end;
		default:  begin Ena_Trans<=0; Fin_Trans <=0; ADC_CS<=0 end;
	endcase
end

endmodule
