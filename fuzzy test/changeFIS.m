function FISnew = changeFIS(param, FISold, Msht)
% Установка новых параметров (param) нечеткой системы FISold

FISnew = FISold;

% Демасштабирование настраиваемых параметров
param = param ./ Msht;

% Коэффициенты конццентрации термов входных переменных
FISnew.input(1).mf(1).params(1) = param(1);
FISnew.input(1).mf(2).params(1) = param(2);
FISnew.input(1).mf(3).params(1) = param(3);	
FISnew.input(1).mf(4).params(1) = param(4);	
FISnew.input(1).mf(5).params(1) = param(5);	

% Координаты термов входных переменных
FISnew.input(1).mf(1).params(2) = param(6);
FISnew.input(1).mf(2).params(2) = param(7);
FISnew.input(1).mf(3).params(2) = param(8);	
FISnew.input(1).mf(4).params(2) = param(9);	
FISnew.input(1).mf(5).params(2) = param(10);	

 