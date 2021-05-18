function FISnew = changeFisGesture(param, FISold, Msht)
% Установка новых параметров (param) нечеткой системы FISold

FISnew = FISold;

% Демасштабирование настраиваемых параметров
param = param ./ Msht;

% Коэффициенты конццентрации термов входных переменных
FISnew.input(1).mf(1).params(1) = param(1);
FISnew.input(1).mf(2).params(1) = param(2);
FISnew.input(1).mf(3).params(1) = param(3);	
FISnew.input(2).mf(1).params(1) = param(4);	
FISnew.input(2).mf(2).params(1) = param(5);
FISnew.input(2).mf(3).params(1) = param(6);
FISnew.input(3).mf(1).params(1) = param(7);
FISnew.input(3).mf(2).params(1) = param(8);	
FISnew.input(3).mf(3).params(1) = param(9);	
FISnew.input(4).mf(1).params(1) = param(10);
FISnew.input(4).mf(2).params(1) = param(11);
FISnew.input(4).mf(3).params(1) = param(12);
FISnew.input(5).mf(1).params(1) = param(13);	
FISnew.input(5).mf(2).params(1) = param(14);	
FISnew.input(5).mf(3).params(1) = param(15);

% Координаты термов входных переменных
FISnew.input(1).mf(1).params(2) = param(16);
FISnew.input(1).mf(2).params(2) = param(17);
FISnew.input(1).mf(3).params(2) = param(18);
FISnew.input(2).mf(1).params(2) = param(19);
FISnew.input(2).mf(2).params(2) = param(20);
FISnew.input(2).mf(3).params(2) = param(21);
FISnew.input(3).mf(1).params(2) = param(22);
FISnew.input(3).mf(2).params(2) = param(23);
FISnew.input(3).mf(3).params(2) = param(24);
FISnew.input(4).mf(1).params(2) = param(25);
FISnew.input(4).mf(2).params(2) = param(26);
FISnew.input(4).mf(3).params(2) = param(27);
FISnew.input(5).mf(1).params(2) = param(28);
FISnew.input(5).mf(2).params(2) = param(29);
FISnew.input(5).mf(3).params(2) = param(30);

