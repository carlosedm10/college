module Divisor_tb;
  reg CLK, RST, start;
  reg [7:0] Num, Den;
  wire done, er;
  wire [7:0] Coc, Res;

  // Instancia del módulo a probar
  Divisor DUT (
    .CLK(CLK),
    .RST(RST),
    .start(start),
    .Num(Num),
    .Den(Den),
    .done(done),
    .er(er),
    .Coc(Coc),
    .Res(Res)
  );

  // Generación de pulsos de reloj
  always begin
    CLK = 0;
    #5;
    CLK = 1;
    #5;
  end

  // Inicialización de entradas
  initial begin
    RST = 0;
    start = 0;
    Num = 0;
    Den = 0;
    #10;

    // Prueba de división válida
    RST = 1;
    Num = 100;
    Den = 20;
    start = 1;
    #20;
    start = 0;
    #100;
    RST = 0;

    // Prueba de división por cero
    RST = 1;
    Num = 50;
    Den = 0;
    start = 1;
    #20;
    start = 0;
    #100;
    RST = 0;

    // Prueba de división con resultado en cero
    RST = 1;
    Num = 0;
    Den = 10;
    start = 1;
    #20;
    start = 0;
    #100;
    RST = 0;

    // Prueba de división con resultado sin cero
    RST = 1;
    Num = 30;
    Den = 5;
    start = 1;
    #20;
    start = 0;
    #100;
    RST = 0;

    // Otras pruebas...
    // ...
    $finish;
  end
endmodule
