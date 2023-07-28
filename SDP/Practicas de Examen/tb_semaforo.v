//Define un timescale
`timescale 1ns/100ps

module semaforo_tb();
    
    // Inputs
    reg CLK;
    reg RST;
    reg EN;
    reg T;
    
    // Outputs
    wire B;
    wire A;
    wire R;
    wire V;
    
    // Instantiate the module under test
    semaforo uut (
        .CLK(CLK),
        .RST(RST),
        .EN(EN),
        .T(T),
        .B(B),
        .A(A),
        .R(R),
        .V(V)
    );
    
    // Clock generation
    always begin
        #5 CLK = ~CLK;
    end
    
    // Initialize inputs
    initial begin
        CLK = 0;
        RST = 1;
        EN = 0;
        T = 0;
        
        // Reset
        #10 RST = 0;
        #10 RST = 1;
        
        // Test case 1
        #10 EN = 1;
        #10 T = 1;
        #10 T = 0;
        #10 T = 1;
        #10 T = 0;
        
        // Test case 2
        #10 T = 1;
        #10 T = 0;
        
        // Test case 3
        #10 EN = 0;
        #10 T = 1;
        #10 T = 0;
        #10 EN = 1;
        
        // Test case 4
        #10 T = 1;
        #10 T = 0;
        #10 T = 1;
        #10 T = 0;
        
        // Test case 5
        #10 EN = 0;
        #10 T = 1;
        #10 T = 0;
        #10 EN = 1;
        
        // End simulation
        #10 $finish;
    end
    
endmodule
